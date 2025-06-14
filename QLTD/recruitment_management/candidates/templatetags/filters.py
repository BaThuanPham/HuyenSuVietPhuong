import os
from django import template

register = template.Library()

@register.filter
def basename(value):
    return os.path.basename(value)
@register.filter

def endswith(value, arg):
    if not isinstance(value, str):
        value = str(value)
    return value.lower().endswith(arg.lower())