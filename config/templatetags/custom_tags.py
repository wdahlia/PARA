from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
from django.utils import translation
from django.conf import settings

register = template.Library()


@register.filter
def price_view(price):
    language_code = translation.get_language()
    return "%s" % (intcomma(price))
