from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
class Genre(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="genre/")

class Film(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.DateField()
    image = models.ImageField(upload_to="films/")
    rating = models.FloatField(validators=[MinValueValidator(0.0),MaxValueValidator(10.0)])
    genre = models.ManyToManyField(Genre)

class Actor(models.Model):
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    born_date = models.DateField()
    image = models.ImageField(upload_to="actors/")
    film = models.ManyToManyField(Film)

class Review(models.Model):
    stars = [(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')]
    username = models.CharField(max_length = 32, verbose_name = 'Ваш никнейм')
    text = models.CharField(max_length=512,verbose_name = 'Текст отзыва')
    star = models.IntegerField(choices = stars,verbose_name = 'Оценка')
    film = models.ForeignKey(Film, on_delete=models.CASCADE)