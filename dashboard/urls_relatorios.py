from django.urls import path
from .views import relatorios

app_name = 'dashboard_relatorios'

urlpatterns = [
    path('', relatorios, name='relatorios')
]