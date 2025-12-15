from django.urls import path
from .views import upload

app_name = 'dashboard_upload'

urlpatterns = [
    path('upload/<str:type>/', upload, name='upload')
]