import os
import time

from django.core.management import call_command, BaseCommand, CommandError
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class CompileSCSSEventHandler(PatternMatchingEventHandler):

    _files_changed = False

    def on_modified(self, event):
        self._files_changed = True

    @property
    def files_changed(self):
        files_changed = self._files_changed
        self._files_changed = False
        return files_changed


class Command(BaseCommand):
    args = 'path'
    help = 'Watch all scss files and compile them to css'

    def handle(self, *args, **options):
        path = args[0] if len(args) else '.'
        if not os.path.exists(path) and not os.path.isdir(path):
            raise CommandError('%s is not an existing directory' % (path,))
        event_handler = CompileSCSSEventHandler(
            ignore_directories=True, patterns=['*.scss'])
        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(2)
                if event_handler.files_changed:
                    call_command('collectstatic', interactive=False, verbosity=0)
                    call_command('compilescss')
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
