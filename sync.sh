# Update / sync with github + mega.nz
rm -rf "Build"
mkdir "Build"
megadl --path "Build" https://mega.nz/folder/CnwDwBjI#SF0jby2EEahtnFUuaMESCQ
source stop.sh
git pull origin main
source start.sh