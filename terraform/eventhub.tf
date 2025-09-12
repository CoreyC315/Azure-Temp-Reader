# The Event Hub Namespace, this is where the Event Hub will go
resource "azurerm_eventhub_namespace" "Temp-Reader-EHNTF" {
  name                = "Temp-Reader-EHTF"
  location            = azurerm_resource_group.temp_reader_rgtf.location
  resource_group_name = azurerm_resource_group.temp_reader_rgtf.name
  sku                 = "Standard"
  capacity            = 1
  
  tags = {
    terraform = "True"
  }
}

resource "azurerm_eventhub" "Temp-Reader-EH" {
  name                = "temp-reader-ioteh-${random_string.unique_suffix.result}"
  namespace_name      = azurerm_eventhub_namespace.Temp-Reader-EHNTF.name
  resource_group_name = azurerm_resource_group.temp_reader_rgtf.name
  partition_count     = 2
  message_retention   = 1
  
}

resource "azurerm_eventhub_authorization_rule" "eventhub_rule" {
  resource_group_name = azurerm_resource_group.temp_reader_rgtf.name
  name                = "eventhub_rule"
  namespace_name      = azurerm_eventhub_namespace.Temp-Reader-EHNTF.name
  eventhub_name       = azurerm_eventhub.Temp-Reader-EH.name

  listen = true
  send   = true
  manage = false  
}