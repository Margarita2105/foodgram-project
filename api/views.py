from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from rest_framework import generics, filters, mixins, viewsets, serializers
from rest_framework.utils import json
from rest_framework.response import Response

from posts.models import ShoppingList, Ingredient, RecipeIngredient
from .serializers import IngredientSerializer, ShoppingListSerializer, RecipeIngredientSerializer


class IngredientListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['title', ]
    ordering_fields = ['title',]


class ShoppingListView(generics.ListCreateAPIView):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer
 

class RecipeIngredientView(generics.ListCreateAPIView):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer