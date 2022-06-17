from django import template

register = template.Library()

@register.filter()
def range(min=0):
    return range(min)