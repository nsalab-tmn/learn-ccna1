resource "azurerm_virtual_network" "vnet" {
  name                = "vnet-${var.lab_instance}-${random_string.learn.result}"
  address_space       = ["10.0.0.0/16"]
  location            = var.location_01
  resource_group_name = azurerm_resource_group.main.name
}

resource "azurerm_subnet" "public-subnet" {
  name                 = "public-subnet"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes       = ["10.0.0.0/24"]
}

resource "azurerm_network_interface" "vif" {
  name                = "vif-${var.lab_instance}-${random_string.learn.result}"
  location            = var.location_01
  resource_group_name = azurerm_resource_group.main.name

  ip_configuration {
    name                          = "public-${var.lab_instance}-${random_string.learn.result}"
    subnet_id                     = azurerm_subnet.public-subnet.id
    private_ip_address_allocation = "Static" #have to be Dynamic according to template. why?
    private_ip_address_version    = "IPv4"
    primary                       = true
    private_ip_address            = "10.0.0.10"
    public_ip_address_id          = azurerm_public_ip.pip.id
  }
}

resource "azurerm_public_ip" "pip" {
  name                    = "pip-${var.lab_instance}-${random_string.learn.result}"
  location                = var.location_01
  resource_group_name     = azurerm_resource_group.main.name
  sku                     = "Basic"
  allocation_method       = "Static"
  ip_version              = "IPv4"
  idle_timeout_in_minutes = 4
}
