from django.conf import settings
from django import template
from django.utils.translation import ugettext_lazy as _


register = template.Library()


class SiteBrandingNode(template.Node):
    def render(self, context):
        return getattr(settings, "SITE_BRANDING", _("Key Manager"))


@register.tag
def site_branding(parser, token):
    return SiteBrandingNode()

