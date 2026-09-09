from django import template

register = template.Library()


@register.filter
def price_format(value):
    if not value:
        return ""

    try:
        return f"{int(value):,}".replace(",", " ")
    except (ValueError, TypeError):
        return value