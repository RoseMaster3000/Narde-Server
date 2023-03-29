sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d florasoft.live -d shahrose.com
# sudo systemctl status certbot.timer  # Check renewal timer
# certbot renew --dry-run              # Test auto-renewal CRON job