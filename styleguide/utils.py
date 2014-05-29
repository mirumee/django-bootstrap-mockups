from os import path, makedirs

from sass import compile_file


def compile_scss_file(input_file, output_file):
    if not path.exists(input_file):
        raise IOError('%s does not exist' % (input_file,))
    output_path = path.split(output_file)[0]
    if not path.exists(output_path):
        makedirs(output_path)
    with open(output_file, 'w') as css_file:
        css_file.write(compile_file(input_file))
