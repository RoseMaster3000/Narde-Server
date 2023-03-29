sudo apt update
sudo apt install certbot
sudo apt install certbot-nginx
certbot --nginx -d florasoft.live -d shahrose.com
# certbot renew --dry-run   # Test auto-renewal CRON job