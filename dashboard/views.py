from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    return render(request, 'dashboard/home.html')

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