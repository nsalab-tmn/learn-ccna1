# Worker-injected variables (learn-lab-deploy passes these to every playbook) plus
# this material's own knobs. Keep names in sync with lab-deploy's tf_vars.

variable "instance_id" {
  description = "userMaterialId — unique per deployment; names the container."
  type        = string
}

variable "tp_name" {
  description = "materialId."
  type        = string
  default     = ""
}

variable "tp_learn_env" {
  description = "LEARN_ENV."
  type        = string
  default     = ""
}

variable "tp_learn_user" {
  description = "The learner's user name."
  type        = string
  default     = ""
}

variable "variant_seed" {
  description = "Per-variant seed (unused by this single-variant lab)."
  type        = string
  default     = "0"
}

variable "netsim_image" {
  description = "The learn-netsim image to run. Overridable for local/offline e2e."
  type        = string
  default     = "ghcr.io/nsalab-tmn/learn-netsim:latest"
}
