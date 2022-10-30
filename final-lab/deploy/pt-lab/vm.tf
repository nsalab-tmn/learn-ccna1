resource "vkcs_compute_instance" "compute" {
  name              = "vm-${random_string.learn.result}"
  count             = 1  // Требуется указать кол-во ВМ
  flavor_id         = data.vkcs_compute_flavor.flavor.id
  security_groups   = ["permit_all_${random_string.learn.result}"]
  image_id          = data.vkcs_images_image.ubuntu.id
  key_pair          = data.vkcs_compute_keypair.kp.id
  availability_zone = "MS1"
  user_data         = base64encode(templatefile("${path.module}/user_data.tpl", {
          admin_pass    = var.root_password,
          student_pass  = random_string.learn.result,
          hostname      = "vm-${random_string.learn.result}"
        }
      )
    )
  config_drive = true

  connection {
    type     = "ssh"
    user     = "root"
    password = var.root_password
    host     = vkcs_compute_instance.compute[0].access_ip_v4

  }

  block_device {
    uuid                  = data.vkcs_images_image.ubuntu.id
    source_type           = "image"
    destination_type      = "volume"
    volume_type           = "ceph-ssd"
    volume_size           = 10
    boot_index            = 0
    delete_on_termination = true
  }

  network {
    uuid = data.vkcs_networking_network.extnet.id
  }

  depends_on = [ vkcs_networking_secgroup.secgroup, null_resource.get_certs ]
}