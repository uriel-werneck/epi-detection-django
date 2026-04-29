from django.urls import path
from .views import home, relatorios, minhas_deteccoes, upload, download_image

app_name = 'dashboard'

urlpatterns = [
   path('home/', home, name='home'),
   path('relatorios/', relatorios, name='relatorios'),
   path('minhas-deteccoes/', minhas_deteccoes, name='minhas_deteccoes'),
   path('dashboard/upload/<str:type>/', upload, name='upload'),
   path('dashboard/detections/<uuid:detection_id>/download/', download_image, name='download_imagem')
]