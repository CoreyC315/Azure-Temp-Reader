<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Real-time Weather Stream</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="container">
    <header>
      <h1>Real-time Weather Dashboard</h1>
      <p id="status-message">Connecting to SignalR and fetching historical data...</p>
      <a href="https://github.com/CoreyC315/Azure-Temp-Reader" target="_blank">
        View this project on GitHub
    </a>
    </header>
    <main>
      <section class="current-data">
        <h2>Current Data</h2>
        <div class="data-card">
          <p><strong>Device ID:</strong> <span id="deviceId">N/A</span></p>
          <p><strong>Temperature:</strong> <span id="temperature">N/A</span> °C</p>
          <p><strong>Humidity:</strong> <span id="humidity">N/A</span> %</p>
        </div>
      </section>
      <section class="historical-data">
        <h2>Historical Temperature</h2>
        <div class="chart-container">
          <canvas id="temperatureChart"></canvas>
        </div>
      </section>
    </main>
  </div> 
  <script src="https://cdnjs.cloudflare.com/ajax/libs/microsoft-signalr/6.0.1/signalr.js"></script> 
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script> 
  <script>
    
    const HUB_NAME = "tempstream";
    const DEFAULT_DEVICE_ID = "${DEFAULT_DEVICE_ID}";
    let chart;

    async function fetchHistoricalData() {
        try {
            const response = await fetch(`https://${API_BASE_URL}/api/historicalData?deviceId=${DEFAULT_DEVICE_ID}`);
            const data = await response.json();
            data.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));

            if (data.length > 0) {
                const latestData = data[data.length - 1];
                document.getElementById('deviceId').innerText = latestData.deviceId;
                document.getElementById('temperature').innerText = latestData.temperature_c;
                document.getElementById('humidity').innerText = latestData.humidity;
            }

            const labels = data.map(item => new Date(item.timestamp).toLocaleTimeString());
            const temperatures = data.map(item => item.temperature_c);

            return { labels, temperatures };
        } catch (error) {
            console.error("Failed to fetch historical data:", error);
            return { labels: [], temperatures: [] };
        }
    }

    function initChart(labels, temperatures) {
        const ctx = document.getElementById('temperatureChart').getContext('2d');
        chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Temperature (°C)',
                    data: temperatures,
                    borderColor: '#1e88e5', // Blue color
                    tension: 0.1,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Time'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Temperature (°C)'
                        }
                    }
                }
            }
        });
    }

    async function startSignalRConnection() {
        try {
            const negotiateResponse = await fetch(`https://${API_BASE_URL}/api/negotiate`, {
                method: 'POST',
            });
            const connectionInfo = await negotiateResponse.json();

            const connection = new signalR.HubConnectionBuilder()
                .withUrl(connectionInfo.url, { accessTokenFactory: () => connectionInfo.accessToken })
                .build();

            connection.on('newMessage', (message) => {
                const data = JSON.parse(message);
                
                document.getElementById('deviceId').innerText = data.deviceId;
                document.getElementById('temperature').innerText = data.temperature_c;
                document.getElementById('humidity').innerText = data.humidity;

                if (chart) {
                    const time = new Date().toLocaleTimeString();
                    chart.data.labels.push(time);
                    chart.data.datasets[0].data.push(data.temperature_c);
                    
                    const maxPoints = 50;
                    if (chart.data.labels.length > maxPoints) {
                        chart.data.labels.shift();
                        chart.data.datasets[0].data.shift();
                    }
                    
                    chart.update();
                }
            });

            await connection.start();
            console.log("SignalR connection established successfully.");
            document.getElementById('status-message').innerText = "Connected! Waiting for data...";
        } catch (error) {
            console.error("SignalR connection failed:", error);
            document.getElementById('status-message').innerText = "Connection failed. Check console for details.";
        }
    }

    document.addEventListener('DOMContentLoaded', async () => {
        document.getElementById('status-message').innerText = "Connecting...";

        const { labels, temperatures } = await fetchHistoricalData();
        initChart(labels, temperatures);
        
        startSignalRConnection();
    });

  </script>
</body>
</html>