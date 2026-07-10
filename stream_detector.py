from kafka import KafkaConsumer
import torch
import torch.nn as nn
import json
from train_model import NetworkAutoencoder

# 1. Load the architecture and the trained weights
model = NetworkAutoencoder(input_dim=10)
model.load_state_dict(torch.load('autoencoder.pth'))
model.eval()

# 2. Connect to the Kafka stream
consumer = KafkaConsumer(
    'server-logs',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='latest',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("Listening for anomalous network traffic...")

# 3. Process the stream in real-time
for message in consumer:
    log_data = message.value
    
    # Convert incoming log features to a PyTorch tensor
    tensor_data = torch.tensor(log_data['features'], dtype=torch.float32)
    
    # Run inference without tracking gradients (saves memory/compute)
    with torch.no_grad():
        reconstruction = model(tensor_data)
        
        # Calculate Mean Squared Error (MSE) reconstruction loss
        loss = nn.functional.mse_loss(reconstruction, tensor_data)
        
        # If the model can't reconstruct the data well, it's an anomaly
        if loss.item() > 0.15: 
            print(f"🚨 ALERT: High-loss traffic detected! IP: {log_data['ip']} | Loss: {loss.item():.4f}")