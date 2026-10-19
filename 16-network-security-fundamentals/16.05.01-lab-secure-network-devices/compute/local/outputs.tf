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
  description = "Legacy alias: SSH port of the first simulated device (RTR-A)."
  value       = 22
}

# One SSH port per simulated device: the base port + its topology id (read from
# topology.yaml, so reordering the devices can't silently break grading). Output
# names are static in Terraform: add one block per simulated device.
output "ssh_port_RTR-A" {
  description = "SSH port of RTR-A (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["RTR-A"]
}

output "ssh_port_SW-1" {
  description = "SSH port of SW-1 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["SW-1"]
}

output "ssh_port_SW-2" {
  description = "SSH port of SW-2 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["SW-2"]
}

output "ssh_port_PC" {
  description = "SSH port of PC (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["PC"]
}

output "ssh_port_Laptop" {
  description = "SSH port of Laptop (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Laptop"]
}

output "ssh_port_Remote-PC" {
  description = "SSH port of Remote-PC (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Remote-PC"]
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
