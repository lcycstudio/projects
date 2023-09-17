# Server Developer VM with Ubuntu/UTM for Apple Silicon CPUs

For Apple silicon CPUs (M1, etc.), use [UTM/Ubuntu](https://www.vagrantup.com/) for the virtual machine (VM)
and this repo to create a local Ubuntu 20.04 VM hosted on UTM configured for Server development. For non-arm64 
architecture CPUs, please refer to the [Vagrant](https://gitlab.com/server1/project-server/vagrant.git) repository.

If you have a virtual machine running on ARM64 architecture, you can jump to step [D](https://gitlab.com/server1/project-server/ubuntu#d-vms-ssh-key-important). UTM is free to download or $9.99 on the Mac App Store. 

## A. Install UTM

Download UTM from the [UTM download page](https://mac.getutm.app/) for Mac and install UTM into Applications.

### Ubuntu: Download

Download Ubuntu 20.04.x arm64 ISO file from the official [Ubuntu download page](https://ubuntu.com/download/server/arm). 
Have this ISO file ready for the following steps.

### UTM: Install

Follow the steps on [UTM/Ubuntu 20.04](https://mac.getutm.app/gallery/ubuntu-20-04) to install Ubuntu VM onto UTM. Use 
the following system options 
during installation:
- VirtIO Size 15 GB
- Username and password
- Install OpenSSH Server
- Instal Ubuntu Desktop
- Enable clipboard and directory sharing

Other options use defaults. Restart Ubuntu when installation finishes.


## B. SSH Connection

### Remote SSH

Use the following command to find the Ubuntu server IP and remember the value, such 100.100.32.3
```bash
hostname -I
```

Now switch to your local machine (MacOS) and create a file called "config" on the `~/.ssh` folder. 
If the folder doesn't exist, create the folder in the first place. Open the MacOS Terminal and enter
the following command:

```bash
mkdir ~/.ssh
touch ~/.ssh/config
```

Copy the following content and paste it to the file. Replace the HostName with the Ubuntu IP adress 
($ubuntu_ip_address) and User with the username ($username).
```
Host serverubuntu
	HostName $ubuntu_ip_address
	User $username
	Port 22
	IdentitiesOnly no
	LogLevel INFO
```

Use the following command on the MacOS Terminal to establish a SSH connection to the Ubuntu server.
```bash
ssh $username@$ubuntu_ip_address
```

### VSCode + Remote SSH

If you're using Visual Studio Code, you can work directly with the VM using VSCode's [remote-ssh
extension and workflow](https://code.visualstudio.com/docs/remote/ssh). I.e., you're using VSCode
installed on the MacOS but working inside the Ubuntu VM via SSH.

In VSCode, search for the extension: Remote-SSH (published by MicroSoft) and install it. Click on
the "Open a Remote Window" icon and find the Ubuntu VM that you added to the "config" file above. 
Click "serverubuntu" to connect. 

Enter your password when prompted.

This will open a new VSCode window that operates in the VM via SSH. 
I.e, the file browser will look in the VM's file system and the integrated terminal will open a 
Bash terminal in the VM.


## C. Ubuntu Customization

It is recommended that you use VSCode to proceed the following steps via a remote ssh connection to the Ubuntu VM.

### Git: Install

To access the terminal, click on the "Show Applications" icon on the left bottom on the desktop. Search "Terminal" 
or scroll to the bottom and drag the "Terminal" icon to the left side for easy access later on. Git is a mature, 
actively maintained open source project, and it comes with Ubuntu. To check that Git is installed properly, use the 
command:
```bash
git --version
```

If Git is not installed, install Git using the following command in the VM terminal:

```bash
sudo apt install git-all
```

### Ubuntu: Repository

Create a folder called "server" on user's profile folder and clone the Ubuntu repository to the directory.

```bash
mkdir ~/server
cd ~/server
git init
git clone https://gitlab.com/server1/project-server/ubuntu.git
```

### Infrastructure: Installation

Use the bash script files in the folder to install system files to run the server project. Run 
the follow commands one by one.

```bash
sudo chmod +x ~/server/ubuntu/ubuntu_upgrade.sh
sudo chmod +x ~/server/ubuntu/ubuntu_apps.sh
sudo chmod +x ~/server/ubuntu/ubuntu_cleanup.sh
sudo ~/server/ubuntu/ubuntu_upgrade.sh
```

### NVM and Node: Installation

Install NVM and NodeJS using command line.

```bash
curl https://raw.githubusercontent.com/creationix/nvm/master/install.sh | bash 
source ~/.profile
nvm install 14.7.0
nvm use 14.7.0
```

Install Python and Pip using command line.

```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.8
python3 --version
sudo apt-get install python3-pip
sudo apt install python3.8-venv
```

### Bash Configuration

On your terminal enter the following command to start editing the file `~/.bashrc` using VSCode.
```bash
code ~/.bashrc
```

Add the following lines to bottom of the file `~/.bashrc`.

```
# ********** BASH CUSTOMIZATIONS **********

# Configure terminal prompt.
parse_git_branch() {
	git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/(git:\1)/'
}

export PS1='\[\e[0;32m\]\u@\h\[\e[m\] \[\e[1;36m\]\w\[\e[m\] $(parse_git_branch)\[\e[m\] \[\e[1;32m\]\$\[\e[m\] \[\e[1;37m\]'

export CLICOLOR=1
export LSCOLORS=gxfxcxdxbxegedabagacad
```

After installing the packages, use the follow command to clean up and reboot the VM. 
Press "CTRL+C" when "ubuntu_apps.sh" is finished executing.

```bash
source ~/.bashrc
sudo ~/server/ubuntu/ubuntu_apps.sh
sudo ~/server/ubuntu/ubuntu_cleanup.sh
```


## D. VM's SSH Key (IMPORTANT!)

Server uses a [jump server](https://en.wikipedia.org/wiki/Jump_server) to connect to AWS resources in
private subnets. So you'll need to [create a SSH key pair](https://docs.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
on your VM. Then add (or ask a Server jump box admin to add) your newly created VM public key to the
jump server's servers's *authorized_keys* file:

```bash
# In a VM terminal, copy the public SSH key to your clipboard.
# In a host terminal, SSH to the jump server.
# Then in the jump server terminal:
echo "$paste_the_vm_public_ssh_key_here" >> ~/.ssh/authorized_keys
```

And if you're running completely in the VM (i.e, not using a synced folder), you'll also need
to add the VM's public key to your GitLab settings so you can clone repos directly in the box.


## E. User IP Address (SUPER IMPORTANT!)

Search your IPv4 address on Google or [this link](https://whatismyipaddress.com/).
Send your address to an admin, and he will add the address to the jump box.
