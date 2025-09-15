# 🌐 IoT Environmental Monitoring Pipeline (Azure)



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

<img width="2823" height="847" alt="Exported-Diagram (1)" src="https://github.com/user-attachments/assets/b23f8336-bcf0-45f3-bb96-b0cbb86d5d26" />


---

## ✨ Features
- 📡 **Real-time streaming** – live sensor updates delivered via SignalR.  
- 📊 **Historical data storage** – last 20 data points retrieved from Cosmos DB for visualization.  
- 🔗 **Metadata enrichment** – each reading tagged with device ID and timestamp.  
- ☁️ **End-to-end Azure solution** – demonstrates IoT ingestion → processing → storage → visualization.  

---

## 🛠️ Technologies Used
- **Hardware:** Raspberry Pi 4, DHT11 sensor  
- **Azure Services:** IoT Hub, Event Hub, Functions, Cosmos DB, SignalR, Storage (Static Websites)  
- **Languages:** Python (for Pi scripts), JavaScript/HTML (frontend), C#/Python (Azure Functions)  

---

## 🚀 Getting Started
> Detailed setup instructions, deployment steps, and prerequisites are provided in the Documentation folder in the root.
At a high level:  
1. Clone the repo
2. Make sure that you have Terraform installed and Azure CLI
3. Open a terminal and log into a valid Azure account with a subscription
4. Go into the terraform file
5. Run terraform init
6. Run terraform plan
7. Run terraform apply
8. Next go into your function folder and run this
```bash
func azure functionapp publish Temp-Reader-Function(RandomID_assigned_by_terraform) --python
```
it might take a couple tries but it will start up
 

---

## 📚 Future Improvements
- Add **Terraform scripts** to provision the full pipeline automatically.  
- Extend the dashboard with **charts/graphs** (e.g., Plotly, Chart.js).  
- Expand to multiple devices with authentication & role-based access.  

---

## 📄 License
This project is open-source and available under the MIT License.  
