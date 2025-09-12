# Storage Account to host the function
resource "azurerm_storage_account" "storage_account" {
  name = "tempreadersa${random_string.unique_suffix.result}"
  resource_group_name = azurerm_resource_group.temp_reader_rgtf.name
  location = azurerm_resource_group.temp_reader_rgtf.location
  account_tier = "Standard"
  account_replication_type = "LRS"
}

# The service plan for the function
resource "azurerm_service_plan" "service_plan" {
  name = "appserviceplan"
  location = azurerm_resource_group.temp_reader_rgtf.location
  resource_group_name = azurerm_resource_group.temp_reader_rgtf.name
  os_type = "Linux"
  sku_name = "S1"
}

# The function App itself
resource "azurerm_linux_function_app" "function_app" {
  name                       = "Temp-Reader-Function-${random_string.unique_suffix.result}"
  resource_group_name        = azurerm_resource_group.temp_reader_rgtf.name
  location                   = azurerm_resource_group.temp_reader_rgtf.location
  service_plan_id            = azurerm_service_plan.service_plan.id
  storage_account_name       = azurerm_storage_account.storage_account.name
  storage_account_access_key = azurerm_storage_account.storage_account.primary_access_key

  site_config {
    application_stack {
      python_version = "3.11"
    }

    cors {
      allowed_origins = [
        trim(azurerm_storage_account.static_website_storage.primary_web_endpoint, "/")
      ]
    }
  }

  app_settings = {
    "AzureWebJobsStorage"        = azurerm_storage_account.storage_account.primary_connection_string
    "FUNCTIONS_WORKER_RUNTIME"   = "python"
    "WEBSITE_RUN_FROM_PACKAGE"   = "1"
    "CosmosDbConnection"         = azurerm_cosmosdb_account.temp_reader_cosmosdb.primary_sql_connection_string
    "EventHubName"               = azurerm_eventhub.Temp-Reader-EH.name
    "TempReader_RootManageSharedAccessKey_EVENTHUB" = azurerm_eventhub_authorization_rule.eventhub_rule.primary_connection_string
    "CosmosDbDatabaseName"       = azurerm_cosmosdb_sql_database.temp_reader_db.name
    "CosmosDbContainerName"      = azurerm_cosmosdb_sql_container.temp_reader_container.name
    "SignalRConnectionString"    = azurerm_signalr_service.signalR.primary_connection_string
  }
}