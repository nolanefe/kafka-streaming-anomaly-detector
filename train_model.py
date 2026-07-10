import torch
import torch.nn as nn
import os

# Define the Autoencoder architecture
class NetworkAutoencoder(nn.Module):
    def __init__(self, input_dim=10):
        super(NetworkAutoencoder, self).__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 6),
            nn.ReLU(),
            nn.Linear(6, 3),
            nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(3, 6),
            nn.ReLU(),
            nn.Linear(6, input_dim),
            nn.Sigmoid()
        )

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

if __name__ == "__main__":
    print("Training base autoencoder on baseline network data...")
    model = NetworkAutoencoder(input_dim=10)
    
    # In a real scenario, this would train on a baseline dataset of normal traffic.
    # Here, we initialize the weights and save it to act as our "pretrained" model.
    torch.save(model.state_dict(), 'autoencoder.pth')
    print("Model weights saved to autoencoder.pth")