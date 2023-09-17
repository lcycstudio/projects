#!/usr/bin/env bash
#
# Provisions an Ubuntu 18.04 Vagrant box for cloud development. This script
# handles all the provisioning as the user. See the *_root.sh script for
# provisioning as root.
#
set -e

# *****************************************
# Config
# *****************************************
readonly nvm_version="v0.35.3"
readonly node_version="14.7.0"
readonly pyenv_version="v1.2.20"
readonly python_version="3.8.5"

# *****************************************
# Configure Bash.
# *****************************************
echo "********** Add Bash customizations."

# Quote the terminator symbol to not evaluate anything in the multiline string.
cat <<"EOBASHRC" >> "$HOME/.bashrc"

# ********** BASH CUSTOMIZATIONS **********

# Configure terminal prompt.
parse_git_branch() {
	git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(git:\1)/'
}

export PS1='\[\e[0;32m\]\u@\h\[\e[m\] \[\e[1;36m\]\w\[\e[m\] $(parse_git_branch)\[\e[m\] \[\e[1;32m\]\$\[\e[m\] \[\e[1;37m\]'

export CLICOLOR=1
export LSCOLORS=gxfxcxdxbxegedabagacad

EOBASHRC

# *****************************************
# Configure dev tools as user.
# *****************************************

echo "********** Configure direnv."
cat <<"EODIRENV" >> "$HOME/.bashrc"
# direnv
eval "$(direnv hook bash)"

EODIRENV

echo "********** Configure Git."
cat <<"EODGITIGNOREGLOBAL" >> "$HOME/.gitignore_global"
# Created by https://www.gitignore.io/api/code,linux
# Edit at https://www.gitignore.io/?templates=code,linux

### Linux ###
*~

# temporary files which can be created if a process still has a handle open of a deleted file
.fuse_hidden*

# KDE directory preferences
.directory

# Linux trash folder which might appear on any partition or disk
.Trash-*

# .nfs files are created when an open file is removed but is still being accessed
.nfs*

# End of https://www.gitignore.io/api/code,linux
EODGITIGNOREGLOBAL

git config --global core.excludesfile "$HOME/.gitignore_global"

# *****************************************
# Install NVM and Node.
# *****************************************

# https://github.com/nvm-sh/nvm#installation-and-update

echo "********** Install nvm to manage multiple Node.js installs."
git clone https://github.com/nvm-sh/nvm.git "$HOME/.nvm"
git -C "$HOME/.nvm" checkout ${nvm_version}
cat <<"EONVM" >> "$HOME/.bashrc"
# nvm
# shellcheck disable=SC2155
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm

EONVM

# shellcheck disable=SC2155
export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm

echo "********** Install Node $node_version."
nvm install "$node_version"
nvm use "$node_version"

# *****************************************
# Install pyenv and Python.
# *****************************************

# https://github.com/pyenv/pyenv#basic-github-checkout

echo "********** Install pyenv to manage multiple Python installs."
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
git -C "$HOME/.pyenv" checkout ${pyenv_version}

cat <<"EOPYENV" >> "$HOME/.bashrc"
# pyenv
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
if command -v pyenv 1>/dev/null 2>&1; then
    eval "$(pyenv init -)"
fi

EOPYENV

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
if command -v pyenv 1>/dev/null 2>&1; then
    eval "$(pyenv init -)"
fi

echo "********** Install Python ${python_version}."
pyenv install "$python_version"
pyenv global "$python_version"
pip install --upgrade pip
pip install pipenv flake8 autopep8

# FIN
