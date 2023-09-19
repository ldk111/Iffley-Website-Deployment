from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name ="home"),
    path('routes/', views.routes, name="routes"),
    path('route/<int:route_id>', views.route_details, name='route_details'),
    path('ticklists/', views.ticklists, name="ticklists"),
    path('circuits/', views.circuits, name="circuits")
]