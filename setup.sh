#!/usr/bin/env bash

if [ "" == "`which wget`" ]; 
then echo "wget Not Found"; 
if [ -n "`which apt-get`" ]; 
then COMMAND="apt-get" ; 
elif [ -n "`which yum`" ]; 
then COMMAND="yum" ; 
fi ; 
fi

$COMMAND -y install wget
$COMMAND -y groupinstall "Development Tools"
wget --no-check-certificate https://www.python.org/ftp/python/2.7.11/Python-2.7.11.tgz
tar -xzf Python-2.7.11.tgz
cd Python-2.7.11
./configure
make 
sudo make install
export PATH=$PATH:/root/python-2.7.11
