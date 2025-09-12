#Create a storage account for the static website

resource "azurerm_storage_account" "static_website_storage" {
  name = "tempreaderwebsite${random_string.unique_suffix.result}"
  resource_group_name = azurerm_resource_group.temp_reader_rgtf.name
  location = azurerm_resource_group.temp_reader_rgtf.location
  account_tier = "Standard"
  account_replication_type = "LRS"

  static_website {
    index_document = "index.html"
  }
}

resource "azurerm_storage_blob" "index_html_blob" {
  name = "index.html"
  storage_account_name = azurerm_storage_account.static_website_storage.name
  storage_container_name = "$web"
  type = "Block"
  source = local_file.index_html.filename
  content_type = "text/html"
}

#Upload the style.css file

resource "azurerm_storage_blob" "style_css_blob" {
  name                   = "style.css"
  storage_account_name   = azurerm_storage_account.static_website_storage.name
  storage_container_name = "$web"
  type                   = "Block"
  source                 = "${path.module}/../content/style.css"
  content_type           = "text/css"
}

output "static_website_endpoint" {
  value = azurerm_storage_account.static_website_storage.primary_web_endpoint
  description = "The primary endpoint for the static website."
}