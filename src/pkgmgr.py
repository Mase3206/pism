import osinfo
import command as cmd
import subprocess




class AptGet:
	def __init__(self):
		self.name = 'apt-get'
	

	def install(self, packages: list[str]):
		"""
		Run `apt-get install -y` with the specified list of packages.
		"""

		command = ['apt-get', 'install', '-y']
		command += packages
		cmd.run(command)

	
	def update(self):
		"""
		Run `apt-get update && apt-get upgrade -y` to update package lists and upgrade all upgradable packages.
		"""

		command = ['apt-get', 'update']
		cmd.run(command)

		command = ['apt-get', 'upgrade', '-y']
		cmd.run(command)

	
	def remove(self, packages: list[str]):
		"""
		Run `apt-get remove -y` with the specified list of packages.
		"""

		command = ['apt-get', 'remove', '-y']
		command += packages
		cmd.run(command)



class Dnf:
	def __init__(self):
		self.name = 'dnf'
	

	def install(self, packages: list[str]):
		"""
		Run `dnf install -y` with the specified list of packages.
		"""

		command = ['dnf', 'install', '-y']
		command += packages
		cmd.run(command)

	
	def update(self):
		"""
		Run `dnf update -y` to update package lists and upgrade all upgradable packages.
		"""

		command = ['dnf', 'update', '-y']
		cmd.run(command)

	
	def remove(self, packages: list[str]):
		"""
		Run `dnf remove -y` with the specified list of packages.
		"""

		command = ['dnf', 'remove', '-y']
		command += packages
		cmd.run(command)



class Pacman:
	def __init__(self):
		self.name = 'pacman'
	

	def install(self, packages: list[str]):
		"""
		Run `pacman -S` with the specified list of packages.
		"""

		command = ['yes' | 'pacman', '-S']
		command += packages
		cmd.run(command)

	
	def update(self):
		"""
		Run `pacman -Syu` to update package lists and upgrade all upgradable packages.
		"""

		command = ['pacman', '-Syu']
		cmd.run(command)

	
	def remove(self, packages: list[str]):
		"""
		Run `pacman -Rs` with the specified list of packages.
		"""

		command = ['pacman', '-Rs']
		command += packages
		cmd.run(command)



class PackageManager:
	"""
	Main class used to interact with the system's package manager. It tries to detect the system automatically, prompting the user to manually input it when it cannot be detected.

	Constructor Arguments
	---------------------
		osRelease (osinfo.Release): the Release class for your Linux distro
	"""
	def __init__(self, osRelease: osinfo.Release):
		pName = self._get_package_manager(osRelease.distro)
		if pName == 'unknown':
			# overwrite input package manager command if unknown, then check
			pName = input('Please enter the command used to install packages: ')
		if pName == 'apt-get':
			self.packageManager = AptGet()
		elif pName == 'dnf':
			self.packageManager = Dnf()
		elif pName == 'pacman':
			self.packageManager = Pacman()
		else:
			cmd.log('PackageManager - package manager could not be set. Exiting.')
			exit(1)

	
	def _get_package_manager(self, distro: str):
		aptDistros = ['ubuntu', 'debian', 'mint']
		dnfDistros = ['rhel', 'fedora', 'rocky', 'centos']
		pacmanDistros = ['arch']
		
		cmd.log(f'PackageManager - found distro "{distro}"')
		if distro in aptDistros:
			cmd.log(f'PackageManager - matched distro "{distro}" to package manager "apt-get"')
			return 'apt-get'
		
		elif distro in dnfDistros:
			cmd.log(f'PackageManager - matched distro "{distro}" to package manager "dnf"')
			return 'dnf'
		
		elif distro in pacmanDistros:
			cmd.log(f'PackageManager - matched distro "{distro}" to package manager "apt-get"')
			return 'pacman'
		
		else:
			cmd.log(f'PackageManager - distro "{distro}" is not in the list of known distros')
			return 'unknown'
		

	def install(self, packages: list[str]):
		self.packageManager.install(packages)

	
	def update(self):
		self.packageManager.update()

	
	def remove(self, packages: list[str]):
		self.packageManager.remove(packages)
			


def _tc():
	pkg = Dnf()
	pkg.update()


if __name__ == '__main__':
	_tc()