from django.urls import path
from .views import home, relatorios, minhas_deteccoes, upload, get_detection_image

app_name = 'dashboard'

urlpatterns = [
    path('home/', home, name='home'),
    path('relatorios/', relatorios, name='relatorios'),
    path('minhas-deteccoes/', minhas_deteccoes, name='minhas_deteccoes'),
    path('dashboard/upload/<str:type>/', upload, name='upload'),
    path('get-detection-image/<int:detection_id>/', get_detection_image, name='get_detection_image')
]