import torch
import torch.nn as nn
import torch.optim as optim
import psycopg2
import numpy as np
import matplotlib.pyplot as plt
from model import TelemetryMLP
from data_prep import load_channel_data, normalize_data, create_dataloaders

WINDOW_SIZE = 32
NUM_FEATURES = 25
BATCH_SIZE = 64
LEARNING_RATE = 0.001
MAX_EPOCHS = 50
PATIENCE = 5  

train_data, test_data = load_channel_data(channel_id="T-1", data_dir="data")
train_norm, test_norm, mean, std_safe = normalize_data(train_data, test_data)

train_loader, val_loader = create_dataloaders(
    train_norm, 
    test_norm, 
    window_size=WINDOW_SIZE, 
    batch_size=BATCH_SIZE
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = TelemetryMLP(window_size=WINDOW_SIZE, num_features=NUM_FEATURES, hidden_dim=128).to(device)
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

best_val_loss = float('inf')
patience_counter = 0
train_loss_history = []
val_loss_history = []
-
for epoch in range(MAX_EPOCHS):

    model.train()  
    running_train_loss = 0.0

    for batch_x, batch_y in train_loader:
        batch_x, batch_y = batch_x.to(device), batch_y.to(device)
        
        optimizer.zero_grad()               
        predictions = model(batch_x)        
        loss = criterion(predictions, batch_y) 
        loss.backward()                    
        optimizer.step()                    
        
        running_train_loss += loss.item()
        
    avg_train_loss = running_train_loss / len(train_loader)
    train_loss_history.append(avg_train_loss)

    model.eval()   
    running_val_loss = 0.0
    
    with torch.no_grad():
        for val_x, val_y in val_loader:
            val_x, val_y = val_x.to(device), val_y.to(device)
            
            val_preds = model(val_x)
            v_loss = criterion(val_preds, val_y)
            running_val_loss += v_loss.item()
            
    avg_val_loss = running_val_loss / len(val_loader)
    val_loss_history.append(avg_val_loss)
    
    print(f"Epoch [{epoch+1}/{MAX_EPOCHS}] | Train MSE: {avg_train_loss:.4f} | Val MSE: {avg_val_loss:.4f}")

    if avg_val_loss < best_val_loss:
        best_val_loss = avg_val_loss
        patience_counter = 0
        torch.save(model.state_dict(), 'saved_models/best_model.pth')
    else:
        patience_counter += 1
        
    if patience_counter >= PATIENCE:
        print(f"Early stopping triggered at epoch {epoch+1}. Restoring best weights.")
        break

plt.figure(figsize=(10, 6))
plt.plot(train_loss_history, label='Training Loss')
plt.plot(val_loss_history, label='Validation Loss')
plt.title('Model Learning Curve')
plt.xlabel('Epochs')
plt.ylabel('MSE Loss')
plt.legend()
plt.savefig('learning_curve.pdf')
print("Learning curve saved to 'learning_curve.pdf'.")

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

    record_data = (
        WINDOW_SIZE, BATCH_SIZE, LEARNING_RATE, (epoch + 1), 
        train_loss_history[-1], best_val_loss, None, 
        "128 hidden neurons, pure MSE physics training"
    )
    
    cur.execute(insert_query, record_data)
    conn.commit()
    
    cur.close()
    conn.close()
    print("Experiment successfully logged to PostgreSQL.")

except Exception as e:
    print(f"Database logging failed: {e}")

print("Training script execution complete. Factory closed.")