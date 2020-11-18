from .models import ShoppingList


def get_shop_list(request):
    """ Количество рецептов списке покупок. """
    if request.user.is_authenticated:
        shop_list_count = ShoppingList.objects.filter(
            user=request.user
        ).count()
    else:
        shop_list_count = None

    return {'shop_list_count': shop_list_count}