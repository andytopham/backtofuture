#!/bin/sh
echo "** Installing fileset needed for Back to the Future display system. **"
# first, check user is root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi
echo "Future display installer"
echo
echo "apt-get update"
apt-get update
echo
echo "apt-get -y upgrade"
apt-get -y upgrade
echo
echo "apt-get -y install python-pip"
apt-get -y install python-pip
echo
echo "pip install beautifulsoup4"
pip install beautifulsoup4
echo
echo "pip install requests"
pip install requests
echo
echo "pip install python-mpd2"
pip install python-mpd2
echo
echo "pip install logging"
pip install logging
echo
echo "apt-get -y install python-serial"
apt-get -y install python-serial
echo
echo "install feedparser"
pip install feedparser
pip install urllib3
echo
echo "apt-get -y install mpd mpc"	
apt-get -y install mpd mpc	
mkdir log
echo "Starting autostart of future.py"
cp fstartup.sh /etc/init.d
chmod 755 /etc/init.d/fstartup.sh
update-rc.d fstartup.sh defaults
echo "main.py must be executable for autostart."
chmod +x main.py
echo
