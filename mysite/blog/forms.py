from django import forms
from .models import Comment


class EmailPostForm(forms.Form):
    # для имени человека, отправляющего пост
    Имя = forms.CharField(max_length=25)
    
    # адрес электронной почты человека, отправившего рекомендуемый пост
    email = forms.EmailField()
    Получатель = forms.EmailField()

    # для комментариев, которые будут вставляться в электронное письмо с рекомендуе-
    # мым постом. Это поле сделано опциональным путем установки required
    # равным значению False, при этом был задан конкретно-прикладной
    # виджет прорисовки поля
    Комментарий = forms.CharField(required=False,
                               widget=forms.Textarea)


# комментирование постов
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


# форма представления для поиска постов
class SearchForm(forms.Form):
    query = forms.CharField()
    