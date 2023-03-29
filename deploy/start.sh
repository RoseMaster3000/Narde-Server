# Services Start 
sudo systemctl daemon-reload
sudo systemctl start narde
sudo systemctl start nginx
# Service Status Report
echo -e "\033[4mGunicorn:\033[0m"
systemctl status narde | grep "Active:"
echo -e "\033[4mNginx:\033[0m"
systemctl status nginx | grep "Active:"
# IP Address Report
echo -e "\033[4mExternal IP:\033[0m";
curl -s "https://api.ipify.org/?format=txt" | awk '{printf "    %s\n", $0}'
echo -e "\033[4mInternal IP:\033[0m";
ip a | awk 'function outline() {if (link>"") {printf "    %s\n", inets}} $0 ~ /^[1-9]/ {outline();  inets=""; link=""} $1 == "link/ether" {link=$2} $1 == "inet" {inet=substr($2, 1, index($2,"/")-1); if (inets>"") inets=inets ","; inets=inets inet} END {outline()}'
