


class Version:
	def __init__(self, pretty: str, number: str, codename: str):
		self.pretty = pretty
		self.id = number
		self.codename = codename



class Release:
	def __init__(self):
		raw = self._get_dict()

		self.name = raw['NAME']
		self.version = Version(
			pretty = raw['VERSION'], 
			number = raw['VERSION_ID'], 
			codename = raw['VERSION_CODENAME']
		)
		self.distro = raw['ID']
		"""
		Lowercase distro name; i.e. 'ubuntu', 'fedora', 'rhel'.
		"""
		self.platformID = raw['PLATFORM_ID']
		self.pretty = raw['PRETTY_NAME']
		self.ansiColor = raw['ANSI_COLOR']
		self.logo = raw['LOGO']
		self.cpeName = raw['CPE_NAME']
		self.defaultHostname = raw['DEFAULT_HOSTNAME'] 
		self.homeURL = raw['HOME_URL']
		self.documentationURL = raw['DOCUMENTATION_URL']
		self.supportURL = raw['SUPPORT_URL']
		self.bugReportURL = raw['BUG_REPORT_URL']
		
	

	def _get_dict(self) -> dict[str, str]:
		d: dict[str, str] = {}

		with open('/etc/os-release', 'r') as f:
			raw = f.readlines()

		# create dictionary from list of lines
		for l in raw:
			pair = l.split()
			d[pair[0]] = pair[1]
		
		return d
