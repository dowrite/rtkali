# rtkali
VagrantFile and supporting resources for customizing Offensive Security's kali-rolling box

# Customizations
Once Vagrant provisioning completes and all manual steps are completed as prompted, the following customizations are in place.

### Install FOSS tools:
  - VS Code
  - Ghidra
  - Caldera
  - CyberChef
  
### Install & activate the following licensed SW (if license key file is found on Vagrant host):
  - BurpSuite
  - Cobalt Strike
  
### Configure terminal logging
  - Update terminal prompt to include hostname, IP, date
  - Log all terminal input by default
  
### Hardening
All Vagrant boxes must have a vagrant account and SSH for Vagrant to work. Once we are done provisioning with Vagrant, the op-setup.sh script will harden the VM by doing the following:
  - Remove Vagrant account
  - Disable sshd

# USAGE
### 1. Download & Install Vagrant
https://developer.hashicorp.com/vagrant/downloads/vmware

### 2. Download & Install Vagrant VMWare Utility
https://developer.hashicorp.com/vagrant/downloads/vmware

### 3. Clone this repo
  - Open VS Code
  - Click "Clone Repository"
  - Enter "https://github.com/dowrite/rtkali.git"

### 4. Create VM
  - `cd rtkali`
  - `vagrant up`
