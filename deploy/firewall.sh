sudo apt update
sudo apt install ufw
ufw default allow outgoing
ufw default deny incoming
ufw allow 'Nginx HTTPS'          # HTTPS/HTTP/Full
# ufw allow 27015:27017          # MongoDB
# ufw allow 25,587,465,2525/tcp  # EMAIL
ufw enable
ufw status