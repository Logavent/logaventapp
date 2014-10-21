from django import template

register = template.Library()

@register.filter
def times(value, i):
  return value*i