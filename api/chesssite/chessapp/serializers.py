from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class GameSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=200)
    description = serializers.CharField(required=False, allow_blank=True, max_length=500)
    move_list = serializers.CharField(required=False, allow_blank=True, max_length=2000)
    white = serializers.CharField(required=False, allow_blank=True, max_length=200)
    white_level = serializers.IntegerField(required=False, allow_blank=True)
    black = serializers.CharField(required=False, allow_blank=True, max_length=500)
    black_level = serializers.IntegerField(required=False, allow_blank=True)
    time_controls = serializers.IntegerField(required=False, allow_blank=True)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Game.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.move_list = validated_data.get('move_list', instance.move_list)
        instance.white = validated_data.get('white', instance.white)
        instance.white_level = validated_data.get('white_level', instance.white_level)
        instance.black = validated_data.get('black', instance.black)
        instance.black_level = validated_data.get('black_level', instance.black_level)
        instance.time_controls = validated_data.get('time_controls', instance.time_controls)
        instance.save()
        return instance