from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('new_post/', views.new_post, name = 'new_post'),
    path('recipes/<username>/', views.profile, name='profile'),
    path('load_from_json/', views.ingredients),
    path('recipes/<username>/<int:recipe_id>/edit/', views.post_edit, name='post_edit'),
    path('recipes/<username>/<int:recipe_id>/', views.recipe_view, name='recipe'),
    path('purchases/', views.shoplist, name='purchases_list'),
    path('favorite/', views.follow_recipe_index, name='favorite_list'),
    path("<username>/follow/", views.follow_index, name="profile_follow"), 
]