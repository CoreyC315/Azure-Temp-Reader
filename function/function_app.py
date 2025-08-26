import azure.functions as func
import logging
import json
import azurefunctions.extensions.bindings.eventhub as eh
import datetime
import uuid

# Create the Function App instance
app = func.FunctionApp()

@app.route(route="negotiate", auth_level=func.AuthLevel.ANONYMOUS, methods=["POST"])
@app.generic_input_binding(arg_name="connectionInfo", type="signalRConnectionInfo", hubName="tempstream", connectionStringSetting="AzureSignalRConnection")
def negotiate(req: func.HttpRequest, connectionInfo) -> func.HttpResponse:
    """
    HTTP-triggered function that provides connection info for SignalR clients.
    Clients call this endpoint to get a secure connection URL and access token.
    This is essential for the frontend to connect to the SignalR service.
    """
    logging.info('Python HTTP trigger function processed a request for negotiate.')
    return func.HttpResponse(connectionInfo, mimetype="application/json")


@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="temp-reader-d72e3d957e",
                              connection="TempReader_RootManageSharedAccessKey_EVENTHUB")
@app.cosmos_db_output(arg_name="outputDocument", database_name="WeatherReadingDb",
                      container_name="TemperatureData_v2", connection="CosmosDbConnection",
                      create_if_not_exists=True, partition_key="/deviceId")
def CosmosDbWriter(azeventhub: eh.EventData, outputDocument: func.Out[func.Document]):
    """
    Writes data from the Event Hub to a Cosmos DB container.
    """
    logging.info('Python EventHub trigger processed an event: %s',
                 azeventhub.body_as_str())

    # Get the incoming message as a JSON object
    try:
        # Use body_as_str() to get the string content
        data = json.loads(azeventhub.body_as_str())
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON from event body.")
        return
    
    # Use .get() with a fallback value to avoid KeyError
    enqueued_time_utc = azeventhub.system_properties.get('EnqueuedTimeUtc')
    if enqueued_time_utc:
        data['timestamp'] = enqueued_time_utc.isoformat()
    else:
        # Fallback: Use the current time if the enqueued time is not available
        data['timestamp'] = datetime.datetime.utcnow().isoformat()
    
    # Check if the deviceId is in the incoming JSON payload.
    # If not, the function will not be able to write the data.
    if 'deviceId' not in data:
        logging.error("The incoming event payload does not contain the 'deviceId' key. Please ensure your device sends this information.")
        return # Exit the function if the partition key is missing
        
    # Every document needs a unique 'id' field for upsert operations.
    # A combination of the deviceId and a unique identifier works well.
    data['id'] = f"{data['deviceId']}-{str(uuid.uuid4())}"

    # Now that we have the partition key ('deviceId') and the unique 'id', we can set the document.
    outputDocument.set(func.Document.from_dict(data))

@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="temp-reader-d72e3d957e",
                                connection="TempReader_RootManageSharedAccessKey_EVENTHUB")
@app.generic_output_binding(arg_name="signalrMessages", type="signalR", hubName="tempstream", connectionStringSetting="AzureSignalRConnection")
def BroadcastSignalR(azeventhub: eh.EventData, signalrMessages: func.Out[str]):
    """
    Broadcasts the incoming Event Hub message to all connected SignalR clients.
    The message body is sent directly.
    """
    # Parse the incoming JSON string from Event Hub
    message_body_str = azeventhub.body_as_str()
    
    # Create the SignalR message object
    # It must contain 'target' and 'arguments' properties
    signalr_message = {
        "target": "newMessage",
        "arguments": [message_body_str] # Arguments must be a list
    }

    # Convert the Python dictionary to a JSON string and set the output binding
    signalrMessages.set(json.dumps(signalr_message))
    logging.info('Broadcasting Event Hub message to SignalR: %s', signalr_message)