#!/usr/bin/env bash

if [ -n "`which apt-get`" ]; 
then COMMAND="apt-get" ; 
elif [ -n "`which yum`" ]; 
then COMMAND="yum" ; 
fi 

sudo COMMAND -y install wget

if [ "yum" == "`$COMMAND`" ];
	then sudo yum groupinstall -y "Development Tools";
	`sudo yum -y install epel-release`;
fi

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

if [ "" == "`find get-pip.py`"]; then
	`cd Python-2.7.11/Tools/scripts`;
	`wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py`;
	fi

sudo python -m  pip -U  install selenium;
wget https://github.com/mozilla/geckodriver/releases/download/v0.18.0/geckodriver-v0.18.0-linux64.tar.gz;
echo "--------------------------------------------------------"
echo "Almost there!"
echo "Unzip geckodriver* using gzip -d or tar -xzvf";
echo "Then chmod +x geckodriver";
