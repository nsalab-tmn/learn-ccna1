module "pt-lab" {
    source = "./pt-lab"
    count = 1
    
    tp_learn_env = "${var.tp_learn_env}"
    tp_learn_user = "${var.tp_learn_user}"    
}

output "URL" {
  value =  module.pt-lab[0].URL 
  description = "Main portal address"
}

output "learn_password" {
  value =  module.pt-lab[0].learn_password 
  description = "Main Password"  
}

output "learn_user" {
  value =  module.pt-lab[0].learn_user 
  description = "Main User"
}

output "pt-url" {
  value       = module.pt-lab[0].pt-url
  description = "PT API address"
}

output "pt-api-port" {
  value       = 8080
  description = "PT API port"
}

variable "tp_learn_env" {
    type        = string
    default     = "dev"
}

variable "tp_learn_user" {
    type        = string
    default     = "user01"
}
