Django bootstrap styleguide
===========================

Mirumee's style guide and mockup app for Django projects based on Boostrap


For contributors
----------------

Start by cloning the repository (`--recursive` also clones the required submodules):

```
$ git clone --recursive https://github.com/mirumee/django-bootstrap-styleguide.git
```

Then enter the newly cloned directory and install the module in development mode:

```
$ cd django-bootstrap-styleguide
$ python setup.py develop
```

Finally build the Bootstrap templates and copy static files:

```
$ python setup.py build_bootstrap
```

Remember to re-run the build step if you edit `jekyll` templates or update the `bootstrap` submodule to a newer version.
