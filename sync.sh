# Update / sync with github + mega.nz
rm -rf "Build"
mkdir "Build"
megadl --path "Build" https://mega.nz/folder/CnwDwBjI#SF0jby2EEahtnFUuaMESCQ
source deploy/stop.sh
git pull origin main
source deploy/start.sh