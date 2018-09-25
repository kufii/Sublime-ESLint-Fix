import os

import sublime


def find_up(directory, path):
    while not os.path.exists(os.path.join(directory, path)):
        parent_dir = os.path.abspath(os.path.join(directory, os.pardir))
        if parent_dir == directory:
            return None
        directory = parent_dir

    return os.path.join(directory, path)


def expand_path(path):
    return os.path.expanduser(os.path.expandvars(path))


def can_exec(path):
    return os.path.isfile(path) and os.access(path, os.X_OK)


def find_executable(paths, executable):
    for directory in paths:
        path = os.path.join(directory, executable)

        # On Windows, if path does not have an extension, try .exe, .cmd, .bat
        if sublime.platform() == 'windows' and not os.path.splitext(path)[1]:
            for extension in ('.exe', '.cmd', '.bat'):
                path_ext = path + extension
                if can_exec(path_ext):
                    return path_ext
        elif can_exec(path):
            return path

    return None
