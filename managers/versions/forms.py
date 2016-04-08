from django.utils.translation import gettext_lazy as _
from django import forms
from django.conf import settings


class VersionForm(forms.Form):
    # name = forms.CharField(label=_("Name"), max_length=20)
    name = forms.ChoiceField(label=_("Name"))
    cpu_limit = forms.IntegerField(label=_("CPU Limit"), min_value=1)
    server_limit = forms.IntegerField(label=_("Server Limit"), min_value=-1)

    def __init__(self, *args, **kwargs):
        super(VersionForm, self).__init__(*args, **kwargs)

        self.fields['name'].choices = settings.VERSIONS
