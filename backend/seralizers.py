from rest_framework import serializers

from backend.models import Book


# class ContentListField(serializers.Field):
#     def to_representation(self, value):
#         return value.replace('&', '')  # 去掉&分割符号
#
#
# class AncientPoetrySerializer(serializers.ModelSerializer):
#     content = ContentListField()  # 序列化字符串
#
#     class Meta:
#         model = AncientPoetry
#         # fields = '__all__'
#         exclude = ['appreciation', 'notes']
#         read_only_fields = ['id']


class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'name', 'pic_url', 'description']
        read_only_fields = ['id']
