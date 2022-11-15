from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter(name='split')
@stringfilter
def split(value, key):
    """
        Returns the value turned into a list.
    """
    return value.split(key)