Use your raspberry pi and make sure it is fully updated and upgraded.

Use these libraries. Make sure they are downloaded for the script.

```bash
SCRIPT HERE
```

make sure that your dht11 sensor is connected properlly.

Here is the code that I used to connect to the IoT Hub:

```bash
import RPi.GPIO as GPIO
import dht11
import time
import datetime
import json  # Import the JSON library to format our data

# Import the Azure IoT Hub libraries
from azure.iot.device import IoTHubDeviceClient, Message

# YOUR AZURE IOT HUB CONNECTION STRING

CONNECTION_STRING = "CONNECTION_STRING_HERE"

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



Set up your Azure IoT hub
<img width="960" height="1020" alt="image" src="https://github.com/user-attachments/assets/117fca09-3ee4-459b-bd4c-e82ca6f88e7e" />
