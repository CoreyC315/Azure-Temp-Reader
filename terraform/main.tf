terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "random_string" "unique_suffix" {
  length  = 5
  special = false
  upper   = false
}

resource "azurerm_resource_group" "temp_reader_rgtf" {
  name     = "TempReaderRGTF"
  location = "eastus2" 
}

resource "local_file" "index_html" {
  filename = "${path.module}/content/index.html"
  content = templatefile("${path.module}/../content/index.html.tpl", {
    API_BASE_URL = azurerm_linux_function_app.function_app.default_hostname
    DEFAULT_DEVICE_ID = "raspberrypi-dht11"
  })
}
