# -*- mode: ruby -*-
# vi: set ft=ruby :

# This vagrant file builds the Kali VM and installs all necessary apps.
# Everything that needs internet connection will be done here.
# The op-setup.sh is run inside the VM and can be run without internet.

Vagrant.configure("2") do |config|
  config.vm.box = "kalilinux/rolling"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  config.vm.network "public_network"

  # VMWare-specific configuration  
  config.vm.provider :vmware_desktop do |vmware|
    # Customize the amount of memory on the VM:
    vmware.memory = "8192"
    vmware.vmx['displayname'] = "RTKali"
  end

  # Prep for provisioning
  config.vm.provision "shell", inline: <<-SHELL
    # Set time zone to UTC
    timedatectl set-timezone UTC

    # Setup RT Folders
    mkdir -p /usr/share/tools
    chmod -R 777 /usr/share/tools  # Temporarily open up permissions for provisioning. We change it to 755 later.

    # Create log directory
    mkdir -p /cricket/terminal_logs
    chown -R root:root /cricket
    chmod -R 3777 /cricket # 3777 - Anyone can read/write. Only root can delete.
    
  SHELL

  # Copy tools folder from host to VM. 
  config.vm.provision :file, source: './tools', destination: "/usr/share/tools"

  # Ensure copied files are in unix CRLF format
  config.vm.provision "shell", inline: <<-SHELL
    find /usr/share/tools -type f -name "*" -exec dos2unix {} \\;
  SHELL

  # Update /etc/skel with our template files
  config.vm.provision "shell", inline: <<-SHELL
    cp /usr/share/tools/template.zshrc /etc/skel/.zshrc
    cp /usr/share/tools/template.zshrc /root/.zshrc # Update /root/.zshrc. The root user was already created using the old file in /etc/skel.
  SHELL
  
  # Install apps & deploy file structure
  config.vm.provision "shell", inline: <<-SHELL
    # Create 'cricket' user
    useradd -m -s /bin/zsh cricket
    usermod -aG sudo cricket

    apt update    
    # Install VS Code
    apt install -y curl gpg gnupg2 software-properties-common apt-transport-https 
    curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
    sudo install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/
    echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" | sudo tee /etc/apt/sources.list.d/vscode.list
    apt update
    apt install code

    # Install xxd
    apt install -y xxd

    # Install Ghidra
    apt install -y ghidra

    # Install pymodbus
    apt install -y python3-pymodbus

    # Install mbtget
    git clone https://github.com/sourceperl/mbtget.git /usr/share/tools/mbtget
    cd /usr/share/tools/mbtget && perl Makefile.PL && make && sudo make install

    # Install zeek, zeek tools, ICS Protocol extensions
    apt install -y zeek zeek-dev libpcap-dev cmake zkg
    mkdir -p /usr/share/tools/zeek-aux
    git clone --recursive https://github.com/zeek/zeek-aux.git /usr/share/tools/zeek-aux
    chmod +x -R /usr/share/tools/zeek-aux/configure 
    cd /usr/share/tools/zeek-aux && ./configure && make && sudo make install
    sudo ln -s /usr/local/zeek/bin/zeek-cut /usr/local/bin
    
        
    # Install Caldera into /usr/share/tools
    mkdir -p /usr/share/tools/caldera
    git clone https://github.com/mitre/caldera.git --recursive /usr/share/tools/caldera
    runuser -l cricket -c "pip3 install -r /usr/share/tools/caldera/requirements.txt"
    # Stage atomics for use with Caldera (data only)
    mkdir -p /usr/share/tools/atomic-red-team
    git clone https://github.com/redcanaryco/atomic-red-team.git /usr/share/tools/atomic-red-team
    
    # Install Sharpshooter
    git clone https://github.com/mdsecactivebreach/SharpShooter.git /usr/share/tools/SharpShooter
    runuser -l cricket -c "pip3 install -r /usr/share/tools/SharpShooter/requirements.txt"

    # Install pyenv
    sudo apt install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python3-openssl git
    curl https://pyenv.run | runuser -l cricket -c bash
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> /home/cricket/.zshrc
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> /home/cricket/.zshrc
    runuser -l cricket -c "pyenv install 2.7.18"

    # TODO 
    # update /usr/share/tools/caldera/conf/local.yml
    # cd /usr/share/tools/caldera; python3 server.py --insecure   # Start Caldera Server with default config (./conf/default.yml)
    # cd /usr/share/tools/caldera; python3 server.py              # Start Caldera Server with custom config (./conf/local.yml)

    # Install CyberChef
    CYBERCHEF_VER=$(curl -si https://github.com/gchq/CyberChef/releases/latest | grep -E "^location:" | grep -Eo "v[0-9]+.[0-9]+.[0-9]+")
    wget -qO "/usr/share/tools/CyberChef_$CYBERCHEF_VER.zip" "https://github.com/gchq/CyberChef/releases/download/$CYBERCHEF_VER/CyberChef_$CYBERCHEF_VER.zip"
    unzip "/usr/share/tools/CyberChef_$CYBERCHEF_VER.zip" -d "/usr/share/tools/CyberChef"
    echo '<meta http-equiv="refresh" content="0;url=file:///usr/share/tools/CyberChef/CyberChef_$CYBERCHEF_VER.html" />' >> /home/cricket/Desktop/CyberChef.html

    # Download privesc helper scripts from github
    wget -qO "/usr/share/tools/linpeas.sh" https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh
    wget -qO "/usr/share/tools/winPEAS.bat" https://github.com/carlospolop/PEASS-ng/releases/latest/download/winPEAS.bat

    # Get the latest RT Arsenal notes
    mkdir -p "/home/cricket/Desktop"
    wget -qO "/home/cricket/Desktop/RTArsenal.html" "https://rtarsenal.tiddlyhost.com/"

  SHELL

  # Install Burpsuite Pro - IF license exists on the host.
  # Since we only have 1 user license, only the designated user will have the burp folder on his host machine.
  if File.exists?("./tools/licensed/burp/prefs.xml")
    config.vm.provision "shell", inline: <<-SHELL
  
    # Download Burpsuite Pro
    # Get latest version
    BURP_VER=$(curl -si https://portswigger.net/burp/releases/professional/latest | grep -E "^location:" | grep -Eo "[0-9]+.[0-9]+.[0-9]+" | sed 's/-/./g')

    # Sample Download Header: GET https://portswigger.net/burp/releases/startdownload?product=pro&version=2022.12.5&type=Linux
    wget -qO "/usr/share/tools/burpsuite_pro_v$BURP_VER_install.sh" "https://portswigger.net/burp/releases/startdownload?product=pro&version=$BURP_VER&type=Linux"
    chmod +x "/usr/share/tools/burpsuite_pro_v$BURP_VER_install.sh"
    runuser -l cricket -c "/usr/share/tools/burpsuite_pro_v$BURP_VER_install.sh -q"

    # Activate BurpSuite Pro
    # See https://burpsuite.guide/blog/activate-burpsuite-inside-docker-container/
    cp "/usr/share/tools/licensed/burp/prefs.xml" "/home/cricket/.java/.userPrefs/burp"
    cp "/home/cricket/BurpSuitePro/Burp Suite Professional.desktop" "/home/cricket/Desktop"

    SHELL
  end

  # Install Cobalt Strike - IF license exists on the host.
  # Since we only have 1 user license, only the designated user will have the cobaltstrike folder on his host machine.
  if File.exists?("./tools/licensed/cobaltstrike/license.txt")
    config.vm.provision "shell", inline: <<-SHELL
  
    # Install dependencies
    apt install -y openjdk-11-jdk
    update-java-alternatives -s java-1.11.0-openjdk-amd64

    # Update
    # /usr/share/tools/licensed/cobaltstrike contains a licensed version of CS. We just need to update it. 
    # Update will fail if the license is expired. 
    #   To update license, overwrite the existing license key with new key in ./tools/licensed/cobaltstrike/license.txt on the host.
    cd /usr/share/tools/licensed/cobaltstrike; echo $(cat license.txt) | /bin/bash update

    SHELL
  end

  # Setup operator user environment and finalize permissions
  config.vm.provision "shell", inline: <<-SHELL
    # Set ownership of cricket tools to the cricket account
    chown -R cricket:cricket /usr/share/tools
    chmod -R 755 /usr/share/tools
    chown -R cricket:cricket /home/cricket


    # Add reminder to run op setup script 
    cat <<'EOL' >> /home/vagrant/.zshrc
    # Reminder

    if [ `hostname -s` = 'kali' ]; then
      echo "
    +------------------------------------------+
    |    RUN THE OP SETUP SCRIPT!              |
    |    sudo /usr/share/tools/op-setup.sh     |
    +------------------------------------------+
    "
    fi
EOL
    
  SHELL

  # TODO
  # By default, the Vagrant box has SSH with password disabled. Do we need to change this?

end
