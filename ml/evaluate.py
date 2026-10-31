import os
import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
from model import TelemetryMLP
from data_prep import load_channel_data, normalize_data

CHANNEL_ID = "B-1"
WINDOW_SIZE = 32
NUM_FEATURES = 25
STD_MULTIPLIER = 3.0  
DATA_DIR = "data"

def evaluate_model():
    print(f"Starting evaluation pipeline for channel: {CHANNEL_ID}...")

    train_data, test_data = load_channel_data(channel_id=CHANNEL_ID, data_dir=DATA_DIR)
    train_norm, test_norm, mean, std_safe = normalize_data(train_data, test_data)

    train_norm = np.clip(train_norm, -5.0, 5.0)
    test_norm = np.clip(test_norm, -5.0, 5.0)   

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = TelemetryMLP(window_size=WINDOW_SIZE, num_features=NUM_FEATURES, hidden_dim=64).to(device)
    
    model_path = "saved_models/best_model.pth"
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Trained model weights not found at {model_path}. Run train.py first!")
    
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    print("Successfully loaded 'best_model.pth'. Model locked in evaluation mode.")

    X_test, y_test = [], []
    for i in range(len(test_norm) - WINDOW_SIZE):
        X_test.append(test_norm[i : i + WINDOW_SIZE])
        y_test.append([test_norm[i + WINDOW_SIZE, 0]]) 

    X_test = torch.tensor(np.array(X_test), dtype=torch.float32).to(device)
    y_test = torch.tensor(np.array(y_test), dtype=torch.float32).to(device)

    criterion = nn.MSELoss(reduction='none')
    with torch.no_grad():
        predictions = model(X_test)
        mse_errors = criterion(predictions, y_test).mean(dim=1).cpu().numpy()

    test_timestamps = []
    base_time = pd.Timestamp("2026-01-01 00:00:00")
    for idx in range(WINDOW_SIZE, len(test_norm)):
        test_timestamps.append(base_time + pd.Timedelta(minutes=idx))

    mu = np.mean(mse_errors)
    sigma = np.std(mse_errors)
    threshold = mu + (STD_MULTIPLIER * sigma)
    
    model_flags = mse_errors > threshold
    print(f"Threshold calculated: {threshold:.5f} (Mean: {mu:.5f}, Std: {sigma:.5f})")

    conn = psycopg2.connect(
        dbname="nasa_telemetry",
        user="postgres",
        password="Klarizzem22",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    query = """
        SELECT start_time, end_time, description 
        FROM anomaly_labels 
        WHERE channel_id = %s;
    """
    cur.execute(query, (CHANNEL_ID,))
    nasa_windows = cur.fetchall()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS detected_anomalies (
            id SERIAL PRIMARY KEY,
            channel_id VARCHAR(50),
            timestamp TIMESTAMP,
            actual_value FLOAT,
            predicted_value FLOAT,
            residual_error FLOAT,
            threshold FLOAT,
            is_correct BOOLEAN
        );
    """)

    gt_binary = np.zeros(len(test_timestamps), dtype=int)
    for start_t, end_t, _ in nasa_windows:
        mask = (pd.Series(test_timestamps) >= start_t) & (pd.Series(test_timestamps) <= end_t)
        gt_binary[mask.values] = 1

    pred_binary = model_flags.astype(int)

    true_positives = np.sum((pred_binary == 1) & (gt_binary == 1))
    false_positives = np.sum((pred_binary == 1) & (gt_binary == 0))
    false_negatives = np.sum((pred_binary == 0) & (gt_binary == 1))

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0
    f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    print("\n" + "="*50)
    print(f"--- EVALUATION RESULTS FOR CHANNEL {CHANNEL_ID} ---")
    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1-Score  : {f1_score:.4f}")
    print("="*50 + "\n")

    anomaly_rows_to_insert = []
    for idx, (ts, err, is_flagged) in enumerate(zip(test_timestamps, mse_errors, model_flags)):
        if is_flagged:

            is_correct = False
            for start_t, end_t, _ in nasa_windows:
                if start_t <= ts <= end_t:
                    is_correct = True
                    break
            
            actual_val = float(test_norm[WINDOW_SIZE + idx, 0])
            pred_val = float(predictions[idx, 0].item())
            anomaly_rows_to_insert.append((CHANNEL_ID, ts, actual_val, pred_val, float(err), float(threshold), is_correct))

    if anomaly_rows_to_insert:
        from psycopg2.extras import execute_values
        execute_values(cur, """
            INSERT INTO detected_anomalies 
            (channel_id, timestamp, actual_value, predicted_value, residual_error, threshold, is_correct)
            VALUES %s
        """, anomaly_rows_to_insert)
        print(f"Logged {len(anomaly_rows_to_insert)} flagged anomaly points into PostgreSQL.")

    
    conn.commit()
    cur.close()
    conn.close()

    plt.figure(figsize=(12, 6))
    plt.plot(test_timestamps, mse_errors, label='Model Residual MSE', color='blue', alpha=0.7, linewidth=1)
    plt.axhline(y=threshold, color='red', linestyle='--', label=f'Threshold ({STD_MULTIPLIER}*Std)', linewidth=1.5)

    for start_t, end_t, desc in nasa_windows:
        plt.axvspan(start_t, end_t, color='red', alpha=0.2, label='NASA Ground Truth Anomaly')

    plt.title(f'Anomaly Detection Evaluation - Channel {CHANNEL_ID}')
    plt.xlabel('Timeline')
    plt.ylabel('Mean Squared Error')

    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='upper right')
    
    plt.tight_layout()
    plt.savefig('anomaly_detection.pdf')
    print("Evaluation plot successfully saved to 'anomaly_detection.pdf'.")

if __name__ == "__main__":
    evaluate_model()