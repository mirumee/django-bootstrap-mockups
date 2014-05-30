import importlib
from os import path

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

STYLE_GUIDE_CONFIG = {
    'title': 'Bootstrap',
    'type': 'less',
    'context': {},
    'style_files': None,
    'css_root': None
}

if not settings.STATIC_ROOT:
    raise ImproperlyConfigured('Stylegude requires STATIC_ROOT')

STYLE_GUIDE_CONFIG.update(getattr(settings, 'STYLE_GUIDE_CONFIG', {}))

if not STYLE_GUIDE_CONFIG['css_root']:
    raise ImproperlyConfigured(
        'You did not set css root path in the STYLE_GUIDE_CONFIG')

if not STYLE_GUIDE_CONFIG['style_files']:
    style_type = STYLE_GUIDE_CONFIG['type']
    input_file = 'sass/style.scss' if style_type == 'sass' else 'less/style.less'
    STYLE_GUIDE_CONFIG['style_files'] = ((input_file, 'css/style.css'),)


def get_context():
    context = STYLE_GUIDE_CONFIG['context']
    if isinstance(context, str):
        context_module = importlib.import_module(context)
        if not hasattr(context_module, 'context'):
            raise ImproperlyConfigured('%s module should contains context dict' % context)
        context = context_module.context
    if not isinstance(context, dict):
        raise ImproperlyConfigured('Style guide context must be a dict object')
    context = context.copy()
    context['config'] = STYLE_GUIDE_CONFIG
    return context
