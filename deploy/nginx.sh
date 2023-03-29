sudo apt update
sudo apt install nginx
sudo cp deploy/nginx.conf /etc/nginx/nginx.conf
systemctl start nginx
systemctl enable nginx
systemctl status nginx