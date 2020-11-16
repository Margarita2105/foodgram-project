from rest_framework import serializers
from django.contrib.auth import get_user_model

from posts.models import Ingredient, ShoppingList, RecipeIngredient, Follow_User, Follow_Recipe


User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'dimension')
        model = Ingredient


class Follow_UserSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    author = serializers.StringRelatedField()
    class Meta:
        fields = ('user', 'author',)
        model = Follow_User


class Follow_RecipeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    recipe = serializers.StringRelatedField()
    class Meta:
        fields = ('user', 'recipe',)
        model = Follow_Recipe


class ShoppingListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    recipe = serializers.StringRelatedField()
    class Meta:
        fields = ('user', 'recipe',)
        model = ShoppingList


class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('ingredient', 'recipe', 'qty',)
        model = ShoppingList