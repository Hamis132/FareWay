from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Attraction(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)

    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True)
    time = models.TimeField(blank=True)
    description = models.CharField(max_length=255)
    image = models.ImageField(blank=True,null=True,upload_to="post_img")

    def __str__(self):
        return self.name


class Route(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    route_name = models.CharField(max_length=30)
    attractions = models.ManyToManyField(Attraction, related_name='attractions')
    start = models.ForeignKey(Attraction, related_name='start', default=None, blank=True, null=True, on_delete=models.CASCADE)
    end = models.ForeignKey(Attraction, related_name='end', default=None, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.route_name
