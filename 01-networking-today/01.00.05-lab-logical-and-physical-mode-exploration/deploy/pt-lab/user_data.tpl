#cloud-config
chpasswd:
  list: |
    root:${admin_pass}
    sysadmin:${student_pass}
  expire: false
hostname: ${hostname}
runcmd:
- service nginx restart
- systemctl restart vncserver@1.service
- systemctl restart pt.service