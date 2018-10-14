import json
import os
from subprocess import Popen, PIPE

import sublime

from . import preferences, pathutil


_IS_WINDOWS = sublime.platform() == 'windows'
_ERROR_EXIT_CODE = 2


def _get_node_path():
    node = pathutil.find_executable(preferences.get_path(), 'node')
    if not node:
        raise Exception('Could not find Node.js. Check that your configuration is correct.')
    return node


def _get_eslint_path():
    eslint = pathutil.find_executable(preferences.get_path(), 'eslint')
    if not eslint:
        raise Exception('Could not find eslint. Check that your configuration is correct.')
    return eslint


def _get_command(directory, filename):
    cmd = None

    local_eslint = preferences.get_local_eslint_path(directory)
    if local_eslint:
        cmd = [_get_node_path(), local_eslint]
    else:
        if _IS_WINDOWS:
            cmd = [_get_eslint_path()]
        else:
            cmd = [_get_node_path(), _get_eslint_path()]

    cmd.extend([
        '--stdin',
        # When formatting from stdin, we need to pass --fix-dry-run, not --fix
        '--fix-dry-run',
        # Default formatter doesn't output formatted code.
        '--format=json'
    ])

    if filename:
        cmd.extend(['--stdin-filename', filename])

    config = preferences.get_config_path(directory)
    if config:
        cmd.extend(['--config', config])

    return cmd


def fix(text, filepath):
    directory = None
    filename = None
    if filepath:
        (directory, filename) = os.path.split(filepath)

    cmd = _get_command(directory, filename)

    try:
        proc = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE, cwd=directory, shell=_IS_WINDOWS)
        (stdout, stderr) = proc.communicate(text.encode('utf-8'))

        if proc.returncode == _ERROR_EXIT_CODE:
            print('ESlint Fix: File not formatted due to an error "%s".' % stderr.decode('utf-8'))
            return None

        obj = json.loads(stdout.decode('utf-8'), encoding='utf-8')
        # First list item is the result for formatted file.
        if 'output' in obj[0]:
            return obj[0].get('output')
    except OSError:
        raise Exception('Error occured when running: %s' % ' '.join(cmd))

    return None
