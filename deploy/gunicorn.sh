sudo cp deploy/narde.service /etc/systemd/system/narde.service
systemctl start narde
systemctl enable narde
systemctl status narde