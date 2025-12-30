from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from dashboard.services.detection import get_detection_stats

# Create your views here.
@login_required
def home(request):
    context = {
        'detection_stats': get_detection_stats(request.user)
    }
    return render(request, 'dashboard/home.html', context)

@login_required
def upload(request, type):
    context = {'type': type}

    if type == 'upload-imagem':
        return render(request, 'dashboard/upload/upload-imagem.html', context)
    elif type == 'upload-video':
        return render(request, 'dashboard/upload/upload-video.html', context)

@login_required
def minhas_deteccoes(request):
    return render(request, 'dashboard/minhas-deteccoes.html')

@login_required
def relatorios(request):
    return render(request, 'dashboard/relatorios.html')

@login_required
def get_detection_image(request, detection_id):
    context = {}
    return render(request, 'dashboard/minhas-deteccoes.html', context)