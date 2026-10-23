import os
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader

def load_channel_data(channel_id, data_dir="data"):

    train_path = os.path.join(data_dir, "train", f"{channel_id}.npy")
    test_path = os.path.join(data_dir, "test", f"{channel_id}.npy")

    if not os.path.exists(train_path) or not os.path.exists(test_path):
        raise FileNotFoundError(
            f"Missing .npy files for channel '{channel_id}' inside {data_dir}"
        )

    train_data = np.load(train_path)
    test_data = np.load(test_path)

    return train_data, test_data

def normalize_data(train_data, test_data):

    mean = np.mean(train_data, axis=0)
    std = np.std(train_data, axis=0)

    std_safe = np.where(std == 0, 1.0, std)

    train_norm = (train_data - mean) / std_safe
    test_norm = (test_data - mean) / std_safe

    return train_norm, test_norm, mean, std_safe

class TelemetryDataset(Dataset):

    def __init__(self, data, window_size=32):
        self.data = torch.tensor(data, dtype=torch.float32)
        self.window_size = window_size

    def __len__(self):
        return len(self.data) - self.window_size

    def __getitem__(self, idx):
        x = self.data[idx : idx + self.window_size, :]
        y = self.data[idx + self.window_size, 0:1]
        return x, y

def create_dataloaders(train_norm, test_norm, window_size=32, batch_size=64):
    train_dataset = TelemetryDataset(train_norm, window_size=window_size)
    test_dataset = TelemetryDataset(test_norm, window_size=window_size)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    return train_loader, test_loader