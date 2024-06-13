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

For `shipwright` on AZL2:
```bash
# Set some variables so you can just copy-paste the rest of the code.
# Use whatever you want for these, of course.
pev_dir=~/pev-env
repo_root=~/datadrive/code/mariner/azl-az-cli-extensions

# For Reasons, this requires a python virtual environment. Assume you want the VE stuff here:
python3 -m venv "${pev_dir}"
. "${pev_dir}/bin/activate"
pip3 install azdev

# Change to the repo directory; this is where it is on my machine.
cd "${repo_root}"
azdev setup -r $(realpath "${repo_root}") -e shipwright

# You can now run the extension.
az shipwright --help
```
