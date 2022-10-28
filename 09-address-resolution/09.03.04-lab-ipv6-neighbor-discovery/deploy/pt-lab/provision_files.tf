resource "null_resource" "lab" {
    connection {
      type     = "ssh"
      user     = "root"
      password = var.root_password
      host     = vkcs_compute_instance.compute[0].access_ip_v4

    }
    provisioner "remote-exec" {
      inline = [
        "#!/bin/bash",
        "mkdir -p /opt/nsalab/lab"
      ]
    }
    provisioner "file" {
      source      = "${path.module}/9.3.4-lab.pka"
      destination = "/opt/nsalab/lab/lab.pka"
    }

    depends_on = [
      vkcs_compute_instance.compute
    ]
}

resource "null_resource" "certs" {
    connection {
      type     = "ssh"
      user     = "root"
      password = var.root_password
      host     = vkcs_compute_instance.compute[0].access_ip_v4

    }
    provisioner "file" {
      source      = "${path.module}/supercert.pem"
      destination = "/home/sysadmin/.vnc/supercert.pem"
    }
    provisioner "file" {
      source      = "${path.module}/supercert.key"
      destination = "/home/sysadmin/.vnc/supercert.key"
    }
    depends_on = [
      null_resource.lab
    ]
}

