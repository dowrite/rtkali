#!/usr/bin/env python3

import argparse, subprocess, re, logging, os, shutil

# Function to validate the subnet. We need to see if it's a valid one, let's say /8 -> /31
def validateSubnet(i):
      toCheck = i.split('/')
      # This should split it so toCheck[0] = the IP address, and toCheck[1] is /8 -> /31
      if int(toCheck[1]) < 8 or int(toCheck[1]) > 31:
          print("This script does not support subnetting outisde of a /8 -> /31. Please re-run with subnetting in this range")
          quit()
def validate_ip(i):
        # Regex from https://www.geeksforgeeks.org/python-program-to-validate-an-ip-address/
        regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
        # Input validation, need to verify it's an IP or if it's an IP range. First, check to see if it's an IP (as it should have 3 periods regardless)
        total = i.count('.')
        if total != 3:
            print(i+" is not a valid IP. Please re-run the script with only valid IPs")
            quit()
        # Check to see if we're going to have to validate subnets. iptables supports subnetting, so we don't have to expand
        totalS = i.count('/')
        if totalS == 1:
            validateSubnet(i)
            if not (re.search(regex, i.split('/')[0])):
                print(i + " does not contain a valid IP. Please re-run with a valid IP")
        elif totalS > 0:
            print("You have included too many /'s per ip, " + i + " is invalid. Please re-run with only 1 /, such as 192.168.1.0/24")
            quit()
        else:
            if not (re.search(regex, i)):
                print(i + " is not contain a valid IP. Please re-run with a valid IP")
def block_ip(i):
    # Input validation has passed, we have valid IPs now. Now, to re-iterate through the list and actually implement the iptables rules
    # blocking TCP
    cmd = ['iptables', '-A', 'OUTPUT', '-d', i, '-p', 'tcp', '-j', 'DROP']
    try: 
        proc = subprocess.run(cmd, capture_output=True)
    except subprocess.CalledProcessError as err:
            print("Something went wrong. See the below error from the iptables process.")
            logger.error(f"{err} {err.stderr.decode('utf8')}")
            quit()
    # blocking UDP
    cmd= ['iptables', '-A', 'OUTPUT', '-d', i, '-p', 'udp', '-j', 'DROP']
    try: 
        proc2 = subprocess.run(cmd, capture_output=True)
    except subprocess.CalledProcessError as err:
            print("Something went wrong. See the below error from the iptables process.")
            logger.error(f"{err} {err.stderr.decode('utf8')}")
            quit()
    # blocking ICMP
    cmd= ['iptables', '-A', 'OUTPUT', '-d', i, '-p', 'icmp', '-j', 'DROP']
    try: 
        proc3 = subprocess.run(cmd, capture_output=True)
    except subprocess.CalledProcessError as err:
            print("Something went wrong. See the below error from the iptables process.")
            logger.error(f"{err} {err.stderr.decode('utf8')}")
            quit()
    

if __name__ == "__main__":
    # Parse and process command line args, template provided by https://www.kdnuggets.com/2021/08/python-data-processing-script-template.html
    parser = argparse.ArgumentParser(description='Quick setup of iptables to block outbound traffic as needed. This will NOT flush your iptables beforehand')
    parser.add_argument('-ip', metavar='-ips',  type=str, help='IPs that are being required to block. Provide via IP1,IP2,IP3,IP_range/24. Examples: 192.168.1.1,192.168.1.2,192.168.2.0/24. Do not utilize spaces otherwise the program won\'t recognize it')
    parser.add_argument('-f', metavar='-file', type=str, help ='Flush the iptables entirely. Note that any custom firewall rules you had beforehand will be flushed.')
    # TODO: SEe if iptables is even installed

    # Used later
    logger = logging.getLogger(__name__)

    # Check the arguments
    try:
        args = parser.parse_args()
    except SystemExit:
        quit()

    # Check to see if iptables is installed
    result = shutil.which('iptables')
    if result is None:
         print("iptables is not installed - please install and re-run")
         quit()

    # we need root privileges to manipulate iptables, so lets check
    if os.geteuid() != 0:
        exit("This script needs root or sudo privileges. Please re-run with sudo")
    # Assign command line args to variables
    ips = args.ip
    file = args.f

    # See if we were passed a file
    if(file):
         # Need to open a file
        try:
             file1=open(file, 'r')
        except:
             print("Ran into an issue in opening "+file+ ". Please make sure to have provided the full path and that it exists")
        while True:
            line = file1.readline()
            if not line:
                break
            # Validate the IP from the file
            line = line.strip("\n")
            validate_ip(line)
            # If we're here, it's valid. Let's block it now
            block_ip(line)
        
        file1.close()
    else: 
        # Now need to parse the IPs. IPs, regardless of type, should be seperated by commas (unless only one is provided). Split will handle this regardless 
        ips_split = ips.split(',')
        for i in ips_split:
            validate_ip(i)
            # Validated, now block
            block_ip(i)
