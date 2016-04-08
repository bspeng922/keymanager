# -*- coding: utf-8 -*-

import logging

from django.conf import settings
from django import forms
from django.utils.translation import gettext_lazy as _


LOG = logging.getLogger(__file__)


class KeyForm(forms.Form):
    version = forms.ChoiceField(label=_("Version"))
    srv_limit = forms.ChoiceField(label=_("Server Limit"),
                                  required=False)
    cpu_limit = forms.IntegerField(label=_("CPU Limit"),
                                   min_value=1)
    company = forms.CharField(label=_("Company"),
                              max_length=200,
                              required=False)

    def __init__(self, *args, **kwargs):
        super(KeyForm, self).__init__(*args, **kwargs)
        self.fields['version'].choices = settings.VERSIONS
        # self.fields['srv_limit'].initial = 3
        self.fields['srv_limit'].choices = settings.SERVER_LIMIT
        self.fields['cpu_limit'].initial = 6


class KeyCreateForm(KeyForm):
    count = forms.IntegerField(label=_("Count"), min_value=1, max_value=100)

    def __init__(self, *args, **kwargs):
        super(KeyCreateForm, self).__init__(*args, **kwargs)
        self.fields['count'].initial = 1


