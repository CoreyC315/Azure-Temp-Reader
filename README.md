# 🌐 IoT Environmental Monitoring Pipeline (Azure)

![Architecture Diagram](./Exported-Diagram.png)

## 📌 Overview
This project demonstrates an **end-to-end IoT data pipeline** built with Azure cloud services.  
A Raspberry Pi with a **DHT11 sensor** collects temperature and humidity data, which is securely ingested into the cloud, processed, stored, and then displayed in real time via a web dashboard.  

The solution showcases **cloud engineering fundamentals** including device-to-cloud communication, event-driven processing, serverless compute, real-time updates, and time-series data storage.  

---

## ⚡ Architecture
1. **Raspberry Pi + DHT11 Sensor** → Captures temperature and humidity data.  
2. **Azure IoT Hub** → Ingests telemetry from IoT devices.  
3. **Azure Event Hub** → Routes streaming telemetry at scale.  
4. **Azure Functions** → Processes incoming messages, enriches with metadata (device ID, timestamp).  
5. **Azure Cosmos DB** → Stores historical telemetry data.  
6. **Azure SignalR Service** → Pushes live updates to connected clients.  
7. **Azure Storage (Static Website)** → Hosts a frontend dashboard to display live and recent readings.  

---

## ✨ Features
- 📡 **Real-time streaming** – live sensor updates delivered via SignalR.  
- 📊 **Historical data storage** – last 20 data points retrieved from Cosmos DB for visualization.  
- 🔗 **Metadata enrichment** – each reading tagged with device ID and timestamp.  
- ☁️ **End-to-end Azure solution** – demonstrates IoT ingestion → processing → storage → visualization.  

---

## 🛠️ Technologies Used
- **Hardware:** Raspberry Pi, DHT11 sensor  
- **Azure Services:** IoT Hub, Event Hub, Functions, Cosmos DB, SignalR, Storage (Static Websites)  
- **Languages:** Python (for Pi scripts), JavaScript/HTML (frontend), C#/Python (Azure Functions)  

---

## 🚀 Getting Started
> Detailed setup instructions, deployment steps, and prerequisites are provided in the [Setup Guide](./SETUP.md) (coming soon).  
At a high level:  
1. Configure Raspberry Pi to send DHT11 readings to Azure IoT Hub.  
2. Deploy Event Hub + Function App in Azure.  
3. Set up Cosmos DB + SignalR connections.  
4. Upload the static HTML dashboard to Azure Storage.  
5. Open the dashboard to see real-time updates!  

---

## 📚 Future Improvements
- Add **Terraform scripts** to provision the full pipeline automatically.  
- Extend the dashboard with **charts/graphs** (e.g., Plotly, Chart.js).  
- Integrate with **Power BI** for richer analytics.  
- Expand to multiple devices with authentication & role-based access.  

---

## 📄 License
This project is open-source and available under the MIT License.  
