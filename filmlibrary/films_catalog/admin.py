from django.contrib import admin
from .models import Film
from .models import Genre
from .models import Actor
from .models import Review


# Register your models here.
admin.site.register(Film)
admin.site.register(Genre)
admin.site.register(Actor)
admin.site.register(Review)