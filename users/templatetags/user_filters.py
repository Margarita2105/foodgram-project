from django import template
from posts.models import Follow_User, ShoppingList, Follow_Recipe
register = template.Library()


@register.filter 
def addclass(field, css):
        return field.as_widget(attrs={"class": css})

@register.filter(name='is_follow')
def is_follow(author, user):
    if not user.is_authenticated:
        return False
    return Follow_User.objects.filter(user=user, author=author).exists()


@register.filter(name='is_favorite')
def is_favorite(recipe, user):
    if not user.is_authenticated:
        return False
    return Follow_Recipe.objects.select_related('recipe').filter(
        user=user, recipe=recipe).exists()


@register.filter(name='is_shoplist')
def shoplist(recipe, user):
    if not user.is_authenticated:
        return False
    return ShoppingList.objects.filter(user=user, recipe=recipe).exists()


@register.filter(name='get_recipes')
def get_recipes(cook):
    return Recipe.objects.select_related('author').filter(author=cook)[:3]


@register.filter(name='get_count_recipes')
def get_count_recipes(cook):
    count = cook.recipes_author.count() - 3
    if count < 1:
        return False

    if count % 10 == 1 and count % 100 != 11:
        end = 'рецепт'
    elif 2 <= count % 10 <= 4 and (count % 100 < 10 or count % 100 >= 20):
        end = 'рецепта'
    else:
        end = 'рецептов'

    return f'Еще {count} {end}...'