# Kafka Streaming Anomaly Detector

A real-time data engineering pipeline designed to ingest server logs and detect network intrusions using unsupervised deep learning. While traditional batch-processing creates a critical vulnerability window for zero-day attacks, this project shifts to an event-driven architecture by streaming continuous network logs through an Apache Kafka cluster. Rather than relying on static, rule-based alerts, the data stream is consumed in real-time by a PyTorch Autoencoder. This model learns the latent representation of baseline traffic, dynamically flagging potential intrusions via high reconstruction loss before they can propagate across the network.

## Core Architecture

* **Message Broker:** Apache Kafka handles the data stream, decoupling the log generation from the inference engine to ensure high-throughput scalability.
* **Inference Engine:** A custom Autoencoder built with PyTorch. It is trained to compress and reconstruct standard network traffic. Traffic that results in a high MSE loss during reconstruction is dynamically flagged as anomalous.
* **Containerization:** Kafka and Zookeeper are orchestrated via Docker Compose for rapid, isolated environment deployment without local dependency conflicts.

## Tech Stack

* **Language:** Python
* **Data Engineering:** Apache Kafka, Zookeeper
* **Machine Learning:** PyTorch, NumPy
* **Infrastructure:** Docker

## Local Setup

Ensure you have Docker and Python installed on your system. 

```bash
# 1. Clone the repository
git clone [https://github.com/nolanefe/kafka-streaming-anomaly-detector.git](https://github.com/nolanefe/kafka-streaming-anomaly-detector.git)
cd kafka-streaming-anomaly-detector

# 2. Install Python dependencies
pip install -r requirements.txt

# 3. Spin up the Kafka & Zookeeper cluster in the background
docker-compose up -d

# 4. Generate the base Autoencoder weights
python train_model.py

# 5. Open a new terminal window and start generating simulated traffic
python producer.py

# 6. Open another new terminal window and start the real-time detector
python stream_detector.py

# 7. When finished, shut down the cluster and remove background containers
docker-compose down