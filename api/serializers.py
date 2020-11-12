from rest_framework import serializers
from django.contrib.auth import get_user_model

from posts.models import Ingredient, ShoppingList, RecipeIngredient


User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'dimension')
        model = Ingredient


class ShoppingListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('user', 'recipe',)
        model = ShoppingList


class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('ingredient', 'recipe', 'qty',)
        model = ShoppingList