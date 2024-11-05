from rest_framework import serializers
from .models import Object


class ObjectSerializer(serializers.Serializer):
    id = serializers.CharField(read_only = True)
    name = serializers.CharField(max_length = 128)
    type = serializers.ChoiceField(choices = Object.TYPE_OPTIONS, required = False)
    level = serializers.IntegerField(min_value = 1, max_value = 5, required = False)
    text = serializers.CharField(required = False)
    published = serializers.BooleanField(default = False)

    def create(self, validated_data):
        return Object(**validated_data).save()

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.type = validated_data.get('type', instance.type)
        instance.level = validated_data.get('level', instance.level)
        instance.text = validated_data.get('text', instance.text)
        instance.published = validated_data.get('published', instance.published)
        instance.save()
        return instance