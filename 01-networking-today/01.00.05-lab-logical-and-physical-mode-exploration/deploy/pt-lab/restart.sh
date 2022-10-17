#!/bin/bash
systemctl restart nginx
systemctl restart vncserver@1.service
systemctl restart pt.service
systemctl restart pt-api.service