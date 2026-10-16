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
  description = "Legacy alias: SSH port of the first simulated device (Building1)."
  value       = 22
}

# One SSH port per simulated device: the base port + its topology id (read from
# topology.yaml, so reordering the devices can't silently break grading). Output
# names are static in Terraform: add one block per simulated device.
output "ssh_port_Building1" {
  description = "SSH port of Building1 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Building1"]
}

output "ssh_port_Building2" {
  description = "SSH port of Building2 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Building2"]
}

output "ssh_port_ASW-1" {
  description = "SSH port of ASW-1 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["ASW-1"]
}

output "ssh_port_ASW-2" {
  description = "SSH port of ASW-2 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["ASW-2"]
}

output "ssh_port_ASW-3" {
  description = "SSH port of ASW-3 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["ASW-3"]
}

output "ssh_port_ASW-4" {
  description = "SSH port of ASW-4 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["ASW-4"]
}

output "ssh_port_Host-A" {
  description = "SSH port of Host-A's command prompt (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Host-A"]
}

output "ssh_port_Host-B" {
  description = "SSH port of Host-B's command prompt (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Host-B"]
}

output "ssh_port_Host-C" {
  description = "SSH port of Host-C's command prompt (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Host-C"]
}

output "ssh_port_Host-D" {
  description = "SSH port of Host-D's command prompt (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Host-D"]
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
