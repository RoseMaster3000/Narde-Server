sudo cp deploy/narde.service /etc/systemd/system/narde.service
sudo systemctl start narde
sudo systemctl enable narde
sudo systemctl status narde