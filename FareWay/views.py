from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden
from django.views import generic
import json

from .models import Attraction, Route, Category
from django.shortcuts import render, get_object_or_404, redirect
from FareWay.forms import RegistrationForm


def home(request):
    attractions = Attraction.objects.get_queryset()
    return render(request,'home.html', {'attractions':attractions})

def attraction_details(request,pk):
    attraction=get_object_or_404(Attraction,pk=pk)
    return render(request,'attraction_details.html',{'attraction':attraction})

def attractions(request):
    atracts=Attraction.objects.get_queryset()
    return render(request,'attractions.html',{'attracts':atracts})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(registration_complete)
    else:
        form = RegistrationForm()
    return render(request, "registration/register.html", {'form': form})


def registration_complete(request):
    return render(request, 'registration/registration_complete.html')


def routes(request):
    return render(request, 'routes.html')


class RoutesView(generic.ListView):
    template_name = 'routes.html'
    context_object_name = 'route_list'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Route.objects.filter(user=self.request.user.id)


class SamleRoutesView(generic.ListView):
    template_name = 'new_route.html'
    context_object_name = 'sample_routes'

    def get_queryset(self):
        return Route.objects.filter(user=None)


@login_required(login_url='login')
def route_config(request, route_pk):
    js_object = {
        'name': "Nowa trasa",
        'start': None,
        'end': None,
        'attractions': [],
    }
    if route_pk != 'empty':
        route = get_object_or_404(Route, pk=route_pk)
        js_object['name'] = route.route_name
        js_object['start'] = route.start.pk if route.start else None
        js_object['end'] = route.end.pk if route.end else None
        for attraction in route.attractions.all():
            js_object['attractions'].append(attraction.pk)
        if route.user:
            js_object['pk'] = route_pk
            if route.user != request.user:
                return HttpResponseForbidden()
    return render(request, 'route_config.html', {'route_pk': json.dumps(js_object)})


@login_required()
def update_route(request):
    if request.method == "POST":
        if 'pk' in request.POST:
            route = Route.objects.get(pk=request.POST['pk'])
        else:
            route = Route.objects.create(user=request.user)
        route.start = Attraction.objects.get(pk=request.POST['start']) if request.POST['start'] else None
        route.end = Attraction.objects.get(pk=request.POST['end']) if request.POST['end'] else None
        route.route_name = request.POST['name']
        route.attractions.clear()
        for pk in request.POST.getlist('attractions[]'):
            route.attractions.add(Attraction.objects.get(pk=pk))
        route.save()
        return HttpResponse()
    else:
        return HttpResponseForbidden()


@login_required()
def remove_route(request, route_pk):
    route = get_object_or_404(Route, pk=route_pk)
    route.delete()
    return redirect('routes')


@login_required()
def attractions(request):
     data = serializers.serialize('json', Attraction.objects.all())
     return HttpResponse(data)


@login_required()
def categories(request):
    data = serializers.serialize('json', Category.objects.all())
    return HttpResponse(data)
