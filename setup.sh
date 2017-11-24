#!/usr/bin/env bash

if [ -n "`which apt-get`" ]; 
then COMMAND="apt-get" ; 
elif [ -n "`which yum`" ]; 
then COMMAND="yum" ; 
fi 

sudo COMMAND -y install wget

if [ "yum" == "`$COMMAND`" ];
	then `sudo yum install -y "Development Tools"`;
	`sudo yum -y install epel-release`;
fi

$COMMAND -y groupinstall "Development Tools"

if [ "" == "`which python2`"];then 
	`wget --no-check-certificate https://www.python.org/ftp/python/2.7.11/Python-2.7.11.tgz`;
	`tar -xzf Python-2.7.11.tg`;
	`cd Python-2.7.11`;
	`./configure`;
	`make`;
	`sudo make install`;
	`export PATH=$PATH:/root/python-2.7.11`;
	fi

sudo $COMMAND -y install python-pip
sudo pip install selenium
