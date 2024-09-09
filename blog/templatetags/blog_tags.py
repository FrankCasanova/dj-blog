from django import template
from ..models import Post_djb
from django.db.models import Count

register = template.Library()


@register.simple_tag
def total_posts():
    return Post_djb.objects.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post_djb.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    return Post_djb.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
