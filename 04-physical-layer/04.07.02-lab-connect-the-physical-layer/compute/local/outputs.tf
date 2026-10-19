# These outputs become tf-dynamic-params.json (raw `terraform output` envelope),
# read by learn-assessment. The address is the container's learn-labs IP / DNS name
# — an assessment-reachable address on the shared network, NEVER localhost (the
# grader runs in a sibling container on learn-labs).

output "lab_host" {
  description = "Docker DNS name (= container name) on learn-labs."
  value       = docker_container.lab.name
}

output "lab_ip" {
  description = "Container IP on the learn-labs network (never localhost)."
  value = one([
    for n in docker_container.lab.network_data : n.ip_address
    if n.network_name == "learn-labs"
  ])
}

output "ssh_port" {
  description = "Legacy alias: SSH port of the first simulated device (East)."
  value       = 22
}

# One SSH port per simulated device: the base port + its topology id (read from
# topology.yaml, so reordering the devices can't silently break grading). Output
# names are static in Terraform: add one block per simulated device.
output "ssh_port_East" {
  description = "SSH port of East (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["East"]
}

output "ssh_port_West" {
  description = "SSH port of West (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["West"]
}

output "ssh_port_Switch1" {
  description = "SSH port of Switch1 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Switch1"]
}

output "ssh_port_Switch4" {
  description = "SSH port of Switch4 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Switch4"]
}

output "ssh_port_Switch3" {
  description = "SSH port of Switch3 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Switch3"]
}

output "ssh_port_Switch2" {
  description = "SSH port of Switch2 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Switch2"]
}

output "ssh_port_PC1" {
  description = "SSH port of PC1 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["PC1"]
}

output "ssh_port_PC2" {
  description = "SSH port of PC2 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["PC2"]
}

output "ssh_port_PC3" {
  description = "SSH port of PC3 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["PC3"]
}

output "ssh_port_PC4" {
  description = "SSH port of PC4 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["PC4"]
}

output "ssh_port_PC5" {
  description = "SSH port of PC5 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["PC5"]
}

output "ssh_port_PC6" {
  description = "SSH port of PC6 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["PC6"]
}

output "ssh_port_PC7" {
  description = "SSH port of PC7 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["PC7"]
}

output "ssh_port_PC8" {
  description = "SSH port of PC8 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["PC8"]
}

output "ssh_port_PC9" {
  description = "SSH port of PC9 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["PC9"]
}

output "ssh_user" {
  description = "SSH username."
  value       = "admin"
}

output "ssh_password" {
  description = "Per-lab SSH password."
  value       = random_password.ssh.result
  sensitive   = true
}

output "URL" {
  description = "Student web canvas (topology + in-page device console) — the platform edge proxies this to the learner."
  value       = "http://${docker_container.lab.name}:7681/"
}
