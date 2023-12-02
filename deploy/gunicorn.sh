# apt install python3-gunicorn
sudo cp deploy/narde.service /etc/systemd/system/narde.service
sudo systemctl daemon-reload
sudo systemctl start narde
sudo systemctl enable narde
sudo systemctl status narde