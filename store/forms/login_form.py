from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class LoginForm(forms.Form):
    """Form for the user login."""

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Sign in', css_class='btn-success'))

        self.fields['email'].widget.attrs.update({'placeholder': 'alex.turner@mail.com', 'class': 'example-label'})
        self.fields['password'].widget.attrs.update({'placeholder': '********', 'class': 'example-label'})
