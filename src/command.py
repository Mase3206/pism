import subprocess


LOG_FILE_PATH = 'setup.log'


def log(output: str, printOutput=True):
	"""
	Logs the given output to a file and stdout. Writing to stdout can be disabled by setting `printOutput` to `False`.
	"""
	with open(LOG_FILE_PATH, '+a') as logF:
		logF.write(output)

	if printOutput:
		print(output)


def run(command: list[str], printOutput=False, logOutput=True):
	"""
	Run the given command.
	"""

	with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
		output = process.communicate()[0]\
			.decode('utf-8')
		
	if printOutput:
		print(output)
	if logOutput:
		log(output, printOutput=False)
