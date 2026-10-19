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
  description = "Legacy alias: SSH port of the first simulated device (MultiServer)."
  value       = 22
}

# One SSH port per simulated device: the base port + its topology id (read from
# topology.yaml, so reordering the devices can't silently break grading). Output
# names are static in Terraform: add one block per simulated device.
output "ssh_port_MultiServer" {
  description = "SSH port of MultiServer (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["MultiServer"]
}

output "ssh_port_Switch" {
  description = "SSH port of Switch (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Switch"]
}

output "ssh_port_HTTP-Client" {
  description = "SSH port of HTTP-Client (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["HTTP-Client"]
}

output "ssh_port_FTP-Client" {
  description = "SSH port of FTP-Client (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["FTP-Client"]
}

output "ssh_port_E-Mail-Client" {
  description = "SSH port of E-Mail-Client (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["E-Mail-Client"]
}

output "ssh_port_DNS-Client" {
  description = "SSH port of DNS-Client (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["DNS-Client"]
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
