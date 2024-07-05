#!/usr/bin/env python3

import argparse

import command as cmd
import osinfo
import pkgmgr
import os


def docker(pkg: pkgmgr.PackageManager, osRelease: osinfo.Release):
	cmd.log('Attempting to remove any existing Docker and Podman installations')
	pkg.remove(['docker', 'docker-client', 'docker-client-latest', 'docker-common', 'docker-latest', 'docker-latest-logrotate', 'docker-logrotate', 'docker-selinux', 'docker-engine-selinux', 'docker-engine', 'podman'])

	# add docker repo in the distro-specific way
	if osRelease.distro == 'fedora':
		cmd.log('Importing Docker CE repo from download.docker.com')
		cmd.run(['dnf', 'config-manager', '--add-repo', 'https://download.docker.com/linux/fedora/docker-ce.repo'])
	elif osRelease.distro == 'rocky' or osRelease.distro == 'centos':
		cmd.log('Importing Docker CE repo from download.docker.com')
		cmd.run(['dnf', 'config-manager', '--add-repo', 'https://download.docker.com/linux/centos/docker-ce.repo'])
	elif osRelease.distro == 'debian':
		cmd.log('Installing ca-certificates and curl (required for Docker CE installation)')
		pkg.install(['ca-certificates', 'curl'])

		# add the repo
		cmd.log('Adding the Docker CE repository')
		cmd.run(['install', '-m', '0755', '-d', '/etc/apt/keyrings'])
		cmd.run(['curl', '-fsSL', 'https://download.docker.com/linux/debian/gpg', '-o', '/etc/apt/keyrings/docker.asc'])
		cmd.run(['chmod', 'a+r', '/etc/apt/keyrings/docker.asc'])

		# add add repo to apt's sources
		cmd.log('Adding the Docker CE repository to Apt\'s sources')
		cmd.run(['echo', '"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc]', 'https://download.docker.com/linux/debian', '$(. /etc/os-release && echo "$VERSION_CODENAME")', 'stable"', '|', 'tee', '/etc/apt/sources.list.d/docker.list'])


	cmd.log('Installing Docker CE components')
	pkg.install(['docker-ce', 'docker-ce-cli', 'containerd.io', 'docker-buildx-plugin', 'docker-compose-plugin'])

	cmd.log('Enable Docker CE')
	cmd.run(['systemctl', 'enable', '--now', 'docker'])

	cmd.log('Testing Docker with hello-world')
	cmd.run(['docker', 'run', 'hello-world'])



def rocky_centos(pkg: pkgmgr.PackageManager):
	"""
	Run Rocky/Cent OS-specific commands, including installing some extras.
	"""
	cmd.log('Installing dnf-plugins-core and EPEL')
	pkg.install(['dnf-plugins-core', 'epel-release'])

	cmd.log('Enabling the Code Ready Builder repo')
	cmd.run(['/usr/bin/crb', 'enable'])

	cmd.log('Installing ncurses for the `clear` command')
	pkg.install(['ncurses'])

	cmd.log('Installing extras')
	pkg.install(['which', 'nano', 'neovim', 'less', 'openssh-server', 'man'])



def fedora(pkg: pkgmgr.PackageManager):
	"""
	Run Fedora-specific commands, including installing some extras.
	"""
	cmd.log('Installing dnf-plugins-core')
	pkg.install(['dnf-plugins-core'])

	cmd.log('Installing extras')
	pkg.install(['which', 'nano', 'neovim', 'less', 'openssh-server', 'man'])



def debian(pkg: pkgmgr.PackageManager):
	"""
	Run Debian-specific commands, including installing some extras.
	"""
	cmd.log('Installing extras')
	pkg.install(['nano', 'neovim', 'less', 'sudo', 'man'])



def ps1():
	cmd.log('Setting PS1')

	ps1var = """
function nonzero_return() {
	RETVAL=$?
	[ $RETVAL -ne 0 ] && echo "<$RETVAL> "
}

export PS1="\\[\\e[31m\\]\\`nonzero_return\\`\\[\\e[m\\][\\[\\e[32m\\]\\u\\[\\e[m\\] @ \\[\\e[36m\\]\\h\\[\\e[m\\] ; \\[\\e[35m\\]\\W\\[\\e[m\\]] \\$ "
"""

	bashrcPath = f'{os.path.expanduser("~")}/.bashrc'

	with open(bashrcPath, 'a') as bashrcF:
		bashrcF.write(ps1var)
		bashrcF.write(f'export HOME=\"{os.path.expanduser("~")}\"\n')

	cmd.run(['source', bashrcPath])



def init():
	osRelease = osinfo.Release()
	if osRelease.distro not in ['fedora', 'rocky', 'centos', 'debian']:
		cmd.log(f'Detected distro {osRelease.distro} is currently not supported for automatic setup installation. Only Fedora, Rocky, Cent OS, and Debian are supported at this time.')
		exit(1)

	
	parser = argparse.ArgumentParser(description='A very helpful automated script used for setting up VMs and LXCs in my homelab.', prog='pism')

	# metavar='non_interactive',
	parser.add_argument('--non-interactive', action='store_true', help='Run in non-interactive mode.')
	parser.add_argument('--docker', action='store_true', help='Install Docker CE')

	args = parser.parse_args()

	if args.non_interactive:
		non_interactive(osRelease, args.docker)
	else:
		interactive(osRelease)



def interactive(osRelease: osinfo.Release):
	def strToBool(string: str, yes='y', defaultYes=True):
		string = string.lower()

		if defaultYes:
			if string == yes or string == '':
				return True
			else:
				return False
		else:
			if string == yes:
				return True
			else:
				return False

	installDocker = strToBool(input('Install Docker CE? [Y/n] '))
	proceed = strToBool(input('Proceed with automated setup? [Y/n] '))

	if proceed != True:
		print('Aborting')
		exit(2)
	else:
		non_interactive(osRelease, installDocker)	



def non_interactive(osRelease: osinfo.Release, installDocker: bool):
	pkg = pkgmgr.PackageManager(osRelease)

	cmd.log('Running updates')
	pkg.update()

	if osRelease.distro == 'fedora':
		fedora(pkg)
	elif osRelease.distro == 'debian':
		debian(pkg)
	elif osRelease.distro == 'rocky' or osRelease.distro == 'centos':
		rocky_centos(pkg)

	if installDocker:
		docker(pkg, osRelease)

	ps1()


if __name__ == '__main__':
	init()
