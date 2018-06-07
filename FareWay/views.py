
from django.contrib.auth.forms import UserCreationForm
from .models import Attraction
from django.shortcuts import render, get_object_or_404, redirect


def home(request):
    attractions = Attraction.objects.get_queryset()
    return render(request,'home.html', {'attractions':attractions})

def attraction_details(request,pk):
    attraction=get_object_or_404(Attraction,pk=pk)
    return render(request,'attraction_details.html',{'attraction':attraction})
# a59c0d55e9c97e97198e45c992173a7003629899

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/register/success')
    else:
        form = UserCreationForm()
        args ={'form':form}
    return render(request, "registration/register.html", args)

def registration_complete(request):
    return render(request, 'registration/registration_complete.html')