from django.conf.urls import patterns, url

from .views import get_template

urlpatterns = patterns(
    '',
    url(r'^$', get_template, {'name': 'index'}, name='index'),
    url(r'^(?P<name>[a-z0-9-]+)\.html$', get_template, {'is_mockup': True}, name='mockup'),
    url(r'^(?P<name>[a-z0-9-]+)$', get_template, name='bootstrap'),
)
