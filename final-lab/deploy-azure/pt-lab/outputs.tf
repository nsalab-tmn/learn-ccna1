output "URL" {
  value       = "https://${azurerm_dns_a_record.a_record.name}.${azurerm_dns_a_record.a_record.zone_name}"
  description = "Main portal address"
  depends_on  = []
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