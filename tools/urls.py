from django.urls import path

from . import views

app_name = 'tools'
urlpatterns = [
    # Home page
    path('', views.get_home, name='home'),
]