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
  description = "Legacy alias: SSH port of the first simulated device (R1)."
  value       = 22
}

# One SSH port per simulated device: the base port + its topology id (read from
# topology.yaml, so reordering the devices can't silently break grading). Output
# names are static in Terraform: add one block per simulated device.
output "ssh_port_R1" {
  description = "SSH port of R1 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["R1"]
}

output "ssh_port_R2" {
  description = "SSH port of R2 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["R2"]
}

output "ssh_port_S1" {
  description = "SSH port of S1 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["S1"]
}

output "ssh_port_S2" {
  description = "SSH port of S2 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["S2"]
}

output "ssh_port_ISP-SW" {
  description = "SSH port of ISP-SW (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["ISP-SW"]
}

output "ssh_port_PC-01" {
  description = "SSH port of PC-01 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["PC-01"]
}

output "ssh_port_PC-02" {
  description = "SSH port of PC-02 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["PC-02"]
}

output "ssh_port_PC-A" {
  description = "SSH port of PC-A (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["PC-A"]
}

output "ssh_port_PC-B" {
  description = "SSH port of PC-B (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["PC-B"]
}

output "ssh_port_Web" {
  description = "SSH port of Web (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Web"]
}

output "ssh_port_DNS1" {
  description = "SSH port of DNS1 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["DNS1"]
}

output "ssh_port_DNS2" {
  description = "SSH port of DNS2 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["DNS2"]
}

output "URL" {
  description = "Student web canvas (topology + in-page device console) — the platform edge proxies this to the learner."
  value       = "http://${docker_container.lab.name}:7681/"
}
