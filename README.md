#Django bootstrap styleguide#

Mirumee's style guide and mockup app for Django projects based on Boostrap. This tool is meant for frontend developers it uses both `less` or `sass` files.

##What for?##

This app provides three minor features.

###Style guide###

This application uses Bootstrap documentation as a style guide for your project. All new developers can easily go to the style guide page and learn what components they can use. Additionally using django static serve functionality developer can easily extend Bootstrap files without editing them!

Project and styleguide are using the same styles, in this approach you can check in one place how new styles act with bootstrap.

###Mockups###

Frontend developer can easily start working on layouts without any help from backend developers. All templates from `templates/styleguide/mockups` are visible  in the mockup view. So you don't need to create any views or urls.

From our experience we knew that forms templates provided by frontend developers don't work well with python form objects. For this case we provided mocked `form` object. In other words frontend developer can easily get field object and work on it. Template created in that way won't need any improvment from backend developer.

Frontend developer can easily mockup flow as well by adding links or forms. You can set django messages as well.

###Compiling css###

By using `./manage.py watch` you can turn on watcher for `less` or `sass` files. If you are using `sass` in your project you won't need to use any addidionaly tools. Application uses `libsass` python wrapper and compile `css` in pure python environment.

##For contributors##

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

