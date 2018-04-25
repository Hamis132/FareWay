from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)


class Coordinates(models.Model):
    X = models.FloatField(null=True, blank=True)
    Y = models.FloatField(null=True, blank=True)


class Attraction(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    coordinates = models.ForeignKey(Coordinates, on_delete=models.CASCADE)
    time = models.TimeField(blank=True)
    description = models.CharField(max_length=255)


class Trip(models.Model):
    user = models.ForeignKey(User, default=0, on_delete=models.CASCADE)
    attractions = models.ManyToManyField(Attraction, through='TripAttraction')


class TripAttraction(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)









