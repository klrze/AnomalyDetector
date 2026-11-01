import torch
import torch.nn as nn

class TelemetryMLP(nn.Module):
    
    def __init__(self, input_dim, num_features=25, hidden_dim=128, dropout_rate=0.2):
        super().__init__()
        
        
        
        self.network = nn.Sequential(

            nn.Flatten(), 
            
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout_rate), 

            nn.Linear(hidden_dim, hidden_dim // 2),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
          
            nn.Linear(hidden_dim // 2, 1)
        )

    def forward(self, x):

        return self.network(x)