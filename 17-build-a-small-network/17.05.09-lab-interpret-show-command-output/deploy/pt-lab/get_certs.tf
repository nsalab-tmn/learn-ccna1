resource "null_resource" "get_certs" {
  provisioner "local-exec" {
    command = "bash ${path.module}/get_certs.sh"
    environment = {
      LOCAL_PATH = path.module
    }
    when = create
  }
}
