from django.urls import path
from .views import home

app_name = 'dashboard_home'

urlpatterns = [
    path('', home, name='home')
]