from django import template
from django.utils.safestring import mark_safe
import markdown
register = template.Library()


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text, extensions=['tables', 'def_list']))


@register.filter
def first_val_in_dict(dictionary: dict):
    for key in dictionary.keys():
        return dictionary[key]
    return None


@register.filter
def first_key_in_dict(dictionary: dict):
    for key in dictionary.keys():
        return key
    return None
