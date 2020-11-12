from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Recipe, Ingredient, RecipeIngredient, Follow_User, Follow_Recipe, ShoppingList


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    list_filter = ('author', 'title')
    inlines = (RecipeIngredientInline,)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('title', 'dimension')
    list_filter = ('title',)


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'qty')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    fields = ('user', 'author')


class FavoritesAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    fields = ('user', 'recipe')


class ShopListAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    fields = ('user', 'recipe')



admin.site.register(Recipe, RecipeAdmin)

admin.site.register(Ingredient, IngredientAdmin)

admin.site.register(RecipeIngredient, RecipeIngredientAdmin)

admin.site.register(Follow_User, FollowAdmin)

admin.site.register(Follow_Recipe, FavoritesAdmin)

admin.site.register(ShoppingList, ShopListAdmin)