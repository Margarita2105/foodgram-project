from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import IngredientListView

router = DefaultRouter()


router.register(r'ingredients', IngredientListView)
router.register(r'purchases', IngredientListView)

urlpatterns = router.urls