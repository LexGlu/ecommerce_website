from django import template

register = template.Library()


@register.filter(name='currency')
def currency(number):
    return f'₴ {number:,}'.replace(',', ' ')


@register.filter(name='phone_format')
def phone_format(number):
    number = str(number)
    return f'{number[:3]} {number[3:6]} {number[6:8]} {number[8:10]} {number[10:]}'
