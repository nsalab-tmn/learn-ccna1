resource "null_resource" "services" {
  connection {
      type     = "ssh"
      user     = "root"
      password = var.root_password
      host     = vkcs_compute_instance.compute[0].access_ip_v4

  }
  provisioner "remote-exec" {
    inline = [
      "#!/bin/bash",
      "systemctl start vncserver@1"
    ]
  }
  depends_on = [
    null_resource.certs
  ]
}