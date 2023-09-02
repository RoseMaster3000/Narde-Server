# Update / sync with github + mega.nz
# rm -rf "Build"
# mkdir "Build"
# megadl --path "Build" https://mega.nz/folder/SvQzWTDQ#dnK-FyLH-0hqrz7BUvY4Sg

source deploy/stop.sh
git pull origin main
source deploy/start.sh