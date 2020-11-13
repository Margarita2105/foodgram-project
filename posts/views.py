from django.contrib.auth import get_user_model
# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
#from django.views.decorators.cache import cache_page

from .forms import RecipeForm
from .models import Ingredient, Recipe, RecipeIngredient, ShoppingList, Follow_User, Follow_Recipe
from .utils import IngredientsValid

User = get_user_model()

def ingredients(request):
    import json
    from django.http import HttpResponse
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
    return render(request, 'singlePage.html', {'recipe':recipe, 'username':author, 'ingredients':inrgedients})

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
    if request.method == 'POST':
        author = request.user
        ingredients = get_ingredients(request)
        form = RecipeForm(request.POST or None, files=request.FILES or None, )
        if not ingredients:
            form.add_error(None, 'Добавьте ингредиенты')
            
        elif form.is_valid():
            form.instance.author = author
            recipe = form.save(commit=False)
            recipe.save()
            data = ingredients.items()
            for pk, rt in data:
                ingredient_obj = get_object_or_404(Ingredient, title=pk)
                ingredient_recipe = RecipeIngredient(ingredient=ingredient_obj, recipe=recipe, qty=rt)#data[pk])
                ingredient_recipe.save()
            form.save_m2m()
            del ingredients
            return redirect('index')
        #del ingredients
        return render(request, 'formRecipe.html', {'form':form})
    form = RecipeForm()
    return render(request, 'formRecipe.html', {'form':form})

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
    profile_recipe = Recipe.objects.filter(author=post_author).order_by("-pub_date").all()
    recipe_list = profile_recipe.filter(
        breakfest__in=food['breakfest'],
        lunch__in=food['lunch'],
        dinner__in=food['dinner'])
    paginator = Paginator(recipe_list, 5)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request,"profile.html", {"post_author": post_author, "paginator": paginator,"page": page, 'food_time':food_time}) 

def recipe_profile(request, recipe):
    recipe = RecipeIngredient.objects.filter(recipe=recipe)
    return render(request,"profile.html", {'recipe': recipe})



@login_required
def post_edit(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.user != recipe.author:
        return redirect('index')

    if request.method == "POST":
        form = RecipeForm(request.POST or None,
                          files=request.FILES or None, instance=recipe)
        ingredients = get_ingredients(request)
        if form.is_valid():
            RecipeIngredient.objects.filter(recipe=recipe).delete()
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            for item in ingredients:
                RecipeIngredient.objects.create(
                    qty=ingredients[item],
                    ingredient=Ingredient.objects.get(title=f'{item}'),
                    recipe=recipe)
            form.save_m2m()
            return redirect('index')

    form = RecipeForm(request.POST or None,
                      files=request.FILES or None, instance=recipe)

    return render(request, 'new.html',
                  {'form': form, 'recipe': recipe, })

    
def page_not_found(request, exception):
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)


@login_required
def follow_index(request):
    follow = Follow_User.objects.filter(user=request.user).values_list("author_id", flat=True)
    count = Follow_User.objects.filter(user=request.user).count()
    recipe_list = Recipe.objects.filter(author_id__in=follow).order_by("-pub_date").all()
    paginator = Paginator(recipe_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "follow1.html", {"page": page, "paginator": paginator, "count": count})


@login_required
def follow_recipe_index(request):
    follow_recipe = Follow_Recipe.objects.filter(user=request.user).values_list("recipe_id", flat=True)
    count = Follow_Recipe.objects.filter(user=request.user).count()
    recipe_list = Recipe.objects.filter(recipe_id__in=follow_recipe).order_by("-pub_date").all()
    paginator = Paginator(recipe_list, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "follow.html", {"page": page, "paginator": paginator, "count": count})
  
@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    follow = Follow_User.objects.filter(user=request.user, author=author)
    if not follow.exists() and author != request.user:
        Follow_User.objects.create(user=request.user, author=author)
    return redirect(follow_index)


@login_required
def profile_unfollow(request, username):
    post_author = get_object_or_404(User, username=username)
    Follow_User.objects.filter(user=request.user, author=post_author).delete()
    return redirect(profile, username)

@login_required
def recipe_follow(request, recipe):
    recipe = get_object_or_404(Recipe, recipe=recipe)
    follow = Follow_Recipe.objects.filter(user=request.user, recipe=recipe)
    if not follow.exists() and author != request.user:
        Follow_Recipe.objects.create(user=request.user, recipe=recipe)
    return redirect(follow_index)


@login_required
def recipe_unfollow(request, username):
    recipe = get_object_or_404(Recipe, recipe=recipe)
    Follow_Recipe.objects.filter(user=request.user, author=post_author).delete()
    return redirect(profile, username)

def shoplist(request):
    shop = get_object_or_404(User, username=request.user.username)
    rein = shop.purchaser.all()
    inglist = {}
    for ing in rein:
        for j in recipe.recipeingredient_set.all():
            name = j.ingredient.title
            dim = j.ingredient.dimension
            am = {}
            if name in inglist.keys():
                inglist[name][dim] += j.qty
            else:
                am[dim] = j.qty
            inglist[name] = am.copy()
    print(inglist)
    return inglist  

def shoppinglist(request):
    shop = ShoppingList.objects.select_related('recipe').filter(user=request.user.id)
    paginator = Paginator(shop, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, 'shoplist1.html', {"page": page, "paginator": paginator,})



