from django.http import Http404
from django.template.base import TemplateDoesNotExist
from django.template.loader import find_template
from django.template.response import TemplateResponse

from .forms import BasicExampleForm, ExampleForm
from . import get_context


def get_template(request, name, is_mockup=False):
    context = get_context()
    context['template_name'] = name
    if is_mockup:
        template = 'styleguide/mockups/%s.html' % (name,)
    else:
        template = 'bootstrap_docs/%s.html' % (name,)
        context['forms'] = {
            'basic': BasicExampleForm(),
            'small': ExampleForm()
        }
    try:
        find_template(template)
    except TemplateDoesNotExist:
        raise Http404(template)
    return TemplateResponse(request, template, context)
