import json
import csv

from django.contrib.auth import get_user_model, decorators
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse

from .forms import RecipeForm
from .models import Ingredient, Recipe, RecipeIngredient, ShoppingList, Follow_User, Follow_Recipe
from .utils import IngredientsValid, food_time_f

User = get_user_model()

def ingredients(request):
    with open('ingredients.json', 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    for i in data:
        print('Новый ингридиент:',i)
        ingredient = Ingredient(title=i['title'], dimension=i['dimension'])
        ingredient.save()
    return HttpResponse('\n'.join(str(data)))


def index(request):
    food = {
        'breakfest': (True, False),
        'lunch': (True, False),
        'dinner': (True, False)
        }
    food_time = request.GET.get('filter')
    if food_time in food:
        food[food_time] = (True,)
    recipes = Recipe.objects.select_related('author').order_by('-pub_date').all()
    recipe_list = recipes.filter(
        breakfest__in=food['breakfest'],
        lunch__in=food['lunch'],
        dinner__in=food['dinner'])
    paginator = Paginator(recipe_list, 10) 
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "index.html", {"page": page, "paginator": paginator, 'food_time':food_time})

def recipe_view(request, username, recipe_id):
    author = get_object_or_404(User, username=username)
    recipe = get_object_or_404(Recipe, pk=recipe_id, author=author)
    inrgedients = RecipeIngredient.objects.filter(recipe_id=recipe.pk)
    can_follow = request.user.is_authenticated and request.user != author
    return render(request, 'singlePage.html', {'recipe':recipe,
        'username':author, 'ingredients':inrgedients, 'follow_button': can_follow})

def get_ingredients(request):
    ingredients = {}
    for key, ingredient_name in request.POST.items():
        if 'nameIngredient' in key:
            _ = key.split('_')
            ingredients[ingredient_name] = int(request.POST[
                f'valueIngredient_{_[1]}']
            )
    return ingredients

@login_required
def new_post(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)

    if request.method == 'POST':
        ingredients = get_ingredients(request)
        if not ingredients:
            form.add_error(None, 'Добавьте ингредиенты')

    if form.is_valid():
        form.instance.author = request.user
        recipe = form.save(commit=False)
        recipe.save()
        data = ingredients.items()
        for pk, am in data:
            ingredient_obj = get_object_or_404(Ingredient, title=pk)
            ingredient_recipe = RecipeIngredient(
                ingredient=ingredient_obj, recipe=recipe, qty=am)
            ingredient_recipe.save()
        form.save_m2m()
        return redirect('index')

    return render(request, 'new.html', {'form': form})

def profile(request, username):
    food = {
        'breakfest': (True, False),
        'lunch': (True, False),
        'dinner': (True, False)
        }
    food_time = request.GET.get('filter')
    if food_time in food:
        food[food_time] = (True,)
  
    post_author = get_object_or_404(User, username=username)
    profile_recipe = Recipe.objects.select_related(
        'author').filter(author_id=post_author.pk)
    recipe_list = profile_recipe.filter(
        breakfest__in=food['breakfest'],
        lunch__in=food['lunch'],
        dinner__in=food['dinner'])
    can_follow = request.user.is_authenticated and request.user != post_author
    paginator = Paginator(recipe_list, 5)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request,"profile.html", {"post_author": post_author,
        "paginator": paginator,"page": page, 'food_time':food_time, 'follow_button': can_follow}) 


@login_required
def post_edit(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id, author__username=username)
    ingredients_objs = RecipeIngredient.objects.filter(recipe=recipe)

    if request.user != recipe.author and not request.user.is_superuser:
        return redirect('recipe', username=username, recipe_id=recipe_id)

    form = RecipeForm(request.POST or None,
                      files=request.FILES or None, instance=recipe)

    if request.method == "POST":
        ingredients = get_ingredients(request)
        form = RecipeForm(request.POST or None,
                          files=request.FILES or None, instance=recipe)
        
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.save()
            RecipeIngredient.objects.filter(recipe=recipe).delete()
            
            data = ingredients.items()
            for pk in data:
                ingredient_obj = get_object_or_404(Ingredient, title=pk[0])
                ingredient_recipe = RecipeIngredient(
                    ingredient=ingredient_obj, recipe=recipe, qty=pk[1])
                ingredient_recipe.save()
        form.save_m2m()
        return redirect('index')

    return render(request, 'formChangeRecipe.html',
                  {'form': form, 'recipe_obj': recipe, 'ingredients_objs': ingredients_objs})



@login_required
def recipe_delete(request, username, recipe_id):
    recipe = get_object_or_404(
        Recipe, author__username=username, pk=recipe_id)

    if request.method == 'POST':
        if recipe.author == request.user or request.user.is_superuser:
            recipe.delete()
        return redirect('index')
    else:
        return render(request, 'DelRecipe.html', {
            'recipe_id': recipe_id,
            'username': username,
            'recipe_obj': recipe})


def page_not_found(request, exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)


@login_required
def follow_index(request):
    author_list = Follow_User.objects.filter(
        user__id=request.user.id).all()
    for i in author_list:
        print(i.author)
    paginator = Paginator(author_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'follow1.html',
        {'page': page, 'paginator': paginator, 'author': author_list}
    )


@login_required
def follow_recipe_index(request):
    
    follow_recipe = Follow_Recipe.objects.filter(user=request.user).values_list("recipe_id", flat=True)
    count = Follow_Recipe.objects.filter(user=request.user).count()
    recipe_list = Recipe.objects.filter(id__in=follow_recipe).order_by("-pub_date").all()
    recipe, food_time = food_time_f(request, recipe_list)
    paginator = Paginator(recipe, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    return render(request, "follow.html", {"page": page, "paginator": paginator, "count": count, "food_time": food_time})


@decorators.login_required
def shoppinglist(request):
    shop = ShoppingList.objects.select_related('recipe').filter(
    user=request.user)
    return render(request, 'shoplist1.html', {"shop": shop})


def shoplist(request):
    recipes = Recipe.objects.filter(purchases__user=request.user)

    ingredients_needed: dict = {}

    for recipe in recipes:
        ingredients = recipe.ingredients.values_list('title', 'dimension')
        content = recipe.recipe_ingredients.values_list('qty', flat=True)

        for num in range(len(ingredients)):
            title: str = ingredients[num][0]
            dimension: str = ingredients[num][1]
            quantity: int = content[num]

            if title in ingredients_needed.keys():
                ingredients_needed[title] = [ingredients_needed[title][0] + quantity, dimension]
            else:
                ingredients_needed[title] = [quantity, dimension]

    response = HttpResponse(content_type='txt/csv')
    writer = csv.writer(response)

    for key, value in ingredients_needed.items():
        writer.writerow([f'{key} ({value[1]}) - {value[0]}'])

    return response
