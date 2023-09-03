from django.shortcuts import render, get_object_or_404
from .forms import FilterGrades, SearchBar
from django.db.models import Q, Count
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

    section_ids_with_routes = set(routes.values_list('section__id', flat=True))
    sections = sections.filter(id__in=section_ids_with_routes)

    return render(request, "iffley_app/routes.html", {"form":form, "searchbar": searchbar, 'routes':routes, 'sections': sections})

def route_details(request, route_id):

    route = get_object_or_404(Route, id=route_id)
    context = {'route': route, 'route_url': settings.STATIC_URL + str(route.image) if route.image else None}

    return render(request, 'iffley_app/route_details.html', context)

def ticklists(request):

    routes = Route.objects.all()

    ticklists = {"Level 1 - First Steps": ["The Ladder", "Ali G", "Boing! Said Zebedee", "The Right Stuff", "Dynosaur", "The Rocker"],
                 "Level 2 - Easy Classics": ["Question Time", "Ice Cube", "Twisted Sister", "The Bad", "The Jester", "No Problem", "Overlap", "Tiffin", "Pebble Beach", "The Slide", "Wax On, Wax Off", "The Sting", "Rock & Roll", "Stroll"],
                 "Level 3 - Into the Fives": ["Sabre Dance", "Die Gerbils!", "Touch Me", "Squetch", "Halloween", "Cosmic", "Long Division", "Varsity", "Weak Like Monkey", "Major League", "Die Yetis!", "Befuddled", "Irn Bru", "Strong Like Bull", "Central Pillar"],
                 "Level 4 - Classic Iffley": ["The Pint Glass", "Superman in Y-Fronts", "Gaston", "Overmantel", "Laah!", "Monocle", "Stage Left", "Wet Paint", "Geronimo!", "Gormenghast", "My Name is Neo", "Green Goddess", "Jenga", "The Sorcerer's Apprentice", "Hebrews 5.10", "Kiss the Wall", "Crushed Strawberry", "Shelve It", "C2", "Chaos Theory", "The Beards of Zeus", "Ape Index", "Judean People's Front Crack Suicide Squad", "Naked", "Enigma", "The Nose", "The Matrix", "Masters of Stone", "PARC Analysis", "High Tension", "Ambiguity"],
                 "Level 5 - The Threshold Problems": ["Analogue", "Digital", "This is a Low", "Twister Variation", "The Apes of Wrath", "The Tactice Variation", "Resurrection", "Hate Mail", "The Tensor", "Deadpoint", "The Dance of the Electric Penguin"],
                 "Level 6 - Hard Iffley": ["The Tall Man Rides a Shovelhead", "Osmosis", "Moby Dick", "The Blair Witch Project", "The Four Minute Mile", "The Fallen", "Zebedee's Torment", "The Witching Hour", "Horny Little Devil", "Potheosis", "Ice Lolly", "Palm Beach", "Bemused", "Ecstasy"],
                 "Girdering - The Black Art": ["Rainbow", "The Easy Touch", "To the Girder", "Curdled Custard", "Long Division", "Up and Away", "Popeye", "Pirates of the Caribbean", "Geronimo!", "Harder, Faster", "Obscenity", "Square Dance", "Swing Like a Monkey, Part 2", "Every Which Way But Up", "Into the Blue", "Dyno 8", "Voyager", "Apollo", "Aviation"] }
                 

    context = {'routes': routes, "ticklists": ticklists}

    return render(request, 'iffley_app/ticklists.html', context)