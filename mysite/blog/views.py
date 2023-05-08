from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage


# представления списка опубликованных постов на странице
def post_list(request):
    # posts = Post.published.all()

    # Постраничная разбивка с 3 постами на страницу
    post_list = Post.published.all()
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        # Если page_number находится вне диапазона, то
        # выдать последнюю страницу
        posts = paginator.page(paginator.num_pages)

    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})


# # представление одиночного поста (s1). Открыть пост по id
# def post_detail(request, id):
#     # try:
#     #     post = Post.published.get(id=id)

#     # # исключение Http404, чтобы вернуть ошибку HTTP с кодом 
#     # # состояния, равным 404, если возникает исключение DoesNotExist, 
#     # # то есть модель не существует, поскольку результат не найден.
#     # except Post.DoesNotExist:
#     #     raise Http404("No post found.")

#     # тоже самое, но с использованием ф-ции сокращенного доступа get_object_or_404
#     post = get_object_or_404(Post,
#                              id=id,
#                              status=Post.Status.PUBLISHED)
    
#     return render(request,
#                   'blog/post/detail.html',
#                   {'post': post})


# представление одиночного поста (s2) с использованием /blog/yeat/month/day/slug/
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})

