#! /usr/bin/env python
from subprocess import check_call
from setuptools import setup, find_packages
from setuptools.command.develop import develop


class PrepareStaticAndTemplatesCommand(develop):

    @staticmethod
    def initialize_git_submodules():
        check_call(['git', 'submodule', 'init'])
        check_call(['git', 'submodule', 'update'])

    @staticmethod
    def build_bootstrap_docs_templates():
        check_call(['(cd jekyll/; jekyll build)'], shell=True)

    @staticmethod
    def copy_bootstrap_docs_static_files():
        # todo: windows compatibility
        static_path = 'styleguide/static/bootstrap_docs'
        check_call(['mkdir', '-p', static_path])
        check_call(['cp', '-r', 'bootstrap/docs/dist', static_path])
        check_call(['cp', '-r', 'bootstrap/docs/assets', static_path])

    def run(self):
        self.initialize_git_submodules()
        self.build_bootstrap_docs_templates()
        self.copy_bootstrap_docs_statics()
        develop.run(self)


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
        'django-bootstrap3>=4.4.1'
    ],
    classifiers=CLASSIFIERS,
    cmdclass={
        'develop': PrepareStaticAndTemplatesCommand
    }
)
