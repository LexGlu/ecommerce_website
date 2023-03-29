from django import forms

email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
email_msg = 'Enter a valid email address (e.g. example@mail.com}'


class LoginForm(forms.Form):
    """Form for the user login."""

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({'placeholder': 'Email', 'id': 'your_email', 'type': 'email',
                                                  'name': 'your_email',
                                                  'pattern': email_pattern,
                                                  'title': email_msg
                                                  })
        self.fields['password'].widget.attrs.update({'placeholder': 'Password', 'id': 'your_pass', 'type': 'password',
                                                     'name': 'your_pass',
                                                     })
