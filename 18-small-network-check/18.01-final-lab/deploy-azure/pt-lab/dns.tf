resource "azurerm_dns_a_record" "a_record" {
  name                = "${random_string.learn.result}"
  zone_name           = "az.skillscloud.company"
  resource_group_name = "nsalab-prod"
  ttl                 = 300
  records             = [azurerm_public_ip.pip.ip_address]
}