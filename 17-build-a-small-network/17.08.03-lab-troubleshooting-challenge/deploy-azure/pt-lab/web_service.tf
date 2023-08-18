data "external" "web_service_availability" {
  program = ["/bin/bash", "${path.module}/web_keepalive_provider.sh"]

  query = {
    url         = "https://${azurerm_dns_a_record.a_record.name}.${var.dns_root}"
    filter      = "200 OK"
    counter     = 200
    sleep       = 5
    prefix      = random_string.learn.result
  }

  depends_on = [
      resource.azurerm_dns_a_record.a_record,
      resource.azurerm_linux_virtual_machine.vm
  ]

}