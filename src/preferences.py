import os

import sublime

from . import pathutil


PLUGIN_NAME = 'eslint-fix'
SETTINGS_FILE = PLUGIN_NAME + '.sublime-settings'


def get_pref(key):
    default = sublime.load_settings(SETTINGS_FILE).get(key)
    custom_settings = sublime.active_window().active_view().settings()

    if custom_settings.has(PLUGIN_NAME):
        return custom_settings.get(PLUGIN_NAME).get(key, default)

    return default


def get_path():
    return map(pathutil.expand_path,
               filter(None,
                      get_pref('paths').get(sublime.platform()) +
                      os.environ.get('PATH', '').split(os.pathsep)))


def get_local_eslint_path(directory):
    local_path = pathutil.expand_path(get_pref('local_eslint_path').get(sublime.platform()))
    if local_path:
        return pathutil.find_up(directory, local_path)
    return None


def get_config_path(directory):
    config_path = pathutil.expand_path(get_pref('config_path').get(sublime.platform()))

    if not config_path:
        return None

    if os.path.isfile(config_path):
        return config_path
    elif directory:
        return pathutil.find_up(directory, config_path)

    return None
