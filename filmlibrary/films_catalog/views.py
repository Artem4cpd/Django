from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .models import Film
from .models import Review
from .models import Actor
from .models import Genre
from .forms import ReviewForm
from django.db.models import Avg

# Create your views here.

def film_detail(request,pk):
    film = get_object_or_404(Film, id=pk)
    form = ReviewForm
    reviews = Review.objects.filter(film=film)
    reviews_count = reviews.count()
    avg_rating = reviews.aggregate(Avg('star'))
    avg_rating = round(avg_rating['star__avg'], 1)
    context ={"film": film,'form':form, 'reviews': reviews, 'reviews_count': reviews_count, 'avg_rating': avg_rating}
    template = "films/film_detail.html"
    return render(request,template,context=context)

def add_review(request,pk):
    film = get_object_or_404(Film,id = pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit = False)
            review.film = film
            review.save()
            return redirect('film:film_detail',pk=pk)
            

def main_menu(request):
    films = Film.objects.all()
    context = {"films":films}
    template="films/main_menu.html"
    return render(request,template,context=context)

def genre_list(request):
    genre = Genre.objects.all()
    context = {"genre":genre}
    template ="films/genre_list.html"
    return render(request,template,context=context)

def genre_detail(request,slug):
    genre = get_object_or_404(Genre,title=slug)
    films = Film.objects.filter(genre=genre)
    context = {"genre": genre,"films":films}
    template = "films/genre_detail.html"
    return render(request, template, context=context)

def actors_list(request):
    actors = Actor.objects.all()
    context = {"actors":actors}
    template="films/actor_list.html"
    return render(request,template,context=context)

def actors_detail(request,pk):
    actor = get_object_or_404(Actor, id=pk)
    films = Film.objects.filter(actor=actor)
    context = {"actor": actor, "films": films}
    template = "films/actors_detail.html"
    return render(request, template, context=context)

def about_us(request):
    template = "films/about_us.html"
    return render(request,template,context={})