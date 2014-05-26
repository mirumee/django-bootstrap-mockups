#! /usr/bin/env python
import os
from contextlib import contextmanager
from subprocess import check_call
from setuptools import setup, find_packages, Command
from shutil import copytree, rmtree


@contextmanager
def cwd(path):
    old_path = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_path)


class PrepareStaticAndTemplatesCommand(Command):

    STATIC_DIR = 'styleguide/static'
    description = 'Copy static data and compile bootstrap docs'
    user_options = []

    def build_bootstrap_docs_templates(self):
        with cwd('jekyll'):
            check_call(['jekyll', 'build'])

    def copy_bootstrap_docs_static_files(self):
        static_docs_path = os.path.join(self.STATIC_DIR, 'bootstrap_docs')
        if os.path.exists(static_docs_path):
            rmtree(static_docs_path)
        dist_path = os.path.join(static_docs_path, 'dist')
        copytree('bootstrap/docs/dist', dist_path)
        assets_path = os.path.join(static_docs_path, 'assets')
        copytree('bootstrap/docs/assets', assets_path)

    def copy_bootstrap_less_files_to_static(self):
        less_dir = os.path.join(self.STATIC_DIR, 'less/bootstrap')
        if os.path.exists(less_dir):
            rmtree(less_dir)
        copytree('bootstrap/less', less_dir)

    def copy_bootstrap_sass_files_to_static(self):
        less_dir = os.path.join(self.STATIC_DIR, 'sass/bootstrap')
        if os.path.exists(less_dir):
            rmtree(less_dir)
        copytree('bootstrap-sass/vendor/assets/stylesheets/bootstrap', less_dir)

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print('Build bootstrap templates')
        self.build_bootstrap_docs_templates()
        print('Copy bootstrap docs static files')
        self.copy_bootstrap_docs_static_files()
        print('Copy bootstrap less files')
        self.copy_bootstrap_less_files_to_static()
        print('Copy bootstrap sass files')
        self.copy_bootstrap_sass_files_to_static()


CLASSIFIERS = [
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.2',
    'Programming Language :: Python :: 3.3',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
    'Topic :: Software Development :: Libraries :: Python Modules']

setup(
    name='django-bootstrap-styleguide',
    author='Mirumee Software',
    author_email='hello@mirumee.com',
    description='Web style guide based on bootstrap',
    license='BSD',
    version='0.1.0a0',
    url='https://github.com/mirumee/django-bootstrap-styleguide',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django>=1.6.5',
        'django-bootstrap3>=4.4.1',
    ],
    classifiers=CLASSIFIERS,
    cmdclass={
        'build_bootstrap': PrepareStaticAndTemplatesCommand
    }
)
