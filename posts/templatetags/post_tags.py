from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
from django.conf import settings

import redis

r = redis.StrictRedis(host=settings.REDIS_HOST,
                      port=settings.REDIS_PORT,
                      db=settings.REDIS_DB)

register = template.Library()

from ..models import Post

@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('posts/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-created')[:count]
    return {'latest_posts': latest_posts}


@register.assignment_tag
def get_most_commented_posts(count=20):
    most_commented = Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
    for post in most_commented:
    	post.total_views = r.get('post:{}:views'.format(post.id))
    return most_commented

    	

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
