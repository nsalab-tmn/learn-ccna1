variable prefix {
  default = "student"
}

variable lab_instance {
  default = "pt-lab"
}

variable "location_01" {
  default = "southcentralus"
  type = string
}

variable "adminuser" {
  default = "azadmin"
  type = string
}

variable "adminpassword" {
  default = "VeryLongP@ssw0rd"
  type = string
}

variable dns_root {
  default = "az.skillscloud.company"
}

variable "tp_learn_env" {
    type        = string
    default     = "dev"
}

variable "tp_learn_user" {
    type        = string
    default     = "user01"
}
