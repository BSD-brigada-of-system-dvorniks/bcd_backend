from rest_framework import serializers

from .models import Article, Object
from accounts.serializers import UserSerializer


class BasicArticleSerializer(serializers.Serializer):
    name = serializers.CharField(max_length = 128)  # Only include basic fields
    published = serializers.BooleanField(default = False)


class BasicObjectSerializer(serializers.Serializer):
    id = serializers.CharField(read_only = True)
    type = serializers.ChoiceField(choices = Object.TYPE_OPTIONS, required = False)
    level = serializers.IntegerField(min_value = 1, max_value = 5, required = False)
    article = BasicArticleSerializer()


class ArticleSerializer(serializers.Serializer):
    name = serializers.CharField(max_length = 128)
    text = serializers.CharField(max_length = 256_000)
    published = serializers.BooleanField(default = False)
    author = UserSerializer(read_only = True)

    def create(self, validated_data):
        return Article(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.published = validated_data.get('published', instance.published)
        instance.author = validated_data.get('author', instance.author)
        return instance


class ObjectSerializer(serializers.Serializer):
    id = serializers.CharField(read_only = True)
    type = serializers.ChoiceField(choices = Object.TYPE_OPTIONS, required = False)
    level = serializers.IntegerField(min_value = 1, max_value = 5, required = False)
    article = ArticleSerializer()

    def create(self, validated_data):
        article_data = validated_data.pop('article')
        article = Article(**article_data)  # Create an Article instance
        obj = Object(article = article, **validated_data)
        obj.save()
        return obj

    def update(self, instance, validated_data):
        instance.type = validated_data.get('type', instance.type)
        instance.level = validated_data.get('level', instance.level)

        article_data = validated_data.get('article')
        if article_data:
            article = instance.article
            article.name = article_data.get('name', article.name)
            article.text = article_data.get('text', article.text)
            article.published = article_data.get('published', article.published)
        
        instance.save()
        return instance
