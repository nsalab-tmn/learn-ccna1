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
  description = "Legacy alias: SSH port of the first simulated device (Building-1)."
  value       = 22
}

# One SSH port per simulated device: the base port + its topology id (read from
# topology.yaml, so reordering the devices can't silently break grading). Output
# names are static in Terraform: add one block per simulated device.
output "ssh_port_Building-1" {
  description = "SSH port of Building-1 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Building-1"]
}

output "ssh_port_First-Floor-Switch" {
  description = "SSH port of First-Floor-Switch (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["First-Floor-Switch"]
}

output "ssh_port_Second-Floor-Switch" {
  description = "SSH port of Second-Floor-Switch (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Second-Floor-Switch"]
}

output "ssh_port_Host-1" {
  description = "SSH port of Host-1 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Host-1"]
}

output "ssh_port_Host-2" {
  description = "SSH port of Host-2 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Host-2"]
}

output "ssh_port_Host-3" {
  description = "SSH port of Host-3 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Host-3"]
}

output "ssh_port_Server" {
  description = "SSH port of Server (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Server"]
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
