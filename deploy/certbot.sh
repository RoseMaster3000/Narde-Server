sudo apt update
sudo apt install certbot
sudo apt install python3-certbot-nginx
sudo certbot --nginx -d florasoft.live -d shahrose.com
# sudo systemctl status certbot.timer  # Check renewal timer
# certbot renew --dry-run              # Test auto-renewal CRON job