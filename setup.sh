#!/usr/bin/env bash

if [ -f /etc/os-release ]; then
    # freedesktop.org and systemd
    . /etc/os-release
    OS=$NAME
elif type lsb_release >/dev/null 2>&1; then
    # linuxbase.org
    OS=$(lsb_release -si)
elif [ -f /etc/lsb-release ]; then
    # For some versions of Debian/Ubuntu without lsb_release command
    . /etc/lsb-release
    OS=$DISTRIB_ID
elif [ -f /etc/debian_version ]; then
    # Older Debian/Ubuntu/etc.
    OS=Debian
elif [ -f /etc/SuSe-release ]; then
    # Older SuSE/etc.
    ...
elif [ -f /etc/redhat-release ]; then
    # Older Red Hat, CentOS, etc.
    ...
else
    # Fall back to uname, e.g. "Linux <version>", also works for BSD, etc.
    OS=$(uname -s)
fi

CentOSSetup ()
{ # This script sets up Chug-A-Lug on Ubuntu
sudo yum -y install wget python-pip tkinter tcl-devel tk-devel epel-release
sudo yum -y groupinstall -y "Development Tools"
if [ "" == "`which python2`" ];
        then wget --no-check-certificate https://www.python.org/ftp/python/2.7.11/Python-2.7.11.tgz;
        `tar -xzf Python-2.7.11.tg`;
        `cd Python-2.7.11`;
        `./configure`;
        `make`;
        `sudo make install`;
        `export PATH=$PATH:/root/python-2.7.11`;
        `cd ..`;
        fi
sudo pip install selenium
wget https://github.com/mozilla/geckodriver/releases/download/v0.18.0/geckodriver-v0.18.0-linux64.tar.gz
tar -xvzf geckodriver*
chmod +x geckodriver
sudo mv geckodriver /usr/local/bin/
rm geckodriver-v0.16.1-linux64.tar.gz
}

case $OS in
	"CentOS Linux")
		CentOSSetup
	;;
	Ubuntu)
		echo "Hi!"
	;;
esac
