from django.urls import path
from . import views


# определяется именное пространство
app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),

    # открыть пост по id
    # path('<int:id>/', views.post_detail, name='post_detail'),

    # чтобы использовать дату публикации и слаг для URL-адреса
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail'),
]
