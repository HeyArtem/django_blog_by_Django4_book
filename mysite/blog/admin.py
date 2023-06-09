from django.contrib import admin
from .models import Post, Comment


# admin.site.register(Post)

"""
В этот класс можно вставлять информацию о том, как показывать модель на сайте и как с ней взаимодействовать.
Атрибут list_display позволяет задавать поля модели, которые вы хотите показывать на странице списка объектов администрирования. 
Декоратор @admin.register() выполняет ту же функцию, что и функция admin.site.register()
"""
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status', 'created',]

    # правая панель позволяет фильтровать результаты по полям, включенным в атрибут list_filter
    list_filter = ['status', 'created', 'publish', 'author']

    # строка поиска
    search_fields = ['title', 'body']

    # slug заполняется автоматически (при заполнении поста)
    prepopulated_fields = {'slug': ('title',)}

    # поле author отображается поисковым виджетом (при заполнении поста)
    raw_id_fields = ['author']

    # навигационные ссылки для навигации по иерархии дат
    date_hierarchy = 'publish'

    # по умолчанию упорядочены по столбцам STATUS (Статус) и PUBLISH (Опубликован)
    ordering = ['status', 'publish']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']



