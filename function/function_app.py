import azure.functions as func
import logging
import json
import azurefunctions.extensions.bindings.eventhub as eh
import datetime
import uuid

app = func.FunctionApp()

@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="events",
                              connection="TempReader_RootManageSharedAccessKey_EVENTHUB")
@app.cosmos_db_output(arg_name="outputDocument", database_name="WeatherReadingDb",
                      container_name="TemperatureData_v2", connection="CosmosDbConnection",
                      create_if_not_exists=True, partition_key="/deviceId")
def CosmosDbWriter(azeventhub: eh.EventData, outputDocument: func.Out[func.Document]):
    logging.info('Python EventHub trigger processed an event: %s',
                 azeventhub.body_as_str())

    # Get the incoming message as a JSON object
    try:
        data = json.loads(azeventhub.body_as_str())
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON from event body.")
        return

    # The previous code assumed the 'iothub-connection-device-id' system property
    # would be present. Based on your error log, it seems the event is coming
    # from a standard Event Hub, not specifically an IoT Hub, so that property is missing.
    # We will now assume the 'deviceId' is part of the JSON payload.
    
    # Use .get() with a fallback value to avoid KeyError
    enqueued_time_utc = azeventhub.system_properties.get('EnqueuedTimeUtc')
    if enqueued_time_utc:
        data['timestamp'] = enqueued_time_utc.isoformat()
    else:
        # Fallback: Use the current time if the enqueued time is not available
        data['timestamp'] = datetime.datetime.utcnow().isoformat()
    
    # ⚠️ Check if the deviceId is in the incoming JSON payload.
    # If not, the function will not be able to write the data.
    if 'deviceId' not in data:
        logging.error("The incoming event payload does not contain the 'deviceId' key. Please ensure your device sends this information.")
        return # Exit the function if the partition key is missing
        
    # Every document needs a unique 'id' field for upsert operations.
    # A combination of the deviceId and a unique identifier works well.
    data['id'] = f"{data['deviceId']}-{str(uuid.uuid4())}"

    # Now that we have the partition key ('deviceId') and the unique 'id', we can set the document.
    outputDocument.set(func.Document.from_dict(data))