# Lets set up the PI

You are going to need a DHT11 Sensor and some cables to connect it to the pi

Connect power to pin 4, Ground to pin 6, and the reader to pin 7

Next go into you pi and make sure that it you set up a virtual enviroment with this code

```bash
python -m venv myenv
```

Then install these libraries
```bash
pip3 install RPi.GPIO
pip3 install RPi.dht11
pip3 install azure-iot-device
```

Next make a file called temp_reader.py and get this code into it

```bash
import RPi.GPIO as GPIO
import dht11
import time
import datetime
import json  # Import the JSON library to format our data

# Import the Azure IoT Hub libraries
from azure.iot.device import IoTHubDeviceClient, Message

# =================================================================
# YOUR AZURE IOT HUB CONNECTION STRING
# =================================================================
# IMPORTANT: Replace this with your actual device connection string
CONNECTION_STRING = "******CONNECTION STRING******"

# =================================================================
# SENSOR SETUP
# =================================================================
# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# read data using pin 4
instance = dht11.DHT11(pin = 4)

# =================================================================
# AZURE IOT HUB CLIENT SETUP
# =================================================================
def create_client():
    """
    Connects to Azure IoT Hub using the device connection string.
    """
    try:
        # Create a client that will connect to the IoT Hub via MQTT
        client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
        return client
    except Exception as ex:
        print(f"Error creating client: {ex}")
        return None

def send_telemetry(client, temperature, humidity):
    """
    Formats the data and sends it as a message to IoT Hub.
    """
    try:
        # Create a JSON payload with our sensor data
        telemetry_data = {
            "temperature_c": temperature,
            "humidity": humidity
        }
        # Convert the dictionary to a JSON string
        msg = json.dumps(telemetry_data)

        # Create an Azure IoT Hub message object
        message = Message(msg)

        # Send the message to IoT Hub
        print(f"Sending message: {message}")
        client.send_message(message)
        print("Message successfully sent!")

    except Exception as ex:
        print(f"Error sending message: {ex}")

# =================================================================
# MAIN LOOP
# =================================================================
def main():
    """
    The main loop that reads the sensor and sends data.
    """
    client = create_client()
    if not client:
        print("Could not create IoT Hub client. Exiting.")
        return

    # Start the IoT Hub client
    client.connect()

    while True:
        try:
            # Read sensor data from the DHT11
            result = instance.read()

            if result.is_valid():
                temperature_c = result.temperature
                humidity = result.humidity

                print("Last valid input: " + str(datetime.datetime.now()))
                print("Temperature: %-3.1f C" % temperature_c)
                print("Humidity: %-3.1f %%" % humidity)

                # Send the data to Azure IoT Hub
                send_telemetry(client, temperature_c, humidity)

            else:
                print("Failed to get a valid reading. Retrying...")

        except Exception as ex:
            print(f"An unexpected error occurred: {ex}")
            # In a real-world scenario, you might want to handle disconnections
            # and reconnections more gracefully here.

        time.sleep(10) # Wait for 10 seconds before the next reading

    # Once the loop is exited, disconnect the client
    client.disconnect()


if __name__ == "__main__":
    main()
```

# Now before we run it we are going to need a connection string to our azure resource.

From here we are going to make an Azure IoT hub to accept the JSON objects that are being sent out from the pi

Should look like this. (I have the errors becuase I have one already running.)

<img width="1688" height="1618" alt="image" src="https://github.com/user-attachments/assets/179e297c-61de-4c79-bb00-48a77034d14f" />

Once Created it should look like this

<img width="1688" height="1618" alt="image" src="https://github.com/user-attachments/assets/6700117f-1b27-4823-896a-863280cbc403" />

Go here and go to devices and create a device

<img width="1688" height="1618" alt="image" src="https://github.com/user-attachments/assets/f15143b2-7791-41cf-ba62-1c9d698fdaf7" />

Once made go into the device and get the primary connection string

<img width="1688" height="1618" alt="image" src="https://github.com/user-attachments/assets/79473a41-001b-4b05-af89-eff29e11a53d" />

Once you have the primary conection string put it into your pi script where it says connection string and run it

You should be getting successful messages going to the IoT hub
