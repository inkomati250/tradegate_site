from django import template

register = template.Library()


@register.filter
def get_item(mapping, key):
    """Look up a dictionary value by key in a template."""
    if not mapping:
        return None
    return mapping.get(key)


@register.filter
def rgb_channels(value, fallback="7 17 31"):
    """'#D6B36A' -> '214 179 106' for CSS variables used by the compiled stylesheet."""
    value = (value or "").strip().lstrip("#")
    if len(value) == 3:
        value = "".join(c * 2 for c in value)
    try:
        return " ".join(str(int(value[i:i + 2], 16)) for i in (0, 2, 4)) if len(value) == 6 else fallback
    except ValueError:
        return fallback
