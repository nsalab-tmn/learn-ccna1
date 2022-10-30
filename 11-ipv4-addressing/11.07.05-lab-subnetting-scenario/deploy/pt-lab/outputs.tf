output "URL" {
  value       = "https://${azurerm_dns_a_record.a_record.name}.${azurerm_dns_a_record.a_record.zone_name}"
  description = "Main portal address"
  depends_on  = []
}

output "pt-url" {
  value       = "${azurerm_dns_a_record.a_record.name}.${azurerm_dns_a_record.a_record.zone_name}"
  description = "PT API address"
  depends_on  = []
}

output "pt-api-port" {
  value       = 8080
  description = "PT API port"
  depends_on  = []
}

output "admin_pass" {
  value = var.root_password
  description = "Admin password"
}

output "learn_user" {
  value       =  "student"
  description = "Main User"
  depends_on  = []
}

output "learn_password" {
  value       = random_string.learn.result
  description = "Main Password"
  sensitive = false
  depends_on  = []
}