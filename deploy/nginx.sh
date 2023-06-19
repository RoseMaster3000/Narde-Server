sudo apt update
sudo apt install nginx
sudo cp deploy/nginx.conf /etc/nginx/nginx.conf
sudo systemctl daemon-reload
systemctl start nginx
systemctl enable nginx
systemctl status nginx