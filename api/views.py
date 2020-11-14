from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework import generics, filters, mixins, viewsets, serializers
from rest_framework.utils import json
from rest_framework.response import Response

from posts.models import ShoppingList, Ingredient, RecipeIngredient, Recipe
from .serializers import IngredientSerializer, ShoppingListSerializer, RecipeIngredientSerializer


class IngredientListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['title', ]
    ordering_fields = ['title',]


#class ShoppingListView(generics.ListCreateAPIView):#, viewsets.GenericViewSet):
class ShoppingListView(generics.CreateAPIView, generics.DestroyAPIView):
    print('cvvdfvdvdfvfdvfdv')
    queryset = ShoppingList.objects.all()
    print('cvvdfvdvdfvfdvfdv111111')
    serializer_class = ShoppingListSerializer
    print('cvvdfvdvdfvfdvfdv222222')

    def perform_create(self, serializer): 
        print('cvvdfvdvdfvfdvfdvфункция1')
        id = self.kwargs.get('recipe_id')
        print('ssddsddsdd', id)
        recipe = get_object_or_404(Recipe, pk = id)
        print('recipe', recipe)       
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