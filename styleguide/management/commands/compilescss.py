from os import path

from django.core.management import BaseCommand, CommandError, call_command
from django.conf import settings

from ... import STYLE_GUIDE_CONFIG
from ...utils import compile_scss_file


class Command(BaseCommand):
    help = 'Compile scss files to css'

    def handle(self, *args, **options):
        call_command(
            'collectstatic', interactive=False, verbosity=0)
        for input_file, output_file in self.get_style_files():
            try:
                compile_scss_file(input_file, output_file)
            except IOError as e:
                raise CommandError(str(e))
            else:
                self.stdout.write('%s > %s' % (input_file, output_file))

    def get_style_files(self):
        style_files = STYLE_GUIDE_CONFIG['style_files']
        css_root = STYLE_GUIDE_CONFIG['css_root']
        for input_file, output_file in style_files:
            yield (path.join(settings.STATIC_ROOT, input_file),
                   path.join(css_root, output_file))
