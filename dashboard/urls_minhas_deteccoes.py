from django.urls import path
from .views import minhas_deteccoes

app_name = 'dashboard_minhas_deteccoes'

urlpatterns = [
    path('', minhas_deteccoes, name='deteccoes')
]