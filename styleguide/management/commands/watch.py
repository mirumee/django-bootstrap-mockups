import os
import time

from django.core.management import call_command, BaseCommand, CommandError
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from sass import compile_file

from ... import STYLE_GUIDE_CONFIG


class CollectStaticsEventHandler(PatternMatchingEventHandler):

    def on_modified(self, event):
        call_command('collectstatic', interactive=False)
        input_file = STYLE_GUIDE_CONFIG['input_file']
        output_file = STYLE_GUIDE_CONFIG['output_file']
        if not os.path.exists(input_file):
            raise CommandError('%s does not exist' % (input_file,))
        output_path = os.path.split(output_file)[0]
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        with open(output_file, 'w') as css_file:
            css_file.write(compile_file(input_file))


class Command(BaseCommand):
    args = 'path'
    help = 'Watch static'

    def handle(self, *args, **options):
        path = args[0] if len(args) else '.'
        if not os.path.exists(path) and not os.path.isdir(path):
            raise CommandError('%s is not an existing directory' % (path,))
        event_handler = CollectStaticsEventHandler(
            ignore_directories=True, patterns=['*.less', '*.scss'])
        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
