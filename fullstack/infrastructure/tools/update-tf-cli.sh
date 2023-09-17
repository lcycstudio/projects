#!/usr/bin/env bash
#
# Installs/upgrades the Terraform CLI tool.
#
# Usage:
#
#   sudo bash <script_name>
#
set -e

readonly terraform_version=${1:-0.13.2}

pushd -n "$(pwd)"
readonly tmp_dir=$(mktemp -d -t terraformupdate-XXXXXXXXXX)
cd "$tmp_dir"
# https://www.terraform.io/downloads.html
wget https://releases.hashicorp.com/terraform/${terraform_version}/terraform_${terraform_version}_linux_amd64.zip
unzip "terraform_${terraform_version}_linux_amd64.zip"
mv terraform /usr/local/bin/
rm -f "terraform_${terraform_version}_linux_amd64.zip"
popd
