terraform {
    required_providers {
        vkcs = {
            source = "vk-cs/vkcs"
            version = "~> 0.1.12" 
        }
    }
}

provider "vkcs" {
    username = "your_username@domain.org"
    password = "password"
    project_id = "666"
    region = "RegionOne"
    
    auth_url = "https://infra.mail.ru:35357/v3/" 
}

provider "azurerm" {
  features {}

  subscription_id = "e458e65e-3c18-4049-88a8-2f0430253fc0"
  tenant_id       = "055ebdfb-ef8c-499e-9ab2-ff28bc1c524d"
}