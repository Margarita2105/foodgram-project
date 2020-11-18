from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

from .views import IngredientListView, ShoppingListView, RecipeIngredientView, Follow_UserView, Follow_RecipeView

router = DefaultRouter()

router.register(r'ingredients', IngredientListView)

urlpatterns = router.urls

urlpatterns += [
    path('<int:recipe_id>/favorites/', views.Follow_RecipeView, name='follow_user'),
    path('<int:author_id>/subscriptions/', views.Follow_UserView, name='follow_user'),
    path('<int:recipe_id>/purshases/', views.ShoppingListView, name='purshases'),
]