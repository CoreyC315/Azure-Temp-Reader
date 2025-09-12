import azure.functions as func
import logging
import json
import azurefunctions.extensions.bindings.eventhub as eh
import datetime
import uuid
import azure.cosmos.cosmos_client as cosmos_client
import os

# Create the Function App instance
app = func.FunctionApp()

@app.route(route="negotiate", 
           auth_level=func.AuthLevel.ANONYMOUS, 
           methods=["POST"])

@app.generic_input_binding(arg_name="connectionInfo", 
                           type="signalRConnectionInfo", 
                           hubName="tempstream", 
                           connectionStringSetting="SignalRConnectionString")
def negotiate(req: func.HttpRequest, connectionInfo) -> func.HttpResponse:
    """
    HTTP-triggered function that provides connection info for SignalR clients.
    Clients call this endpoint to get a secure connection URL and access token.
    """
    logging.info('Python HTTP trigger function processed a request for negotiate.')
    return func.HttpResponse(connectionInfo, mimetype="application/json")


@app.event_hub_message_trigger(arg_name="azeventhub", 
                               event_hub_name=os.getenv("EventHubName"),    #"temp-reader-d72e3d957e",
                               connection="TempReader_RootManageSharedAccessKey_EVENTHUB",
                               consumer_group="$Default")
@app.generic_output_binding(arg_name="signalrMessages", 
                            type="signalR", 
                            hubName="tempstream", 
                            connectionStringSetting="SignalRConnectionString")
@app.cosmos_db_output(arg_name="outputDocument", 
                      database_name=os.getenv("CosmosDbDatabaseName"),    #"WeatherReadingDb",
                      container_name=os.getenv("CosmosDbContainerName"),     #"TemperatureData_v2", 
                      connection="CosmosDbConnection",     #"CosmosDbConnection",
                      create_if_not_exists=True, 
                      partition_key="/deviceId")
def EventHubProcessor(azeventhub: eh.EventData, signalrMessages: func.Out[str], outputDocument: func.Out[func.Document]):
    """
    Reads data from the Event Hub, writes it to Cosmos DB, and broadcasts it to SignalR clients.
    """
    logging.info('Python EventHub trigger processed an event: %s', azeventhub.body_as_str())
    
    # Log environment variables to confirm bindings are configured
    logging.info(f"Cosmos DB Database Name: {os.getenv('CosmosDbDatabaseName')}")
    logging.info(f"Cosmos DB Container Name: {os.getenv('CosmosDbContainerName')}")
    
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
    else:
        data['id'] = f"{data['deviceId']}-{str(uuid.uuid4())}"
        
        # Log the document data before setting it
        logging.info(f"Document to be written: {data}")
        
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

@app.route(route="historicalData", 
           auth_level=func.AuthLevel.ANONYMOUS, 
           methods=["GET"])
@app.cosmos_db_input(arg_name="documents", 
                     database_name=os.getenv("CosmosDbDatabaseName"),
                     container_name=os.getenv("CosmosDbContainerName"), 
                     connection="CosmosDbConnection",
                     sql_query="SELECT c.temperature_c, c.timestamp, c.deviceId, c.humidity FROM c WHERE c.deviceId = {deviceId} ORDER BY c.timestamp DESC OFFSET 0 LIMIT 10")
def historicalData(req: func.HttpRequest, documents: func.DocumentList) -> func.HttpResponse:
    """
    HTTP-triggered function that retrieves the 10 latest data points from Cosmos DB
    for a specified deviceId and returns them as a JSON array.
    """
    logging.info('Python HTTP trigger function processed a request for historicalData.')

    deviceId = req.params.get('deviceId')
    if not deviceId:
        return func.HttpResponse(
             "Please pass a deviceId on the query string",
             status_code=400
        )
    
    historical_data = [doc.to_dict() for doc in documents]
    
    return func.HttpResponse(
        json.dumps(historical_data),
        mimetype="application/json"
    )