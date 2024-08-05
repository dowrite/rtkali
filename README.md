# rtkali
RT Kali gives you a Kali Rolling VM with these additional customizations:

### Additional FOSS tools
  - VS Code
  - xxd
  - feroxbuster
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
### 4. Troubleshoot VM Provisioning
The first time `vagrant up` is run, the VM is created and `vagrant provision` is automatically run. However, this step is most problematic since we're installing many tools. 
  - If provisioning fails/stalls
    - Reboot the VM and run `vagrant provision` to re-provision the VM
  - If errors continue, force a new download of the `kalilinux/rolling` box:
    ```
    vagrant box remove kalilinux/rolling
    vagrant up
    ``` 
### 5. Run setup script in RTKali VM
  - Login to rtkali (default creds: vagrant/vagrant)
  - Launch Terminal
  - Follow on-screen prompts
