from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    return d.get(key)

@register.filter
def mul(value, arg):
    try:
        res = float(value) * float(arg)
        return f"{res:.2f}".rstrip('0').rstrip('.')
    except (ValueError, TypeError):
        return 0
