rm -rf "Build"
mkdir "Build"
megadl --path "Build" https://mega.nz/folder/aypBRY6A#Zir3-GcI0V0AtQBZwovYPg
source stop.sh
git pull origin main
source start.sh