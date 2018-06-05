from django.shortcuts import render
from django.http import HttpResponse
from .models import Attraction

def home(request):
    attractions = Attraction.objects.get_queryset()
    return render(request,'home.html', {'attractions':attractions})