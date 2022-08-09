output "learn_rg" {
  value       = azurerm_resource_group.learn.name
  description = "Main resource group"
  depends_on  = []
}

output "learn_user" {
  value       = azuread_user.learn.user_principal_name
  description = "Main User"
  depends_on  = []
}

output "learn_password" {
  value       = azuread_user.learn.password
  description = "Main Password"
  depends_on  = []
  sensitive   = true

}