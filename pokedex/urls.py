from django.urls import path

from . import views

app_name = 'pokedex'
urlpatterns = [
    # Home page
    path('', views.home, name='index'),
]