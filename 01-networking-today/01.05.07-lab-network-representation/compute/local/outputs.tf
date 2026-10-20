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
  description = "Legacy alias: SSH port of the first simulated device (R4)."
  value       = 22
}

# One SSH port per simulated device: the base port + its topology id (read from
# topology.yaml, so reordering the devices can't silently break grading). Output
# names are static in Terraform: add one block per simulated device.
output "ssh_port_R4" {
  description = "SSH port of R4 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["R4"]
}

output "ssh_port_S4" {
  description = "SSH port of S4 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["S4"]
}

output "ssh_port_BranchServer" {
  description = "SSH port of BranchServer (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["BranchServer"]
}

output "ssh_port_Sales" {
  description = "SSH port of Sales (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Sales"]
}

output "ssh_port_Accounting" {
  description = "SSH port of Accounting (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Accounting"]
}

output "ssh_port_Guest" {
  description = "SSH port of Guest (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Guest"]
}

output "ssh_port_Wireless-AP" {
  description = "SSH port of Wireless-AP (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Wireless-AP"]
}

output "ssh_port_Smart-Phone" {
  description = "SSH port of Smart-Phone (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Smart-Phone"]
}

output "ssh_port_R2" {
  description = "SSH port of R2 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["R2"]
}

output "ssh_port_D1" {
  description = "SSH port of D1 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["D1"]
}

output "ssh_port_D2" {
  description = "SSH port of D2 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["D2"]
}

output "ssh_port_S1" {
  description = "SSH port of S1 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["S1"]
}

output "ssh_port_S2" {
  description = "SSH port of S2 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["S2"]
}

output "ssh_port_S3" {
  description = "SSH port of S3 (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["S3"]
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

output "ssh_port_CentralServer" {
  description = "SSH port of CentralServer (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["CentralServer"]
}

output "ssh_port_ISP-Tier3a" {
  description = "SSH port of ISP-Tier3a (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["ISP-Tier3a"]
}

output "ssh_port_ISP-Tier3b" {
  description = "SSH port of ISP-Tier3b (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["ISP-Tier3b"]
}

output "ssh_port_famous-dns" {
  description = "SSH port of famous-dns (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["famous-dns"]
}

output "ssh_port_netacad" {
  description = "SSH port of netacad (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["netacad"]
}

output "ssh_port_WRS" {
  description = "SSH port of WRS (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["WRS"]
}

output "ssh_port_HomeDesktop" {
  description = "SSH port of HomeDesktop (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["HomeDesktop"]
}

output "ssh_port_Home-Laptop" {
  description = "SSH port of Home-Laptop (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Home-Laptop"]
}

output "ssh_port_Tablet" {
  description = "SSH port of Tablet (ssh_base_port + its topology id)."
  value       = local.ssh_base_port + local.device_ids["Tablet"]
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
