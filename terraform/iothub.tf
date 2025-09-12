# The IoT hub itself
resource "azurerm_iothub" "temp_reader_iothub" {
  name                = "TempReaderIoT-${random_string.unique_suffix.result}"
  resource_group_name = azurerm_resource_group.temp_reader_rgtf.name
  location            = azurerm_eventhub_namespace.Temp-Reader-EHNTF.location
  sku {
    name  = "F1"
    capacity = 1
  }
}

# The IoT Hub Endpoint acts as a bridge, defining the Event Hub as a destination for messages.
resource "azurerm_iothub_endpoint_eventhub" "eventhub_endpoint" {
  name                = "iot-eventhub-endpoint"
  resource_group_name = azurerm_resource_group.temp_reader_rgtf.name
  iothub_id           = azurerm_iothub.temp_reader_iothub.id
  connection_string   = azurerm_eventhub_authorization_rule.eventhub_rule.primary_connection_string
  
}

# The IoT hub routing to the event hub
resource "azurerm_iothub_route" "eventhub_route" {
  name                = "default_route"
  resource_group_name = azurerm_resource_group.temp_reader_rgtf.name
  iothub_name         = azurerm_iothub.temp_reader_iothub.name
  source              = "DeviceMessages"
  condition           = "true"
  endpoint_names      = [ azurerm_iothub_endpoint_eventhub.eventhub_endpoint.name ]
  enabled             = true
  
}