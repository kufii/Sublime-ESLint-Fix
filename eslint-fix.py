import sublime
import sublime_plugin

from .src import eslint


class EslintFixCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        full_file_region = sublime.Region(0, self.view.size())
        file_text = self.view.substr(full_file_region)
        fixed_text = eslint.fix(file_text, self.view.file_name())

        if not fixed_text or fixed_text == file_text:
            return

        self.view.replace(edit, full_file_region, fixed_text)
