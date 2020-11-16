from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework import generics, filters, mixins, viewsets, serializers
from rest_framework.utils import json
from rest_framework.response import Response

from posts.models import ShoppingList, Ingredient, RecipeIngredient, Recipe, Follow_User, Follow_Recipe, User
from .serializers import IngredientSerializer, ShoppingListSerializer, RecipeIngredientSerializer, Follow_UserSerializer, Follow_RecipeSerializer


class IngredientListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['title', ]
    ordering_fields = ['title',]


class Follow_UserView(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = Follow_User.objects.all()
    serializer_class = Follow_UserSerializer

    def perform_create(self, serializer): 
        id = self.kwargs.get('author_id')
        print('id', id)
        #author = get_object_or_404(User, pk = id)
        author = User.objects.get(pk=id)
        serializer.save(user=self.request.user, author=author)

    def get_object(self):
        id = self.kwargs.get('author_id')
        follow = get_object_or_404(Follow_User,  user = self.request.user, authore__id=id)
        return follow

    def  get_parser_context ( self ,  http_request ): 
        print('parser')
        return {'success': True}


class Follow_RecipeView(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = Follow_Recipe.objects.all()
    serializer_class = Follow_RecipeSerializer

    def perform_create(self, serializer): 
        id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, pk = id)
        serializer.save(user=self.request.user, recipe=recipe)

    def get_object(self):
        id = self.kwargs.get('recipe_id')
        follow = get_object_or_404(Follow_Recipe,  user = self.request.user, recipe__id=id)
        return follow

    def  get_parser_context ( self ,  http_request ): 
        print('parser')
        return {'success': True}


class ShoppingListView(generics.CreateAPIView, generics.DestroyAPIView):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer

    def perform_create(self, serializer): 
        id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, pk = id)
        serializer.save(user=self.request.user, recipe=recipe)

    def get_object(self):
        id = self.kwargs.get('recipe_id')
        shoppinglist = get_object_or_404(ShoppingList,  user = self.request.user, recipe__id=id)
        return shoppinglist

    def  get_parser_context ( self ,  http_request ): 
        print('parser')
        return {'success': True}
 

class RecipeIngredientView(generics.ListCreateAPIView, viewsets.GenericViewSet):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer