# rtkali
RT Kali gives you a Kali Rolling VM with these additional customizations:

### Additional FOSS tools
  - VS Code
  - xxd
  - [Ghidra](https://github.com/NationalSecurityAgency/ghidra)
  - OT testing tools: mbtget, pymodbus, Redpoint
  - certmitm
  - Zeek
  - Caldera
  - Windows specific tools: Sharpshooter, Bloodhound
  - CyberChef
  
### Installed & activated SW (if license key file is found on Vagrant host):
  - BurpSuite
  - Cobalt Strike
  
### Terminal logging
  - Updates terminal prompt to include hostname, IP, date
  - Log all terminal input by default
  
### Hardening
All Vagrant boxes must have a vagrant account and SSH for Vagrant to work. Once we are done provisioning with Vagrant, the op-setup.sh script will harden the VM by doing the following:
  - Removes Vagrant account
  - Disables sshd

# INSTALLATION
### PREREQUISITES
The following SW must be installed on the host machine before following the installation steps: 
  - [Vagrant](https://developer.hashicorp.com/vagrant/downloads)
  - VMWare Workstation Pro or [VMWare Workstation Player](https://www.vmware.com/content/vmware/vmware-published-sites/us/products/workstation-player.html)
  - [VS Code](https://code.visualstudio.com/download)

### 1. Install Vagrant VMWare Utility
  - Download & Install the driver: https://developer.hashicorp.com/vagrant/downloads/vmware
  - Install the vagrant plugin `vagrant plugin install vagrant-vmware-desktop`

### 2. Clone this repo
  - Open VS Code
  - Click "Clone Repository"
  - Enter "https://github.com/dowrite/rtkali.git"

### 3. Create VM
  - Open Terminal in VS Code. Type the following commands in VS Code's terminal.
    ```
    cd rtkali
    vagrant up
    ```
    - If `vagrant up` fails at any point after creating the VM, run `vagrant provision` to re-provision the VM.

### 4. Run setup script in RTKali VM
  - Login to rtkali (default creds: vagrant/vagrant)
  - Launch Terminal
  - Follow on-screen prompts
