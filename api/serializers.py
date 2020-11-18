from rest_framework import serializers
from django.contrib.auth import get_user_model

from posts.models import Ingredient, RecipeIngredient


User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'dimension')
        model = Ingredient


class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('ingredient', 'recipe', 'qty',)
        model = RecipeIngredient