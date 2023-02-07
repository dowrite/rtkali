# rtkali
VagrantFile and supporting resources for customizing Offensive Security's kali-rolling box

# Customizations
Once Vagrant provisioning completes and all manual steps are completed as prompted, the following customizations are in place.

## Install FOSS tools:
  - VS Code
  - Ghidra
  - Caldera
  - CyberChef
  
## Install & activate the following licensed SW (if license key file is found on Vagrant host):
  - BurpSuite
  - Cobalt Strike
  
## Configure terminal logging
  - Update terminal prompt to include hostname, IP, date
  - Log all terminal input by default
  
## Hardening
All Vagrant boxes must have a vagrant account and SSH for Vagrant to work. Once we are done provisioning with Vagrant, the op-setup.sh script will harden the VM by doing the following:
  - Remove Vagrant account
  - Disable sshd
