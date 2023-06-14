from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity


# представления списка опубликованных постов на странице
def post_list(request, tag_slug=None):
    # posts = Post.published.all()
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    # Постраничная разбивка с 3 постами на страницу    
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
                  {'posts': posts,
                   'tag': tag})


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
    
    # Список активных комментариев к этому посту
    comments = post.comments.filter(active=True)

    # Форма для комментирования пользователями
    form = CommentForm()   

    # Список схожих постов по тегам
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                                    .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                    .order_by('-same_tags', '-publish')[:4]
    
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form,
                   'similar_posts': similar_posts})


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


# комментирование постов
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post,
                             id=post_id, 
                             status=Post.Status.PUBLISHED)
    comment = None
    # Комментарий был отправлен
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Создать объект класса Comment, не сохраняя его в базе данных
        comment = form.save(commit=False)
        # Назначить пост комментарию
        comment.post = post
        # Сохранить комментарий в базе данных
        comment.save()
    
    return render(request, 'blog/post/comment.html',
                  {'post': post,
                   'form': form,
                   'comment': comment})

# форма представления для поиска постов
'''
Поле запроса будет использоваться для того, чтобы давать пользователям
возможность вводить поисковые запросы.
Для проверки того, что форма была передана на обработку, в сло-
варе request.GET отыскивается параметр query. Форма отправляется методом
GET, а не методом POST, чтобы результирующий URL-адрес содержал пара-
метр query и им было легко делиться. После передачи формы на обработку
создается ее экземпляр, используя переданные данные GET, и проверяется
валидность данных формы. Если форма валидна, то с по мощью конкретно-
прикладного экземпляра SearchVector, сформированного с использованием
полей title и body, выполняется поиск опубликованных постов.
'''
def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']            
            results = Post.published.annotate(
                similarity=TrigramSimilarity('title', query),                
            ).filter(similarity__gt=0.1).order_by('-similarity')

    return render(request,
                  'blog/post/search.html',
                  {'form': form,
                   'query': query,
                   'results': results})
