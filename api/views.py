import json
import csv

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from rest_framework import generics, filters, mixins, viewsets, serializers
from rest_framework.utils import json
from rest_framework.response import Response


from posts.models import ShoppingList, Ingredient, RecipeIngredient, Recipe, Follow_User, Follow_Recipe, User
from .serializers import IngredientSerializer, RecipeIngredientSerializer


class IngredientListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter, ]
    search_fields = ['title', ]
    ordering_fields = ['title',]



@login_required
@require_http_methods(['POST', 'DELETE'])
def Follow_UserView(request, author_id):

    if request.method == 'POST':
        author_id = json.loads(request.body).get('id')
        author = get_object_or_404(User, id=author_id)

        obj, created = Follow_User.objects.get_or_create(user=request.user, author=author)

        return JsonResponse({'success': created})

    elif request.method == 'DELETE':
        author = get_object_or_404(User, id=author_id)

        removed = Follow_User.objects.filter(user=request.user, author=author).delete()
        return JsonResponse({'success': bool(removed)})


    

@login_required
@require_http_methods(['POST', 'DELETE'])
def Follow_RecipeView(request, recipe_id):

    if request.method == 'POST':
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)

        obj, created = Follow_Recipe.objects.get_or_create(user=request.user, recipe=recipe)

        return JsonResponse({'success': created})

    elif request.method == 'DELETE':
        recipe = get_object_or_404(Recipe, id=recipe_id)

        removed = Follow_Recipe.objects.filter(user=request.user, recipe=recipe).delete()
        return JsonResponse({'success': bool(removed)})


@login_required
@require_http_methods(['POST', 'DELETE'])
def ShoppingListView(request, recipe_id):

    if request.method == 'POST':
        recipe_id = json.loads(request.body).get('id')
        recipe = get_object_or_404(Recipe, id=recipe_id)

        obj, created = ShoppingList.objects.get_or_create(user=request.user, recipe=recipe)

        return JsonResponse({'success': created})

    elif request.method == 'DELETE':
        recipe = get_object_or_404(Recipe, id=recipe_id)

        removed = ShoppingList.objects.filter(user=request.user, recipe=recipe).delete()
        return JsonResponse({'success': bool(removed)})
 

class RecipeIngredientView(generics.ListCreateAPIView, viewsets.GenericViewSet):
    queryset = RecipeIngredient.objects.all()
    serializer_class = RecipeIngredientSerializer