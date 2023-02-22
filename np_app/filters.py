from django_filters import FilterSet, DateFilter, CharFilter, ModelChoiceFilter
from .models import Post, Author, Category
from django import forms

class PostFilter(FilterSet):
#   class Meta:
#       model = Post
#       fields = {
#           'header_post':['icontains'],
#           'author': ['exact'],
#           'time_create_post': ['date__gte']
#       }
    search_title = CharFilter(
        field_name = 'header_post',
        label = 'Название статьи',
        lookup_expr = 'icontains'
    )
    search_author = ModelChoiceFilter(
        empty_label = 'Все авторы',
        field_name = 'author',
        label = 'Автор',
        queryset = Author.objects.all()
    )
    search_category = ModelChoiceFilter(
        empty_label = 'Все категории',
        field_name = 'category',
        label = 'Категория',
        queryset = Category.objects.all()
    )

    post_date__gt = DateFilter(
        field_name = 'time_create_post',
        widget = forms.DateInput(attrs = {'type': 'date'}),
        label = 'Дата',
        lookup_expr = 'date__gte'
    )