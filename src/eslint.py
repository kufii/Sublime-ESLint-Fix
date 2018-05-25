import os
import tempfile
from subprocess import Popen, PIPE
from time import sleep

import sublime

from . import preferences


def fix(text, filename):
	dirname = None
	if filename:
		dirname = os.path.dirname(filename)
	with tempfile.NamedTemporaryFile(mode='w+', delete=False, dir=dirname, encoding='utf-8') as tmp:
		try:
			tmp.write(text)
			tmp.close()
			return _run(tmp.name, dirname)
		finally:
			# The loop is here as a really dumb workaround for a rare google drive race condition.
			for _ in range(0, 10):
				try:
					os.unlink(tmp.name)
					break
				except PermissionError:
					sleep(0.01)
	return None


def _run(filename, directory):
	node = preferences.get_node_path()
	eslint = preferences.get_eslint_path(directory)
	config = preferences.get_config_path(directory)

	if node and eslint:
		cmd = [node, eslint, '--fix', filename]
		if config:
			cmd.extend(['--config', config])

		try:
			proc = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=(sublime.platform() == 'windows'))
			proc.communicate()
			with open(filename, 'r', encoding='utf-8') as formatted:
				return formatted.read()
		except OSError:
			raise Exception('Couldn\'t find Node.js. Check that your configuration is correct.')

	return None
