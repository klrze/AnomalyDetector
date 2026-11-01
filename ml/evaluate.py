import os
import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
from model import TelemetryMLP
from data_prep import load_channel_data, normalize_data, create_dataloaders

CHANNEL_ID = "C-1"
WINDOW_SIZE = 32
STD_MULTIPLIER = 1.5  # Adjusted for better sensitivity
DATA_DIR = "data"

def evaluate_model():
    print(f"Starting evaluation pipeline for channel: {CHANNEL_ID}...")

    train_data, test_data = load_channel_data(channel_id=CHANNEL_ID, data_dir=DATA_DIR)
    train_norm, test_norm, mean, std_safe = normalize_data(train_data, test_data)

    train_norm = np.clip(train_norm, -5.0, 5.0)
    test_norm = np.clip(test_norm, -5.0, 5.0)   

    # Re-create dataloader briefly just to extract matching input_dim dynamically
    temp_train_loader, _ = create_dataloaders(train_norm, test_norm, window_size=WINDOW_SIZE, batch_size=64)
    sample_x, _ = next(iter(temp_train_loader))
    input_dim = sample_x.shape[1] * sample_x.shape[2]

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = TelemetryMLP(input_dim=input_dim, hidden_dim=128).to(device)
    
    model_path = "saved_models/best_model.pth"
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Trained model weights not found at {model_path}. Run train.py first!")
    
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    print("Successfully loaded 'best_model.pth' with matching input dimensions.")

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
        dbname="nasa_telemetry", user="postgres", password="Klarizzem22", host="localhost", port="5432"
    )
    cur = conn.cursor()

    cur.execute("SELECT start_time, end_time, description FROM anomaly_labels WHERE channel_id = %s;", (CHANNEL_ID,))
    nasa_windows = cur.fetchall()

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

    cur.close()
    conn.close()

if __name__ == "__main__":
    evaluate_model()