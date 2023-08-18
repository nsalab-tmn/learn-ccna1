#cloud-config
chpasswd:
  list: |
    root:${admin_pass}
    sysadmin:${student_pass}
  expire: false
hostname: ${hostname}
runcmd:
- wget -O - https://learncertstore.blob.core.windows.net/supercert/supercert.pem > /home/sysadmin/.vnc/supercert.pem
- wget -O - https://learncertstore.blob.core.windows.net/supercert/supercert.key > /home/sysadmin/.vnc/supercert.key
- wget -O - https://kvmstore.blob.core.windows.net/images/17.8.3-lab.pka > /opt/nsalab/lab/lab.pka
- systemctl start vncserver@1
- iptables -A OUTPUT -p tcp -m tcp -o eth0 --sport 443 -j ACCEPT
- iptables -A OUTPUT -p tcp -m tcp -o eth0 --sport 80 -j ACCEPT
- iptables -A OUTPUT -p tcp -m tcp -o eth0 --sport 22 -j ACCEPT
- iptables -A OUTPUT -p tcp -m tcp -o eth0 --sport 8080 -j ACCEPT
- iptables -A OUTPUT -d 169.254.169.254 -j ACCEPT
- iptables -A OUTPUT -o eth0 -j DROP
- iptables-save > /etc/iptables/rules.v4