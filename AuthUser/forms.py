"""
Forms for the AuthUser app.

Includes customizations for the Django authentication form.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CustomLoginForm(AuthenticationForm):
    """
    Custom login form that applies Tailwind CSS classes for styling.

    Inherits from Django's built-in `AuthenticationForm` and overrides the
    default widget attributes for the username and password fields.
    """

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'h-[24px] border-2 rounded-sm border-slate-300 '
                     'focus:outline-none focus:border-slate-700 px-2 text-sm',
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'h-[24px] border-2 rounded-sm border-slate-300 '
                     'focus:outline-none focus:border-slate-700 px-2 text-sm',
        })
    )
