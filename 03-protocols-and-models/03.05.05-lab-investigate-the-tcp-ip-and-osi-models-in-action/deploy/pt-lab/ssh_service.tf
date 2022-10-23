# data "external" "ssh_service_availability" {
#   program = ["/bin/bash", "${path.module}/ssh_keepalive_provider.sh"]

#   query = {
#     #url         = vkcs_compute_instance.compute[0].access_ip_v4
#     url         = "${azurerm_dns_a_record.a_record.name}.${azurerm_dns_a_record.a_record.zone_name}"
#     filter      = "vm-${random_string.learn.result}"
#     counter     = 200
#     sleep       = 5
#     prefix      = random_string.learn.result
#     password    = var.root_password
#   }

#   depends_on = [
#       resource.vkcs_compute_instance.compute
#   ]

# }