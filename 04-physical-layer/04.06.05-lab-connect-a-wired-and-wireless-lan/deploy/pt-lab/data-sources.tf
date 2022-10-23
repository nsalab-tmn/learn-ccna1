data "vkcs_compute_keypair" "kp" {
  name = "PT-tjBrRMum"
}

data "vkcs_compute_flavor" "flavor" {
  name = "Standard-2-4-40"
}

data "vkcs_networking_network" "extnet" {
  name = "ext-net"
}

data "vkcs_images_image" "ubuntu" {
  name        = "learn-pt-lab"
  most_recent = true

  properties = {
    key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCqLyGIy8DX6FtxUSbf2NAgR0omAMg9LSiVeha7sjCkfGPlasN249ThlGHaoFxTICR/9WYCbeHQ7ag3PM0hP74gKTHnR8HUA7+7Xs8ZYnCMmMHKQUkgRQDLmTkipmWkty5xKpmHyAA61hej8DE+O8DjqACUtyMRLVsKTQmIUtu6UWUZBGzfRfS39pGKTkJLkgser9Epa780ueN3aDHaJYghNyilMS63HYmgih7HEEtdWyfPScO0/y7fJnUrxvKufYOULzMGzc4s7acZBvLDNhGllj/vhswpZC9YEicrlNndubpiVwh/6Q9KXMqqFBpPheVRjxHatFulhtVSr/USkSGz Generated-by-Nova"
  }
}