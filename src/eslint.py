import json
import os
from subprocess import Popen, PIPE

import sublime

from . import preferences, pathutil


def fix(text, filename):
    return _run(text, filename)


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


def _run(text, filepath):
    cmd = None

    filename = None
    directory = None
    if filepath:
        (directory, filename) = os.path.split(filepath)

    local_eslint = preferences.get_local_eslint_path(directory)
    if local_eslint:
        cmd = [_get_node_path(), local_eslint]
    else:
        if sublime.platform() == 'windows':
            cmd = [_get_eslint_path()]
        else:
            cmd = [_get_node_path(), _get_eslint_path()]

    config = preferences.get_config_path(directory)

    cmd.extend([
        '--stdin',
        # When formatting from stdin, we need to pass --fix-dry-run, not --fix
        '--fix-dry-run',
        # Default formatter doesn't output formatted code.
        '--format=json'
    ])
    if filename:
        # Report file name to eslint.
        cmd.extend(['--stdin-filename', filename])
    if config:
        cmd.extend(['--config', config])

    try:
        proc = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE,
                     cwd=directory,
                     shell=(sublime.platform() == 'windows'))
        (stdout, stderr) = proc.communicate(text.encode('utf-8'))
        # Possible exit codes:
        #  0 - no linting issues. Might or might not provide formatting.
        #  1 - has linting issues. Might or might not provide formatting.
        #  2 - serious error, e.g. missing configuration; error in stderr
        if proc.returncode <= 1:
            obj = json.loads(stdout.decode('utf-8'), encoding='utf-8')
            # First list item is the result for formatted file.
            if 'output' in obj[0]:
                return obj[0].get('output')
        else:
            err = stderr.decode('utf-8')
            print('ESlint Fix: File not formatted due to an error "%s".' % err)
    except OSError:
        raise Exception('Error occured when running: %s' % ' '.join(cmd))

    return None
