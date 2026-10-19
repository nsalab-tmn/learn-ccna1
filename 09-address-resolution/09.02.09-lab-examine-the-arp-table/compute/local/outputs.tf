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
  description = "Legacy alias: SSH port of the first simulated device (Router0)."
  value       = 22
}

# One SSH port per simulated device: the base port + its topology id (read from
# topology.yaml, so reordering the devices can't silently break grading). Output
# names are static in Terraform: add one block per simulated device.
output "ssh_port_Router0" {
  description = "SSH port of Router0 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Router0"]
}

output "ssh_port_Router1" {
  description = "SSH port of Router1 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Router1"]
}

output "ssh_port_Switch0" {
  description = "SSH port of Switch0 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Switch0"]
}

output "ssh_port_Access-Point" {
  description = "SSH port of Access-Point (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Access-Point"]
}

output "ssh_port_Switch1" {
  description = "SSH port of Switch1 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Switch1"]
}

output "ssh_port_Laptop-10-2" {
  description = "SSH port of Laptop-10-2 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Laptop-10-2"]
}

output "ssh_port_Laptop-10-3" {
  description = "SSH port of Laptop-10-3 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Laptop-10-3"]
}

output "ssh_port_PC-31-2" {
  description = "SSH port of PC-31-2 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["PC-31-2"]
}

output "ssh_port_PC-31-3" {
  description = "SSH port of PC-31-3 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["PC-31-3"]
}

output "ssh_port_PC-31-4" {
  description = "SSH port of PC-31-4 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["PC-31-4"]
}

output "URL" {
  description = "Student web canvas (topology + in-page device console) — the platform edge proxies this to the learner."
  value       = "http://${docker_container.lab.name}:7681/"
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
