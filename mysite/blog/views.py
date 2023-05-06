from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404


# представления списка опубликованных постов на странице
def post_list(request):
    posts = Post.published.all()
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})


# представление одиночного поста
def post_detail(request, id):
    # try:
    #     post = Post.published.get(id=id)

    # # исключение Http404, чтобы вернуть ошибку HTTP с кодом 
    # # состояния, равным 404, если возникает исключение DoesNotExist, 
    # # то есть модель не существует, поскольку результат не найден.
    # except Post.DoesNotExist:
    #     raise Http404("No post found.")

    # тоже самое, но с использованием ф-ции сокращенного доступа get_object_or_404
    post = get_object_or_404(Post,
                             id=id,
                             status=Post.Status.PUBLISHED)
    
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})

