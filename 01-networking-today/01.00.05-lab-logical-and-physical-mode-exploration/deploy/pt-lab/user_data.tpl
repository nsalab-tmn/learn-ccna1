#cloud-config
chpasswd:
  list: |
    root:${admin_pass}
    sysadmin:${student_pass}
  expire: false
hostname: ${hostname}