Django bootstrap styleguide
===========================

Mirumee's style guide and mockup app for Django projects based on Boostrap


For contributors
----------------


Project preparation

```console
# clone the repository with submodules
$ git clone --recursive https://github.com/mirumee/django-bootstrap-styleguide.git
# go into repository
$ cd django-bootstrap-styleguide
# setup project in development mode
$ python setup.py develop
# build bootstrap templates and copy static files
$ python setup.py build_bootstrap
```

Remember to re-run `python setup.py build_bootstrap` if you change any `jekyll` templates.
