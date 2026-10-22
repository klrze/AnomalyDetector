import torch
import torch.nn as nn
import torch.optim as optim
import psycopg2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score
from torch.utils.data import DataLoader

# Assume these are imported from your Pillar 1 and Pillar 2 scripts
from model import TelemetryMLP
from dataset import NASATelemetryDataset 

# ==========================================
# 1. THE SETUP (Hyperparameters)
# ==========================================
WINDOW_SIZE = 32
NUM_FEATURES = 25
BATCH_SIZE = 64
LEARNING_RATE = 0.001
MAX_EPOCHS = 50
PATIENCE = 5  # Early stopping limit

# ==========================================
# 2. THE CONVEYOR BELT (DataLoaders)
# ==========================================
# Instantiating the datasets (assumes pre-processed .npy files from Pillar 1)
train_dataset = NASATelemetryDataset(data_path='data/train_data.npy', labels_path='data/train_labels.npy', window_size=WINDOW_SIZE)
val_dataset = NASATelemetryDataset(data_path='data/val_data.npy', labels_path='data/val_labels.npy', window_size=WINDOW_SIZE)

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)

# ==========================================
# 3. THE BLUEPRINT, GRADER, & MECHANIC
# ==========================================
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = TelemetryMLP(window_size=WINDOW_SIZE, num_features=NUM_FEATURES, hidden_dim=128).to(device)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

# Tracking variables for Early Stopping and Logging
best_val_loss = float('inf')
patience_counter = 0
train_loss_history = []
val_loss_history = []
final_f1_score = 0.0

# ==========================================
# 4. THE OUTER GEAR (Epoch Loop)
# ==========================================
for epoch in range(MAX_EPOCHS):
    
    # --- TRAINING PHASE ---
    model.train()  # Enables Dropout
    running_train_loss = 0.0
    
    # The Inner Gear (Batch Loop)
    for batch_x, batch_y, _ in train_loader:
        batch_x, batch_y = batch_x.to(device), batch_y.to(device)
        
        optimizer.zero_grad()               # Step 1: The Wipe
        predictions = model(batch_x)        # Step 2: The Forward Pass
        loss = criterion(predictions, batch_y) # Step 3: The Grader
        loss.backward()                     # Step 4: The Calculus
        optimizer.step()                    # Step 5: The Mechanic (Wrench)
        
        running_train_loss += loss.item()
        
    avg_train_loss = running_train_loss / len(train_loader)
    train_loss_history.append(avg_train_loss)

    # --- VALIDATION PHASE ---
    model.eval()   # Disables Dropout
    running_val_loss = 0.0
    all_errors = []
    all_true_labels = []
    
    with torch.no_grad(): # The Safety Lock (No backpropagation)
        for val_x, val_y, val_labels in val_loader:
            val_x, val_y = val_x.to(device), val_y.to(device)
            
            val_preds = model(val_x)
            v_loss = criterion(val_preds, val_y)
            running_val_loss += v_loss.item()
            
            # Calculate physical error gaps for anomaly detection
            errors = torch.abs(val_preds - val_y).cpu().numpy()
            all_errors.extend(errors)
            all_true_labels.extend(val_labels.numpy())
            
    avg_val_loss = running_val_loss / len(val_loader)
    val_loss_history.append(avg_val_loss)
    
    # Calculate F1 Score (Statistical Safety Threshold)
    error_mean = np.mean(all_errors)
    error_std = np.std(all_errors)
    threshold = error_mean + (4 * error_std) # 4 Standard Deviations
    
    predicted_anomalies = [1 if e > threshold else 0 for e in all_errors]
    current_f1 = f1_score(all_true_labels, predicted_anomalies)

    print(f"Epoch [{epoch+1}/{MAX_EPOCHS}] | Train MSE: {avg_train_loss:.4f} | Val MSE: {avg_val_loss:.4f} | Val F1: {current_f1:.4f}")

    # --- EARLY STOPPING & SAVING ---
    if avg_val_loss < best_val_loss:
        best_val_loss = avg_val_loss
        final_f1_score = current_f1
        patience_counter = 0
        torch.save(model.state_dict(), 'saved_models/best_model.pth')
    else:
        patience_counter += 1
        
    if patience_counter >= PATIENCE:
        print(f"Early stopping triggered at epoch {epoch+1}. Restoring best weights.")
        break

# ==========================================
# 5. THE SHUTDOWN SEQUENCE (Logging & DB)
# ==========================================

# A. Save the Learning Curve for LaTeX
plt.figure(figsize=(10, 6))
plt.plot(train_loss_history, label='Training Loss')
plt.plot(val_loss_history, label='Validation Loss')
plt.title('Model Learning Curve')
plt.xlabel('Epochs')
plt.ylabel('MSE Loss')
plt.legend()
plt.savefig('learning_curve.pdf')
print("Learning curve saved to 'learning_curve.pdf'.")

# B. Log the Experiment to PostgreSQL
try:
    conn = psycopg2.connect(
        dbname="nasa_telemetry", 
        user="postgres", 
        password="your_password", 
        host="localhost"
    )
    cur = conn.cursor()
    
    insert_query = """
        INSERT INTO experiment_log (
            window_size, batch_size, learning_rate, epochs, 
            final_train_loss, val_loss, f1_score, notes
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    
    # Note: Using the last recorded train_loss, but the best_val_loss and best f1_score
    record_data = (
        WINDOW_SIZE, BATCH_SIZE, LEARNING_RATE, (epoch + 1), 
        train_loss_history[-1], best_val_loss, final_f1_score, 
        "128 hidden neurons, 4-sigma threshold"
    )
    
    cur.execute(insert_query, record_data)
    conn.commit()
    
    cur.close()
    conn.close()
    print("Experiment successfully logged to PostgreSQL.")

except Exception as e:
    print(f"Database logging failed: {e}")

print("Training script execution complete. Factory closed.")