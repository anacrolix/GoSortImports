import os
import subprocess
import sublime, sublime_plugin

class GoSortImports(sublime_plugin.TextCommand):
    '''This command runs the view text through rogpeppe's sortimports.'''

    def run(self, edit):
        view = self.view
        filename = view.file_name()
        if not filename.endswith('.go'):
            return
        region = sublime.Region(0, view.size())
        input = view.substr(region).encode('utf8')
        if not input:
            return
        settings = view.settings()
        env_settings = settings.get('env')
        env = os.environ.copy()
        if 'GOPATH' in env_settings:
            env['GOPATH'] = os.path.expandvars(env_settings['GOPATH'])
        if 'PATH' in env_settings:
            env['PATH'] = os.path.expandvars(env_settings['PATH'])
        if 'GOPATH' not in env:
            print('calling sortimports without GOPATH')
        popen = subprocess.Popen(
            [settings.get("sortimports", "sortimports"), "-c", filename],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
        stdout, stderr = popen.communicate(input)
        if popen.returncode != 0:
            raise Exception(stderr)
        if input == stdout:
            return
        view.replace(edit, region, stdout.decode('utf8'))


class SortImports(sublime_plugin.EventListener):

    def on_pre_save(self, view):
        view.run_command('go_sort_imports')
