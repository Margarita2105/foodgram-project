from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('new_post/', views.new_post, name = 'new_post'),
    path('purchases/', views.shoppinglist, name='purchases_list'),
    path('recipes/<username>/', views.profile, name='profile'),
    path('load_from_json/', views.ingredients),
    path('recipes/<username>/<int:recipe_id>/edit/', views.post_edit, name='post_edit'),
    path('recipes/<username>/<int:recipe_id>/', views.recipe_view, name='recipe'),
    path('follows/', views.follow_index, name='profile_follow'),
    path('favorite/', views.follow_recipe_index, name='favorite_list'),
    path('recipes/<str:username>/<int:recipe_id>/delete/',
         views.recipe_delete, name='recipe_delete'),
    path('download_card', views.shoplist, name='download_card'),
]