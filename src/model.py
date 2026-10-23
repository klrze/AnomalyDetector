import torch
import torch.nn as nn

class TelemetryMLP(nn.Module):
    
    def __init__(self, window_size=32, num_features=25, hidden_dim=128, dropout_rate=0.2):
        super().__init__()
        
        self.flattened_size = window_size * num_features
        
        self.network = nn.Sequential(

            nn.Flatten(), 
            
            nn.Linear(self.flattened_size, hidden_dim),
            2,
            nn.Dropout(dropout_rate), 

            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
          
            nn.Linear(hidden_dim // 2, 1)
        )

    def forward(self, x):

        return self.network(x)