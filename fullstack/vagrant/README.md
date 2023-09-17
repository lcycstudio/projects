# Developer VM with Vagrant

Use [Vagrant](https://www.vagrantup.com/) and this repo to create a local Ubuntu 18.04 VM configured
for fargate development.

Detailed steps follow, but if you already know Vagrant, it's the basic ```vagrant up``` and the
other standard Vagrant commands. But please read part F about the VM SSH key, jump boxes, and
GitLab.

## A. Install Vagrant

Download Vagrant the [Vagrant downloads page](https://www.vagrantup.com/downloads) and install the
command-line tool.

### Mac: Homebrew

If you're on Mac and have [Homebrew](https://brew.sh/) installed, you can also install Vagrant via:

```bash
brew cask install vagrant
```

## B. Install a Provider

A Vagrant "provider" is a hypervisor to run VM on your development machine. The Vagrant tool has
built-in support for VirtualBox, Hyper-V, and Docker. If you can't decide, install
[VirtualBox](https://www.virtualbox.org/).

### Mac: Parallels (or Other Providers)

If you're using [Parallels](https://github.com/Parallels/vagrant-parallels) to run VMs on your Mac,
install the Parallels plugin:

```bash
vagrant plugin install vagrant-parallels
```

Do something similar if you're using another hypervisor that's not supported by Vagrant by default.

#### Parallels Workaround (2020/08/04)

Provision the Parallels guest tools manually after creating the box or after updating Parallels.

```bash
vagrant ssh
sudo ptiagent-cmd
exit
vagrant reload
```

This is to workaround a [bug](https://github.com/Parallels/vagrant-parallels/issues/350). After that
is resolved, undo this note and the workaround in the Vagrantfile.

## C. Update Vagrant

If you already have Vagrant installed and setup on your computer, make sure to update the boxes and
plugins before creating the VM:

```bash
vagrant plugin update
vagrant box update
```

## D. Provision the VM

Open this repo in the terminal, and then enter:

```bash
vagrant up
```

That will generate a Vagrant-managed Ubuntu 18.04 VM following the instructions in the
*Vagrantfile*. That in-turn uses the Bash scripts in the ```./provisioners``` folder. Examine those
scripts to see what exactly is being done to the base Ubuntu 18.04 VM.

## E. Use the VM

To enter the VM, run ```vagrant ssh``` from the repo folder. To SSH from anywhere, run
```vagrant ssh-config``` and copy that to your ```~/.ssh/config``` folder. Then you can
```ssh $vagranthostname``` from any terminal or from any client that uses the SSH config file.
Although consider renaming the box's host name from probably *default* to something more memorable
(e.g., *fargatevagrant*).

To stop the VM (e.g., after you're done for the day), run: ```vagrant suspend``` (sleep) or
```vagrant halt``` (shutdown). The next day, re-start the VM with ```vagrant up``` command. Or you
can restart with ```vagrant reload```.

To destroy the VM, run: ```vagrant destroy```. Re-create the VM with the ```vagrant up``` command.
If you do this, you'll need to create a new VM SSH key and update both GitLab and the fargate jump
box (see part F discussing VM's SSH key).

Learn more in the [Vagrant CLI documentation](https://www.vagrantup.com/docs/cli).

### VSCode + Remote SSH

If you're using Visual Studio Code, you can work directly with the VM using VSCode's [remote-ssh
extension and workflow](https://code.visualstudio.com/docs/remote/ssh). I.e., you're using VSCode
installed on the host but working inside the VM via SSH.

First, add the Vagrant box to your SSH config using ```vagrant ssh-config``` as described
previously.

Then in VSCode, run the *Remote-SSH: Connect to Host* command; find the Vagrant VM host that you
added to the SSH config file; and click to connect. This will open a new VSCode window that operates
in the VM via SSH. I.e, the file browser will look in the VM's file system and the integrated
terminal will open a Bash terminal in the VM.

### Synced Folders

Another way is to setup sync folders that folders on your computer that are mounted on the VM. Then
you can make changes to anything in the sync folders from either your host computer or from within
the VM.

If you do this, point your IDE to the sync folders from your host computer side, make changes, and
then ```vagrant ssh`` into the VM to run/test.

If you go this way, create a branch of this repo called *dev/$your-name* and add the sync folder
configuration to the Vagrantfile. See the
[synced folder documentation](https://www.vagrantup.com/docs/synced-folders/basic_usage) for more
info.

## F. VM's SSH Key (IMPORTANT!)

fargate uses a [jump server](https://en.wikipedia.org/wiki/Jump_server) to connect to AWS resources in
private subnets. So you'll need to [create a SSH key pair](https://docs.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
on your VM. Then add (or ask a fargate jump box admin to add) your newly created VM public key to the
jump server's servers's *authorized_keys* file:

```bash
# In a VM terminal, copy the public SSH key to your clipboard.
# In a host terminal, SSH to the jump server.
# Then in the jump server terminal:
echo "$paste_the_vm_public_ssh_key_here" >> ~/.ssh/authorized_keys
```

And if you're running completely in the VM (i.e, not using a synced folder), you'll also need
to add the VM's public key to your GitLab settings so you can clone repos directly in the box.

## G. User IP Address (SUPER IMPORTANT!)

Search your IPv4 address on Google or [this link](https://whatismyipaddress.com/)
Send your address to an admin, and he will add the address to the jump box.


## H. Updating the Vagrantfile

If there are changes to the Vagrantfile (e.g., increasing the RAM, changing the sync folders, etc.),
run this to capture the changes in the box:

```bash
cd path/to/this/repo
vagrant reload
```
