resource "azurerm_cosmosdb_account" "temp_reader_cosmosdb" {
  name                = "tempreadercdb-${random_string.unique_suffix.result}"
  resource_group_name = azurerm_resource_group.temp_reader_rgtf.name
  location            = azurerm_resource_group.temp_reader_rgtf.location
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"
  free_tier_enabled = true

  consistency_policy {
    consistency_level = "Session"
  }

  geo_location {
    location          = azurerm_resource_group.temp_reader_rgtf.location
    failover_priority = 0
  }
}

# The NoSQL database
resource "azurerm_cosmosdb_sql_database" "temp_reader_db" {
  name = "WeatherReadingDb"
  resource_group_name = azurerm_resource_group.temp_reader_rgtf.name
  account_name        = azurerm_cosmosdb_account.temp_reader_cosmosdb.name
}

# The container to store the data
resource "azurerm_cosmosdb_sql_container" "temp_reader_container" {
  name                = "TemperatureData_v2"
  resource_group_name = azurerm_resource_group.temp_reader_rgtf.name
  account_name        = azurerm_cosmosdb_account.temp_reader_cosmosdb.name
  database_name       = azurerm_cosmosdb_sql_database.temp_reader_db.name
  partition_key_paths  = ["/deviceId"]
}