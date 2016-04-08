# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import gettext_lazy as _


class UserForm(forms.Form):
    username = forms.CharField(label=_("User Name"))
    email = forms.EmailField(label=_("Email"), required=False)


class UserCreateForm(UserForm):
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput(render_value=False))


class UserEditForm(UserForm):
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput(render_value=False),
                               required=False)

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True


class LoginForm(forms.Form):
    username = forms.CharField(label=_("User Name"),
               widget=forms.TextInput(attrs={"autofocus": "autofocus"}))
    password = forms.CharField(label=_("Password"),
               widget=forms.PasswordInput(render_value=False))