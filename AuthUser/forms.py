from django import forms
from django.contrib.auth.forms import AuthenticationForm


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'h-[24px] border-2 rounded-sm border-slate-300 focus:outline-none focus:border-slate-700 px-2 text-sm',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'h-[24px] border-2 rounded-sm border-slate-300 focus:outline-none focus:border-slate-700 px-2 text-sm',
        })
    )
