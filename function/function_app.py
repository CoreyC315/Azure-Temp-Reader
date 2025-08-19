import azure.functions as func
import logging
import json

app = func.FunctionApp()

@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="events",
                               connection="TempReader_RootManageSharedAccessKey_EVENTHUB") 

@app.cosmos_db_output(arg_name="outputDocument", database_name="WeatherReadingDb", 
                      container_name="TemperatureData", connection="CosmosDbConnection") 

def CosmosDbWriter(azeventhub: func.EventHubEvent, outputDocument: func.Out[func.Document]):
    logging.info('Python EventHub trigger processed an event: %s',
                azeventhub.get_body().decode('utf-8'))
    
    #Get the incoming message as a JSON object
    Message_body = azeventhub.get_body().decode('utf-8')
    data = json.loads(Message_body)

    #Add a timestamp and device ID to the document
    data['timestamp'] = azeventhub.enqueued_time.isoformat()
    data['deviceId'] = azeventhub.get_system_properties()['iothub-connection-deviceid']

    outputDocument.set(func.Document.from_dict(data))




# This example uses SDK types to directly access the underlying EventData object provided by the Event Hubs trigger.
# To use, uncomment the section below and add azurefunctions-extensions-bindings-eventhub to your requirements.txt file
# import azurefunctions.extensions.bindings.eventhub as eh
# @app.event_hub_message_trigger(
#     arg_name="event", event_hub_name="events", connection="TempReader_RootManageSharedAccessKey_EVENTHUB"
# )
# def CosmosDbWriter(event: eh.EventData):
#     logging.info(
#         "Python EventHub trigger processed an event %s",
#         event.body_as_str()
#     )
