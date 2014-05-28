from django.core.management import BaseCommand, CommandError

from ... import STYLE_GUIDE_CONFIG
from ...utils import compile_scss_file


class Command(BaseCommand):
    help = 'Compile scss files to css'

    def handle(self, *args, **options):
        for input_file, output_file in STYLE_GUIDE_CONFIG['style_files']:
            try:
                compile_scss_file(input_file, output_file)
            except IOError as e:
                raise CommandError(e.message)
            else:
                self.stdout.write('%s > %s' % (input_file, output_file))
