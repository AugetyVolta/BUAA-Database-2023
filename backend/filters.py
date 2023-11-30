import django_filters
from .models import Book


# 表格字段筛选
# class AncientPoetryFilter(django_filters.FilterSet):
#     title = django_filters.CharFilter(field_name='title', lookup_expr='contains')
#     category = django_filters.CharFilter(field_name='category', lookup_expr='exact')
#     author = django_filters.CharFilter(field_name="author", lookup_expr="contains")
#     dynasty = django_filters.CharFilter(field_name="dynasty", lookup_expr="exact")
#     content = django_filters.CharFilter(field_name="content", lookup_expr='contains')
#
#     class Meta:
#         model = AncientPoetry
#         fields = ('title', 'category', 'author', 'dynasty', 'content')


class BooksFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Book
        fields = ('name',)
