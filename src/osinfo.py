class Version:
	def __init__(self, pretty: str, number: str, codename: str):
		self.pretty = pretty
		self.id = number
		self.codename = codename
	
	def __repr__(self) -> str:
		return f"Version(pretty='{self.pretty}', id='{self.id}', codename='{self.codename}')"



class Release:
	def __init__(self):
		raw = self._get_dict()

		self.name = raw['NAME']
		self.version = Version(
			pretty = raw.get('VERSION', ''), 
			number = raw.get('VERSION_ID', ''), 
			codename = raw.get('VERSION_CODENAME', '')
		)
		self.distro = raw['ID']
		"""
		Lowercase distro name; i.e. 'ubuntu', 'fedora', 'rhel'.
		"""
		self.platformID = raw['PLATFORM_ID']
		self.pretty = raw['PRETTY_NAME']
		#self.ansiColor = raw['ANSI_COLOR']
		#self.logo = raw['LOGO']
		#self.cpeName = raw['CPE_NAME']
		
	

	def _get_dict(self) -> dict[str, str]:
		d: dict[str, str] = {}

		with open('/etc/os-release', 'r') as f:
			raw = f.readlines()

		# create dictionary from list of lines
		for l in raw:
			pair = l[:-1].split('=')
			if (pair[1][0] == "'" or pair[1][0] == '"') and (pair[1][-1] == "'" or pair[1][-1] == '"'):
				d[pair[0]] = pair[1][1:-1]
			else:
				d[pair[0]] = pair[1]
		
		return d
	
	def __repr__(self) -> str:
		return f"Release(name='{self.name}', version={self.version}, distro='{self.distro}', platformID='{self.platformID}', pretty='{self.pretty}', ansiColor='{self.ansiColor}', logo='{self.logo}', cpeName='{self.cpeName}')"


def _tc():
	r = Release()
	a = repr(r)
	print(r)

if __name__ == '__main__':
	_tc()
