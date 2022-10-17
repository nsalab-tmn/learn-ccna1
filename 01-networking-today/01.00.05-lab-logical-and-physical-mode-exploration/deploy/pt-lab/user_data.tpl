#cloud-config
chpasswd:
  list: |
    root:${admin_pass}
    sysadmin:${student_pass}
  expire: false
hostname: ${hostname}
runcmd:
- chmod +x /opt/nsalab/lab/restart.sh
- bash /opt/nsalab/lab/restart.sh