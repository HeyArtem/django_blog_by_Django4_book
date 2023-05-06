from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

"""
Простой блог

"""

# конкретно-прикладной менеджер для модели Post, возвращает опубликованные посты 
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
        .filter(status=Post.Status.PUBLISHED)
    

class Post(models.Model):

    # В постах будут использоваться статусы Draft (Черновик) и Published(Опубликован).
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

        
    title = models.CharField(max_length=250)
    """
    slug: поле SlugField, которое транслируется в столбец VARCHAR в базе дан-
    ных SQL. Слаг – это короткая метка, содержащая только буквы, цифры,
    знаки подчеркивания или дефисы. мы будем использовать поле slug для формиро-
    вания красивых и дружественных для поисковой оптимизации URL-
    адресов постов блога;"""
    slug = models.SlugField(max_length=250)

    """
    взаимосвязь многие-к-одному, означающую, что каждый пост написан пользователем и пользо-
    ватель может написать любое число постов.
    related_name, чтобы указывать имя обратной связи, от User к Post. Такой подход позволит легко обращаться к связанным объектам из
    объекта User, используя обозначение user.blog_posts."""
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    # для хранения даты и времени публикации поста
    publish = models.DateTimeField(default=timezone.now)
    # для хранения даты и времени создания поста.
    created = models.DateTimeField(auto_now_add=True)
    # для хранения последней даты и времени обновления поста.
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    
    """
    Первый объявленный в модели менеджер становится менеджером, ко-
    торый используется по умолчанию. Для того чтобы указать другой такой
    менеджер, применяется Meta-атрибут default_manager_name. Если менеджер
    в модели не определен, то Django автоматически создает для нее стандарт-
    ный менеджер objects. Если в своей модели вы объявляете какие-либо менед-
    жеры, но также хотите сохранить менеджер objects, то вы должны добавить
    его в свою модель явным образом. В приведенном выше исходном коде мы
    добавили в модель Post стандартный менеджер objects и конкретно-при-
    кладной менеджер published.
    """
    objects = models.Manager() # менеджер, применяемый по умолчанию
    published = PublishedManager() # конкретно-прикладной менеджер


    """
    ordering-сортировать результаты по полю publish. 
    Указанный порядок будет применяться по умолчанию для запросов к базе данных, когда в запросе не
    указан конкретный порядок. 
    Убывающий порядок задается с по мощью дефиса перед именем поля: -publish. 
    По умолчанию посты будут возвращаться в обратном хронологическом порядке.
    """        
    class Meta:
        ordering = ['-publish']

        """
        Индекс повысит производительность запросов
        по полю publish, а перед именем поля применен дефис, чтобы определить
        индекс в убывающем порядке. Создание этого индекса будет вставляться
        в миграции базы данных
        """
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title
