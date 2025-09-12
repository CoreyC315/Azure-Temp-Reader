resource "azurerm_signalr_service" "signalR" {
  name = "Temp-Reader-SRTF-${random_string.unique_suffix.result}"
  location = azurerm_resource_group.temp_reader_rgtf.location
  resource_group_name = azurerm_resource_group.temp_reader_rgtf.name

  sku {
    name = "Free_F1"
    capacity = 1
  }

  cors {
    allowed_origins = ["*"]
  }

  service_mode = "Serverless"
}