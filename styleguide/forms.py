from collections import defaultdict

from django import forms
from django.forms.forms import BoundField, pretty_name
from django.template import TemplateSyntaxError
from django.utils.text import slugify
from faker import Faker

fake = Faker()


class FieldMock(object):

    fake_words = fake.words(6)

    def __init__(self, field_class):
        self.field_class = field_class
        self.field_kwargs = {'help_text': None, 'required': False, 'initial': None}
        self.form = forms.Form()
        if issubclass(field_class, forms.ChoiceField):
            self.field_kwargs['choices'] = [(slugify(unicode(word)), pretty_name(word)) for word in self.fake_words[:4]]

    def __getattr__(self, name):
        args = name.split('__')
        name = args.pop(0)
        if name == 'help_text':
            self.field_kwargs['help_text'] = args[0] if args else self.fake_words[4]
        elif name == 'required':
            self.field_kwargs['required'] = True
        elif name == 'initial':
            if len(args) == 1:
                initial = args[0]
            elif len(args) > 1:
                initial = args
            else:
                initial = self.fake_words[5]
            self.field_kwargs['initial'] = initial
        elif name == 'choices':
            choices = [(slugify(unicode(choice)), pretty_name(choice)) for choice in args]
            if choices:
                self.field_kwargs['choices'] = choices
        else:
            field = self.field_class(**self.field_kwargs)
            return BoundField(form=self.form, field=field, name=name)
        return self


class FormFactory(object):

    fields_kwargs = None

    def __init__(self):
        self.fields_kwargs = defaultdict(dict)
        self.form = forms.Form()

    def non_field_errors(self):
        return self.form.non_field_errors()

    def __getitem__(self, name):
        kwargs = self.fields_kwargs[name]
        field_class = kwargs.pop('field_class', forms.CharField)
        try:
            bound_field = BoundField(form=self.form, field=field_class(**kwargs), name=name)
        except TypeError:
            raise TemplateSyntaxError('Bad keywords in %s field' % (name,))
        else:
            return bound_field
