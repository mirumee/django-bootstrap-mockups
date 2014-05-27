import importlib
from os import path

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

STYLE_GUIDE_CONFIG = {
    'title': 'Bootstrap',
    'type': 'less',
    'context': {},
    'input_file': None,
    'output_file': None
}

STYLE_GUIDE_CONFIG.update(getattr(settings, 'STYLE_GUIDE_CONFIG', {}))

if not STYLE_GUIDE_CONFIG['input_file']:
    style_type = STYLE_GUIDE_CONFIG['type']
    name = 'style.scss' if style_type == 'sass' else 'style.less'
    STYLE_GUIDE_CONFIG['input_file'] = path.join(
        settings.STATIC_ROOT, style_type, name)

if not STYLE_GUIDE_CONFIG['output_file']:
    STYLE_GUIDE_CONFIG['output_file'] = path.join(
        settings.STATIC_ROOT, 'css', 'style.css')


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
