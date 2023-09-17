#!/usr/bin/env bash
#
# Provisions an Ubuntu 18.04 Vagrant box for SERVER development. This script
# handles cleaning up the provisioning as root.
#
set -e

echo "********** Cleanup and reboot Ubuntu."

# Set apt-get to non-interactive. Still need to pass in -y.
export DEBIAN_FRONTEND=noninteractive

apt-get autoremove -y
reboot

# FIN
