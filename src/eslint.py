import os
import tempfile
from subprocess import Popen, PIPE
from time import sleep

import sublime

from . import preferences, pathutil


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
    cmd = None

    local_eslint = preferences.get_local_eslint_path(directory)
    if local_eslint:
        node = pathutil.find_executable(preferences.get_path(), 'node')
        if not node:
            raise Exception('Could not find Node.js. Check that your configuration is correct.')
        cmd = [node, local_eslint]
    else:
        eslint = pathutil.find_executable(preferences.get_path(), 'eslint')
        if not eslint:
            raise Exception('Could not find eslint. Check that your configuration is correct.')
        cmd = [eslint]

    config = preferences.get_config_path(directory)

    cmd.extend(['--fix', filename])
    if config:
        cmd.extend(['--config', config])

    print(cmd)
    try:
        proc = Popen(cmd, stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=(sublime.platform() == 'windows'))
        proc.communicate()
        with open(filename, 'r', encoding='utf-8') as formatted:
            return formatted.read()
    except OSError:
        raise Exception('Error occured when running --fix')

    return None
