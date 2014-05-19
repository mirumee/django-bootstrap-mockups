from django import forms


class BasicExampleForm(forms.Form):

    email_address = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    file_input = forms.FileField(
        help_text='Example block-level help text here.')
    check_me_out = forms.ChoiceField(widget=forms.CheckboxInput())


class ExampleForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    remember_me = forms.ChoiceField(widget=forms.CheckboxInput())
