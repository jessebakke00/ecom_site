#!/bin/bash


function site_setup {
sudo python2 assets/Django/setup.py install

. assets/Komodo-Edit/install.sh && sudo ln -s "/home/kali/Komod-Edit/bin/komodo" /usr/local/bin/komodo
}

function git_setup {

git config --global user.email "jesse.bakke.00@gmail.com"

git config --global user.name "jessebakke00"
}

#site_setup
#git_setup

