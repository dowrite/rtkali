#!/bin/bash

##### Op-setup.sh #####

if [ "$EUID" -ne 0 ] 
then 
	echo "Please run as root"
	exit
fi

read -p "This script will change the hostname and disable Vagrant support. Are you ready? (N/y): " prompt
if [[ ! "$prompt" =~ ^([yY][eE][sS]|[yY])$  ]] 
then
	echo "Aborted. No changes made."
	exit
fi

### Harden Kali
echo 
echo "#### Disabling sshd ####"
systemctl disable sshd

### Hostname change
echo
echo "#### Defining Hostname ####"
echo "What is the mission name (defined by team lead)?"
read -p 'Mission name: ' missionname
echo ""
echo "What is your 2-digit laptop number?"
read -p 'Laptop number (##): ' laptopnumber
newhostname="$missionname-kali$laptopnumber"
echo "$newhostname" > /etc/hostname
hostname -b "$newhostname"
sed -i "s/127.0.1.1.*/127.0.1.1\t$newhostname/g" /etc/hosts

### Change cricket user password
echo ""
echo "### Set password for 'cricket' ###"
passwd cricket

### Configure logging
echo ""
echo "### Configuring terminal logging ###"
mkdir -p /cricket/assessment/termlogs
chown -R root:root /cricket
chmod -R 3777 /cricket # 3777 - Anyone can read/write. Only root can delete.

if test -f "/usr/share/tools/template.zshrc"; then
	cp /usr/share/tools/template.zshrc /root/.zshrc
	cp /usr/share/tools/template.zshrc /home/cricket/.zshrc
else
	echo "/usr/share/tools/template.zshrc not found." 
	echo "Exiting. Op-setup.sh did not complete!"
	exit
fi

echo ""
echo "+------------------------------------------+"
echo "|  MANUAL STEPS - DO NOW                   |"
echo "|                                          |"
echo "|  1. Delete 'vagrant' user                |"
echo "|     sudo userdel -f vagrant              |"
echo "|  2. Power off VM                         |"
echo "|     systemctl poweroff -i                |"
echo "|  3. Remove NAT interface                 |"
echo "|     In VM Settings GUI                   |"
echo "+------------------------------------------+"

# Switch to cricket user since we're going to delete the vagrant user 
su cricket