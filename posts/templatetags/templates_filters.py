from django import template

from posts.models import Follow_User, Follow_Recipe, ShoppingList

register = template.Library()


@register.filter(name='is_follow')
def is_follow(author, user):
    return Follow_User.objects.filter(user=user, author=author).exists()


@register.filter(name='is_favorite')
def is_favorite(post, user):
    return Follow_Recipe.objects.filter(user=user, post=post).exists()


@register.filter(name='is_shop')
def is_shop(recipe, user):
    return ShoppingList.objects.filter(user=user, recipe=recipe).exists()


@register.filter(name='get_filter_values')
def get_filter_values(value):
    return value.getlist('filters')


@register.filter(name="get_filter_link")
def get_filter_link(request, tag):
    new_request = request.GET.copy()

    if tag.slug in request.GET.getlist("filters"):
        filters = new_request.getlist("filters")
        filters.remove(tag.slug)
        new_request.setlist("filters", filters)
    else:
        new_request.appendlist("filters", tag.slug)

    return new_request.urlencode()