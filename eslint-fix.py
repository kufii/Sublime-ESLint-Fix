import tempfile
import os
from subprocess import Popen, PIPE
import sublime
import sublime_plugin

PLUGIN_NAME = 'eslint-fix'
SETTINGS_FILE = PLUGIN_NAME + '.sublime-settings'
IS_WINDOWS = sublime.platform() == 'windows'

class EslintFixCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		full_file_region = sublime.Region(0, self.view.size())
		file_text = self.view.substr(full_file_region)
		fixed_text = EsLint.fix(file_text, self.view.file_name())

		if not fixed_text or fixed_text == file_text:
			return

		self.view.replace(edit, full_file_region, fixed_text)


class EsLint:
	@staticmethod
	def fix(text, filename):
		dirname = None
		if filename:
			dirname = os.path.dirname(filename)
		with tempfile.NamedTemporaryFile(mode='w+', delete=False, dir=dirname, encoding='utf-8') as tmp:
			try:
				tmp.write(text)
				tmp.close()
				return EsLint.run_eslint(tmp.name, dirname)
			finally:
				os.unlink(tmp.name)
		return None

	@staticmethod
	def run_eslint(filename, directory):
		node = Preferences.get_node_path()
		eslint = Preferences.get_eslint_path(directory)
		config = Preferences.get_config_path(directory)

		if node and eslint:
			cmd = [node, eslint, '--fix', filename]
			if config:
				cmd.extend(["--config", config])

			try:
				proc = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=IS_WINDOWS)
				proc.communicate()
				with open(filename, "r", encoding="utf-8") as formatted:
					return formatted.read()
			except OSError:
				raise Exception('Couldn\'t find Node.js. Make sure it\'s in your $PATH by running `node -v` in your command-line.')

		return None

class Preferences:
	@staticmethod
	def get_pref(key):
		default = sublime.load_settings(SETTINGS_FILE).get(key)
		custom_settings = sublime.active_window().active_view().settings()

		if custom_settings.has(PLUGIN_NAME):
			return custom_settings.get(PLUGIN_NAME).get(key, default)

		return default

	@staticmethod
	def find_up(directory, path):
		while not os.path.exists(os.path.join(directory, path)):
			parent_dir = os.path.abspath(os.path.join(directory, os.pardir))
			if parent_dir == directory:
				return None
			directory = parent_dir

		return os.path.join(directory, path)

	@staticmethod
	def get_node_path():
		return Preferences.get_pref('node_path').get(sublime.platform())

	@staticmethod
	def get_local_eslint_path(directory):
		return Preferences.find_up(directory, Preferences.get_pref('local_eslint_path').get(sublime.platform()))

	@staticmethod
	def get_eslint_path(directory):
		if directory:
			local_path = Preferences.get_local_eslint_path(directory)
			if local_path:
				return local_path

		return Preferences.get_pref('eslint_path').get(sublime.platform())

	@staticmethod
	def get_config_path(directory):
		config_path = Preferences.get_pref("config_path").get(sublime.platform())

		if not config_path:
			return None

		if os.path.isfile(config_path):
			return config_path
		elif not directory:
			return None

		return Preferences.find_up(directory, config_path)
