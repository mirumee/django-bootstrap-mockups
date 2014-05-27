from collections import defaultdict
from django import template
from django import forms
from django.forms.forms import pretty_name
from django.utils.text import slugify

register = template.Library()


def generate_choices_from_list(word_list):
    word_list = word_list or ['lorem', 'ipsum', 'dolor', 'sit amet', 'consectetur']
    return [(slugify(unicode(word)), pretty_name(word)) for word in word_list]


FIELD_TYPE_MAPPING = defaultdict(lambda: (forms.CharField, None), {
    'number': (forms.IntegerField, None),
    'date': (forms.DateField, None),
    'datetime': (forms.DateTimeField, None),
    'select': (forms.ChoiceField, None),
    'multi_select': (forms.MultipleChoiceField, None),
    'text': (forms.CharField, forms.Textarea),
    'url': (forms.URLField, None),
    'checkbox': (forms.MultipleChoiceField, forms.CheckboxSelectMultiple),
    'radio': (forms.ChoiceField, forms.RadioSelect),
    'file': (forms.FileField, None)
})


@register.simple_tag(takes_context=True)
def prepare_field(context, field_name, **kwargs):
    form = context['form']
    field_type = kwargs.pop('type', None)
    if field_type in ['select', 'radio', 'multi_select', 'checkbox']:
        choices = kwargs.get('choices')
        choices_list = choices.split(',') if choices else []
        kwargs['choices'] = generate_choices_from_list(choices_list)
        if field_type in ['multi_select', 'checkbox']:
            initial = kwargs.get('initial')
            kwargs['initial'] = initial.split(',') if initial else None
    kwargs['field_class'], kwargs['widget'] = FIELD_TYPE_MAPPING[field_type]
    form.fields_kwargs[field_name] = kwargs
    return ''


@register.simple_tag(takes_context=True)
def prepare_errors(context, **kwargs):
    form = context['form']
    force_show = kwargs.pop('force_show', False)
    if force_show:
        form.data = {}
    for name, errors in kwargs.items():
        for error in errors.split(','):
            form.errors[name].append(error)
    return ''
