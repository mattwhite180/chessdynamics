from rest_framework import serializers
from chessapp.models import Game


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = [
            "id",
            "name",
            "description",
            "move_list",
            "white",
            "black",
            "time_controls",
            "results",
            "available",
            "turn",
            "fen",
            "legal_moves",
            "pgn",
            "creation_date",
        ]

    def create(self, validated_data):
        """
        Create and return a new `Game` instance, given the validated data.
        """
        return Game.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Game` instance, given the validated data.
        """
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.white = validated_data.get("white", instance.white)
        instance.black = validated_data.get("black", instance.black)
        instance.time_controls = validated_data("time_controls", instance.time_controls)
        instance.save()
        return instance
