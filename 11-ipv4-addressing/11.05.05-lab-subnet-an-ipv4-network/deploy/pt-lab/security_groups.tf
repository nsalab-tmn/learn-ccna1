resource "vkcs_networking_secgroup" "secgroup" {
  name        = "permit_all_${random_string.learn.result}"
  description = "Permit all traffic"
}

resource "vkcs_networking_secgroup_rule" "secgroup_in" {
  direction         = "ingress"
  ethertype         = "IPv4"
  security_group_id = "${vkcs_networking_secgroup.secgroup.id}"
  
  depends_on = [
    vkcs_networking_secgroup.secgroup
  ]  
}