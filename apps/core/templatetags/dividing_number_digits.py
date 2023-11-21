from django import template

register = template.Library()

@register.filter
def dividing_number_digits(value):
    return f'{value:,}'.replace(',', ' ')