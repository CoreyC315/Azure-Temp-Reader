import azure.functions as func
import logging

app = func.FunctionApp()

@app.event_hub_message_trigger(arg_name="azeventhub", event_hub_name="events",
                               connection="TempReader_RootManageSharedAccessKey_EVENTHUB") 
def CosmosDbWriter(azeventhub: func.EventHubEvent):
    logging.info('Python EventHub trigger processed an event: %s',
                azeventhub.get_body().decode('utf-8'))


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
