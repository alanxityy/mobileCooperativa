from django import template

register = template.Library()

@register.filter
def brl(value):
    try:
        v = float(value)
    except (TypeError, ValueError):
        return value
    # formatação simples: R$ 1.234,56
    s = f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {s}"
