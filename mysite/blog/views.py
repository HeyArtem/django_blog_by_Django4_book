from django.shortcuts import render, get_object_or_404
from .models import Post
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage
from django.views.generic import ListView
from .forms import EmailPostForm
from django.core.mail import send_mail


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


class PostListView(ListView):
    '''
    представление списка постов
    на основе класса
    '''

    # атрибут queryset используется для того, чтобы иметь конкретно-при-
    # кладной набор запросов QuerySet, не извлекая все объекты. Вместо
    # определения атрибута queryset мы могли бы указать model=Post, и Django
    # сформировал бы для нас типовой набор запросов Post.objects.all()
    queryset = Post.published.all()
    
    # контекстная переменная posts используется для результатов запроса.
    # Если не указано имя контекстного объекта context_object_name, то по
    # умолчанию используется переменная object_list;
    context_object_name = 'posts'
    
    # в атрибуте paginate_by задается постраничная разбивка результатов
    # с возвратом трех объектов на страницу;
    paginate_by = 3

    # конкретно-прикладной шаблон используется для прорисовки страницы
    # шаблоном template_name. Если шаблон не задан, то по умолчанию List-
    # View будет использовать blog/post_list.html.
    template_name = 'blog/post/list.html'


# Отправка электронных писем
def post_share(request, post_id):
    # Извлечь пост по идентификатору id
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    
    '''
    мы объявили переменную sent с изна-
    чальным значением False. Мы задаем этой переменной значение True после от-
    правки электронного письма. Позже мы будем использовать переменную sent
    в шаблоне отображения сообщения об успехе при успешной передаче формы.
    Поскольку ссылка на пост должна вставляться в электронное письмо, мы
    получаем абсолютный путь к посту, используя его метод get_absolute_url().
    Мы используем этот путь на входе в метод request.build_absolute_uri(), чтобы
    сформировать полный URL-адрес, включая HTTP-схему и хост-имя (hostname).
    Мы создаем тему и текст сообщения электронного письма, используя очи-
    щенные данные валидированной формы. Наконец, мы отправляем электрон-
    ное письмо на адрес электронной почты, указанный в поле to (Кому) формы.
    '''
    sent = False

    if request.method == 'POST':
        # Форма была передана на обработку
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['Имя']} recommends you read " \
                f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                f"{cd['Имя']}\'s comments: {cd['Комментарий']}"
            send_mail = (subject, message, 'your_accoun@gmail.com',
                         [cd['Получатель']])
            
            sent = True
            
    else:
        form = EmailPostForm()
    
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})