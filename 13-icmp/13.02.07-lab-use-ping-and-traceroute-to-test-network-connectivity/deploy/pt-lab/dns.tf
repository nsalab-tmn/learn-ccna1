resource "azurerm_dns_a_record" "a_record" {
  name                = "${random_string.learn.result}"
  zone_name           = "az.skillscloud.company"
  resource_group_name = "nsalab-prod"
  ttl                 = 300
  records             = [vkcs_compute_instance.compute[0].access_ip_v4]
  tags = {
    "Provider" = "VKCS"
  }
}