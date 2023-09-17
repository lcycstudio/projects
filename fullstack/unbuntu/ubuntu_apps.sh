#!/usr/bin/env bash
#
# Provisions an Ubuntu 18.04 Vagrant box for SERVER development. This script
# handles all the provisioning as root. See the *_user.sh script for
# provisioning as the user.
#

# *****************************************
# Config
# *****************************************

# See the *_user.sh script for languages installed by version managers like
# pyenv. And if a version is not specified here or the *_user.sh script, assume
# one of the scripts installs the latest version available on Ubuntu 18.04,
# preferring LTS's if they exist.
readonly postgresql_major_version="12"
# readonly shellcheck_version="latest"
readonly terraform_version="1.0.7"

# *****************************************
# Update Ubuntu.
# *****************************************
echo "********** Update Ubuntu."

# Set apt-get to non-interactive. Still need to pass in -y.
# export DEBIAN_FRONTEND=noninteractive
apt-get update

# *****************************************
# Install build/install dependencies.
# *****************************************

# There may be some repetition in the install lists. That's ok.

echo "********** Install Docker install dependencies."
# https://docs.docker.com/install/linux/docker-ce/ubuntu/
apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common

echo "********** Install the Python build dependencies."
# https://github.com/pyenv/pyenv/wiki/common-build-problems
apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

echo "********** Install the Python psycopg2 (PostgreSQL ORM) build dependencies."
# https://www.psycopg.org/docs/install.html
apt-get install -y libpq-dev python3-dev

echo "********** Install other build/install dependencies."
apt-get install -y unzip xz-utils

# *****************************************
# Install dev tools.
# *****************************************

echo "********** Install direnv."
# https://direnv.net/
apt-get install -y direnv

echo "********** Install latest Git."
# https://launchpad.net/~git-core/+archive/ubuntu/ppa
add-apt-repository -y ppa:git-core/ppa
apt-get update
apt-get install -y git tig

echo "********** Install jq."
# https://stedolan.github.io/jq/
apt-get install -y jq

echo "********** Install poppler-utils."
apt-get install -y poppler-utils
# echo "********** Install shellcheck {$shellcheck_version}."
# https://www.shellcheck.net/
# wget -qO- "https://github.com/koalaman/shellcheck/releases/download/${shellcheck_version?}/shellcheck-${shellcheck_version?}.linux.x86_64.tar.xz" | tar -xJv
# cp "shellcheck-${shellcheck_version}/shellcheck" /usr/local/bin/

# *****************************************
# Install cloud tools.
# *****************************************

echo "********** Install the latest stable AWS CLI."
# https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html
curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
./aws/install --update
rm -f awscliv2.zip
/usr/local/bin/aws --version

echo "********** Install latest stable Docker-CE."
# https://docs.docker.com/install/linux/docker-ce/ubuntu/
# apt-get remove docker docker-engine docker.io cotainerd runc
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
apt-key fingerprint 0EBFCD88
add-apt-repository -y "deb [arch=arm64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-get update
apt-get install docker-ce docker-ce-cli containerd.io


echo "********** Install latest stable docker-compose."
# https://docs.docker.com/compose/install/
curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
curl -L https://raw.githubusercontent.com/docker/compose/1.29.2/contrib/completion/bash/docker-compose -o /etc/bash_completion.d/docker-compose
# docker-compose --version

# echo "********** Install Terraform ${terraform_version}."
# https://www.terraform.io/downloads.html
# wget https://releases.hashicorp.com/terraform/${terraform_version}/terraform_${terraform_version}_linux_arm64.zip
#unzip terraform_${terraform_version}_linux_arm64.zip
#mv terraform /usr/local/bin/
#rm -f terraform_${terraform_version}_linux_arm64.zip

# *****************************************
# Install SERVER dependencies.
# *****************************************

echo "********** Install PostgreSQL ${postgresql_major_version}."
# https://www.postgresql.org/download/linux/ubuntu/
sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
apt-get update -y
apt-get install -y postgresql-${postgresql_major_version}
systemctl start postgresql@${postgresql_major_version}-main
systemctl status postgresql@${postgresql_major_version}-main

echo "********** Install Redis."
# https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-18-04
apt-get install -y redis-server
sed -i 's/supervised no/supervised systemd/g' /etc/redis/redis.conf
systemctl restart redis.service
systemctl status redis.service

# FIN (but more in the user script)
