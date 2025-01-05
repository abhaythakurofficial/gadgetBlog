from django import template

register = template.Library()

@register.filter
def dict_has_key(dictionary, key):
    """Check if the key exists in the dictionary."""
    return key in dictionary

@register.filter
def dict_get_value(dictionary, key):
    """Get the value for a given key in the dictionary."""
    return dictionary.get(key, [])
