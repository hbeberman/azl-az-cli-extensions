# az-cli-extensions
This repository contains azure-cli extensions developed by the Azure Linux team

Rough development setup example:
``` bash
mkdir -p ~/projects
sudo apt install -y python3.10-venv
python3 -m venv ~/projects/pydev
source ~/projects/pydev/bin/activate
pip3 install azdev
azdev setup -r ~/repos/azl-az-cli-extensions/ -e my-extension
```