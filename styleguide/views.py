from collections import defaultdict

from django.contrib import messages
from django.http import Http404
from django.template.base import TemplateDoesNotExist
from django.template.loader import find_template
from django.template.response import TemplateResponse

from .forms import FormFactory
from . import get_context


def add_messages_from_request(request):
    data = request.POST or request.GET
    for name, message in data.items():
        if name.endswith('_message'):
            message_type = getattr(messages, name[:-8].upper(), messages.INFO)
            messages.add_message(request, message_type, message)


def get_template(request, name, is_mockup=False):
    context = get_context()
    context['template_name'] = name
    if is_mockup:
        add_messages_from_request(request)
        data = request.POST or request.GET
        data = dict(
            (key, value) for key, value in data.copy().items()
            if not key.endswith('_message'))
        context['form'] = FormFactory(data=data or None)
        template = 'styleguide/mockups/%s.html' % (name,)
    else:
        template = 'bootstrap_docs/%s.html' % (name,)
    try:
        find_template(template)
    except TemplateDoesNotExist:
        raise Http404(template)
    return TemplateResponse(request, template, context)
