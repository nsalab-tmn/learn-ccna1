resource "azurerm_linux_virtual_machine" "vm" {
  name                            = "vm-${var.lab_instance}-${random_string.learn.result}"
  resource_group_name             = azurerm_resource_group.main.name
  location                        = var.location_01
  size                            = "Standard_DS1_v2"
  admin_username                  = var.adminuser
  admin_password                  = var.adminpassword
  disable_password_authentication = false
  provision_vm_agent              = true


  allow_extension_operations = true
  computer_name              = "vm-${var.lab_instance}-${random_string.learn.result}"
  network_interface_ids = [
    azurerm_network_interface.vif.id,
  ]

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "StandardSSD_LRS"
    disk_size_gb         = 30
    name                 = "disk-${var.lab_instance}-${random_string.learn.result}"
  }

  source_image_id  = "/subscriptions/e458e65e-3c18-4049-88a8-2f0430253fc0/resourceGroups/nsalab-prod/providers/Microsoft.Compute/galleries/pt/images/pt-lab/versions/1.0.2"
  
  custom_data = base64encode(templatefile("${path.module}/user_data.tpl", {
    admin_pass   = var.adminpassword,
    student_pass = random_string.learn.result,
    hostname     = "vm-${random_string.learn.result}"
    }
  )
)
}