from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

from .views import IngredientListView, shopping_list, RecipeIngredientView, follow_user, follow_recipe

router = DefaultRouter()

router.register(r'ingredients', IngredientListView)

urlpatterns = router.urls

urlpatterns += [
    path('<int:recipe_id>/favorites/', views.follow_recipe, name='follow_user'),
    path('<int:author_id>/subscriptions/', views.follow_user, name='follow_user'),
    path('<int:recipe_id>/purshases/', views.shopping_list, name='purshases'),
]