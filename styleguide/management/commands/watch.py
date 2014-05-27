import os
import time

from django.core.management import call_command, BaseCommand, CommandError
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler


class CollectStaticsEventHandler(PatternMatchingEventHandler):

    def on_modified(self, event):
        call_command('collectstatic', interactive=False)


class Command(BaseCommand):
    args = 'path'
    help = 'Watch static'

    def handle(self, *args, **options):
        path = args[0] if len(args) else '.'
        if not os.path.exists(path) and not os.path.isdir(path):
            raise CommandError('%s is not an existing directory' % (path,))
        event_handler = CollectStaticsEventHandler(
            ignore_directories=True, patterns=['*.less', '*.sass'])
        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
