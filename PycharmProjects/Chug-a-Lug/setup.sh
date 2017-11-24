#!/usr/bin/env bash

wget --no-check-certificate https://www.python.org/ftp/python/2.7.11/Python-2.7.11.tgz
tar -xzf Python-2.7.11.tgz
cd Python-2.7.11
./configure
make 
sudo make install
export PATH=$PATH:/root/python-2.7.11
