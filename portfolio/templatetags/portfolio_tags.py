from django import template

register = template.Library()


@register.filter
def split_commas(value):
    """Split a comma-separated string into a list."""
    if not value:
        return []
    return [item.strip() for item in value.split(',') if item.strip()]
