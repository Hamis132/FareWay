from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# class Coordinates(models.Model):
#    latitude = models.DecimalField(
#        max_digits=9, decimal_places=6, null=True, blank=True)
#
#    longitude = models.DecimalField(
#        max_digits=9, decimal_places=6, null=True, blank=True)


class Attraction(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
#    position = models.ForeignKey(Coordinates, on_delete=models.CASCADE)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)

    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)
    time = models.TimeField(blank=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Trip(models.Model):
    user = models.ForeignKey(User, default=0, on_delete=models.CASCADE)
    attractions = models.ManyToManyField(Attraction, through='TripAttraction')


class TripAttraction(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)
