from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown


register = template.Library()

# простой шаблонный тег, который возвращает число опубликованных в блоге постов.
@register.simple_tag
def total_posts():
    return Post.published.count()

# тег, чтобы отображать последние посты на боковой панели блога
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

# чтобы отображать посты с наибольшим числом комментариев
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]

# для поддержки синтаксиса Markdown
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
