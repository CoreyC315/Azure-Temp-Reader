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
    """
    logging.info('Python HTTP trigger function processed a request for negotiate.')
    return func.HttpResponse(connectionInfo, mimetype="application/json")


@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="temp-reader-d72e3d957e",
                              connection="TempReader_RootManageSharedAccessKey_EVENTHUB",
                              consumer_group="$Default")
@app.generic_output_binding(arg_name="signalrMessages", type="signalR", hubName="tempstream", connectionStringSetting="AzureSignalRConnection")
@app.cosmos_db_output(arg_name="outputDocument", database_name="WeatherReadingDb",
                      container_name="TemperatureData_v2", connection="CosmosDbConnection",
                      create_if_not_exists=True, partition_key="/deviceId")
def EventHubProcessor(azeventhub: eh.EventData, signalrMessages: func.Out[str], outputDocument: func.Out[func.Document]):
    """
    Reads data from the Event Hub, writes it to Cosmos DB, and broadcasts it to SignalR clients.
    """
    logging.info('Python EventHub trigger processed an event: %s',
                 azeventhub.body_as_str())

    # Get the incoming message as a JSON object
    try:
        data = json.loads(azeventhub.body_as_str())
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON from event body.")
        return
    
    # Process for Cosmos DB
    enqueued_time_utc = azeventhub.system_properties.get('EnqueuedTimeUtc')
    if enqueued_time_utc:
        data['timestamp'] = enqueued_time_utc.isoformat()
    else:
        data['timestamp'] = datetime.datetime.utcnow().isoformat()
    
    if 'deviceId' not in data:
        logging.error("The incoming event payload does not contain the 'deviceId' key. The document will not be saved to Cosmos DB.")
        # You can choose to still broadcast the message even if the deviceId is missing.
    else:
        data['id'] = f"{data['deviceId']}-{str(uuid.uuid4())}"
        outputDocument.set(func.Document.from_dict(data))
        logging.info("Document successfully set for Cosmos DB.")

    # Process for SignalR
    message_body_str = azeventhub.body_as_str()
    signalr_message = {
        "target": "newMessage",
        "arguments": [message_body_str]
    }
    signalrMessages.set(json.dumps(signalr_message))
    logging.info('Broadcasting Event Hub message to SignalR: %s', signalr_message)

# You can keep your historical data function here if you are using it.
# @app.route(route="historicalData", ... )
# ...