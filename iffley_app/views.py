from django.shortcuts import render, get_object_or_404
from .forms import FilterGrades, SearchBar
from django.db.models import Q
from django.conf import settings

from .models import *

def home(request):
    return render(request, "iffley_app/home.html")

def routes(request):
    
    routes = Route.objects.all()
    sections = Section.objects.all()

    if request.method == "GET":

        form = FilterGrades(request.GET)
        searchbar = SearchBar(request.GET)

        if form.is_valid():
            grades = form.cleaned_data["grades"]
            print(grades)
        
        if searchbar.is_valid():
            query = searchbar.cleaned_data["search"]
            if grades:
                routes = routes.filter((Q(name__icontains=query) | Q(holds__name__iexact=query) | Q(tech_grade__grade__iexact=query) | Q(b_grade__grade__iexact=query) | Q(furlong_grade__grade__iexact=query)) & Q(tech_grade__in=grades)).distinct()
            else:
                routes = routes.filter(Q(name__icontains=query) | Q(holds__name__iexact=query) | Q(tech_grade__grade__iexact=query) | Q(b_grade__grade__iexact=query) | Q(furlong_grade__grade__iexact=query)).distinct()
        
    else:
        form = FilterGrades()
        searchbar = SearchBar()
    
    return render(request, "iffley_app/routes.html", {"form":form, "searchbar": searchbar, 'routes':routes, 'sections': sections})

def route_details(request, route_id):

    route = get_object_or_404(Route, id=route_id)
    context = {'route': route, 'route_url': settings.STATIC_URL + str(route.image) if route.image else None}

    return render(request, 'iffley_app/route_details.html', context)
