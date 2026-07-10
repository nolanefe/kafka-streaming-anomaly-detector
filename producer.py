from kafka import KafkaProducer
import json
import time
import random
import numpy as np

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic_name = 'server-logs'

print(f"Starting network traffic simulation on topic: {topic_name}")

try:
    while True:
        # Simulate standard background traffic (features normalized between 0 and 1)
        features = np.random.uniform(0.1, 0.4, 10).tolist()
        ip_addr = f"192.168.1.{random.randint(1, 100)}"
        
        # Inject an anomaly 5% of the time (e.g., massive traffic spike)
        if random.random() < 0.05:
            features = np.random.uniform(0.8, 1.0, 10).tolist()
            ip_addr = f"10.0.0.{random.randint(1, 50)}" # Suspicious external IP
            
        log_payload = {
            "timestamp": time.time(),
            "ip": ip_addr,
            "features": features
        }
        
        producer.send(topic_name, log_payload)
        print(f"Sent log from {ip_addr}")
        time.sleep(0.5) # Send a log every half second

except KeyboardInterrupt:
    print("Simulation stopped.")
    producer.close()