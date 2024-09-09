from django import template
from ..models import Post_djb

register = template.Library()


@register.simple_tag
def total_posts():
    return Post_djb.objects.count()