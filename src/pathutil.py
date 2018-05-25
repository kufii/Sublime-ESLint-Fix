import os


def find_up(directory, path):
	while not os.path.exists(os.path.join(directory, path)):
		parent_dir = os.path.abspath(os.path.join(directory, os.pardir))
		if parent_dir == directory:
			return None
		directory = parent_dir

	return os.path.join(directory, path)


def expand_path(path):
	return os.path.expanduser(os.path.expandvars(path))
