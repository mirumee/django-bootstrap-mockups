import importlib

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

STYLE_GUIDE_CONFIG = {
    'type': 'less',
    'context': {}
}

STYLE_GUIDE_CONFIG.update(getattr(settings, 'STYLE_GUIDE_CONFIG', {}))


def get_context():
    context = STYLE_GUIDE_CONFIG['context']
    if isinstance(context, str):
        context = importlib.import_module(context)
    if not isinstance(context, dict):
        raise ImproperlyConfigured('Style guide context must be a dict object')
    context = context.copy()
    context['config'] = STYLE_GUIDE_CONFIG
    return context
