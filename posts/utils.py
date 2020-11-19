def food_time_f(request, queryset):
    food = {
        'breakfest': (True, False),
        'lunch': (True, False),
        'dinner': (True, False)
    }
    food_time = request.GET.get('filter')

    if food_time in food:
        food[food_time] = (True,)

    queryset_new = queryset.filter(
        breakfest__in=food['breakfest'],
        lunch__in=food['lunch'],
        dinner__in=food['dinner'])

    return queryset_new, food_time