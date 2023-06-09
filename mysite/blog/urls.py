from django.urls import path
from . import views
from .feeds import LatestPostFeed


# определяется именное пространство
app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),

    # представление на основе класса
#     path('', views.PostListView.as_view(), name='post_list'),

    # открыть пост по id
    # path('<int:id>/', views.post_detail, name='post_detail'),

    # чтобы использовать дату публикации и слаг для URL-адреса
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail'),
    
    # Отправка электронных писем
    path('<int:post_id>/share/',
         views.post_share, name='post_share'),

     # комментирование постов
     path('<int:post_id>/comment/',
          views.post_comment, name='post_comment'),

    # СОЗДАНИЕ НОВОСТНЫХ ЛЕНТ
     path('feed/', LatestPostFeed(), name='post_feed'),

     # ПРЕДСТАВЛЕНИЯ ПОИСКА
     path('search/', views.post_search, name='post_search'),
    
]
