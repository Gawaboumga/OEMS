from django import template

import bleach
from markdownx import utils

register = template.Library()


@register.filter
def show_markdown(text):
    allowed_attributes = bleach.sanitizer.ALLOWED_TAGS
    allowed_attributes += ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']
    return bleach.clean(utils.markdownify(text), tags=allowed_attributes, attributes=bleach.sanitizer.ALLOWED_ATTRIBUTES)

