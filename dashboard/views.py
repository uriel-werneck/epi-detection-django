from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'dashboard/home.html')

def upload(request, type):
    context = {'type': type}

    if type == 'upload-imagem':
        return render(request, 'dashboard/upload/upload-imagem.html', context)
    elif type == 'upload-video':
        return render(request, 'dashboard/upload/upload-video.html', context)

def minhas_deteccoes(request):
    return render(request, 'dashboard/minhas-deteccoes.html')

def relatorios(request):
    return render(request, 'dashboard/relatorios.html')

def get_detection_image(request, detection_id):
    context = {}
    return render(request, 'dashboard/minhas-deteccoes.html', context)