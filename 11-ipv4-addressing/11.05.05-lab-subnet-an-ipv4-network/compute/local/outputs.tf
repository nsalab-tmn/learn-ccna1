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
  description = "Legacy alias: SSH port of the first simulated device (CustomerRouter)."
  value       = 22
}

# One SSH port per simulated device: the base port + its topology id (read from
# topology.yaml, so reordering the devices can't silently break grading). Output
# names are static in Terraform: add one block per simulated device.
output "ssh_port_CustomerRouter" {
  description = "SSH port of CustomerRouter (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["CustomerRouter"]
}

output "ssh_port_LAN-A" {
  description = "SSH port of LAN-A (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["LAN-A"]
}

output "ssh_port_LAN-B" {
  description = "SSH port of LAN-B (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["LAN-B"]
}

output "ssh_port_PC-A" {
  description = "SSH port of PC-A (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["PC-A"]
}

output "ssh_port_PC-B" {
  description = "SSH port of PC-B (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["PC-B"]
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
