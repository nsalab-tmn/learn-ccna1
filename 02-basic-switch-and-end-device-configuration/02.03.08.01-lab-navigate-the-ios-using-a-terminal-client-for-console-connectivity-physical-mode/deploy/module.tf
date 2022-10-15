module "pt_lab" {
    source = "./pt-lab"
    count = 1
}

output "URL" {
  value =  module.pt_lab[0].URL 
  description = "Main portal address"
}

output "learn_password" {
  value =  module.pt_lab[0].learn_password 
  description = "Main Password"  
}

output "learn_user" {
  value =  module.pt_lab[0].learn_user 
  description = "Main User"
}

output "pt_url" {
  value       = module.pt_lab[0].pt_url
  description = "PT API address"
}

output "pt_api_port" {
  value       = 8080
  description = "PT API port"
}