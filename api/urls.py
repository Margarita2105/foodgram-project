from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import IngredientListView, ShoppingListView, RecipeIngredientView

router = DefaultRouter()


router.register(r'ingredients', IngredientListView)
#router.register(r'purchases', ShoppingListView)
#router.register(r'recipeingredient', RecipeIngredientView)

urlpatterns = router.urls

urlpatterns += [
#    path('', include(router.urls)),
    path('<int:recipe_id>/purshases/', ShoppingListView.as_view(), name='purshases'),
]