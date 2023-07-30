# First time setup

# https://github.com/settings/tokens
# git clone https://github.com/RoseMaster3000/Narde-Server.git

sudo apt install megatools
python3.9 -m venv virt
source virt/bin/activate
pip install -r requirements.txt

rm -rf "Build"
mkdir "Build"
megadl --path "Build" https://mega.nz/folder/CnwDwBjI#SF0jby2EEahtnFUuaMESCQ