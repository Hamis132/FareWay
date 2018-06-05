from django.shortcuts import render
from django.http import HttpResponse
from .models import Attraction
from django.shortcuts import render, get_object_or_404

def home(request):
    attractions = Attraction.objects.get_queryset()
    return render(request,'home.html', {'attractions':attractions})

def attraction_details(request,pk):
    attraction=get_object_or_404(Attraction,pk=pk)
    return render(request,'attraction_details.html',{'attraction':attraction})