#!/usr/bin/env bash
#
# Provisions an Ubuntu 18.04 Vagrant box for SERVER development. This script
# handles upgrading the box as root before moving along.
#
set -e

echo "********** Upgrade and reboot Ubuntu."

# Set apt-get to non-interactive. Still need to pass in -y.
export DEBIAN_FRONTEND=noninteractive

apt-get update
apt-get dist-upgrade -y
apt-get autoremove -y

snap refresh
