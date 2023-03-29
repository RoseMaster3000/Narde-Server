sudo apt-get update
sudo apt-get install ufw
sudo ufw default allow outgoing
sudo ufw default deny incoming
sudo ufw allow 'Nginx HTTPS'          # HTTPS/HTTP/Full
# ufw allow 27015:27017          # MongoDB
# ufw allow 25,587,465,2525/tcp  # EMAIL
sudo ufw enable
sudo ufw status