from collections import defaultdict

from django import forms
from django.core.exceptions import ValidationError
from django.forms.util import ErrorList
from django.forms.forms import BoundField, NON_FIELD_ERRORS
from django.template import TemplateSyntaxError


class FormFactory(object):

    fields_kwargs = None
    error_class = ErrorList
    auto_id = None

    def __init__(self, data=None):
        self.data = data
        self.fields_kwargs = defaultdict(dict)
        self.errors = defaultdict(self.error_class)
        self.initial = {}
        self.files = {}

    def non_field_errors(self):
        return self.errors[NON_FIELD_ERRORS]

    @property
    def is_bound(self):
        return self.data is not None

    def add_prefix(self, field_name):
        return field_name

    def add_initial_prefix(self, field_name):
        return 'initial-%s' % field_name

    def __getitem__(self, name):
        if name == 'non_field_errors':
            raise KeyError()
        kwargs = self.fields_kwargs[name]
        field_class = kwargs.pop('field_class', forms.CharField)
        field = field_class(**kwargs)
        if self.is_bound:
            value = field.widget.value_from_datadict(self.data, self.files, name)
            try:
                field.clean(value)
            except ValidationError as e:
                self.errors[name] = self.error_class(e.messages)
        try:
            bound_field = BoundField(form=self, field=field, name=name)
        except TypeError:
            raise TemplateSyntaxError('Bad keywords in %s field' % (name,))
        else:
            return bound_field
