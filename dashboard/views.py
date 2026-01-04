from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages
from .services.detection import get_detection_stats
from .upload_config import UPLOAD_CONFIG
from .models import Detection
from django.urls import reverse


# Create your views here.
@login_required
def home(request):
    context = {
        'detection_stats': get_detection_stats(request.user)
    }
    return render(request, 'dashboard/home.html', context)


@login_required
def upload(request, type):
    config = UPLOAD_CONFIG.get(type)
    if not config:
        raise Http404('Invalid upload type')
    
    form_class = config.get('form')
    template_name = config.get('template_name')
    service = config.get('service')
    
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            detection = service(request.user, form.cleaned_data)
            messages.success(request, 'Imagem processada com sucesso! Clique em "Ver no Dashboard" para visualizar as estatísticas atualizadas.')
            return redirect(f'{reverse('dashboard:upload', kwargs={'type': type})}?detection={detection.id}')
    else:
        form = form_class()

    detection_id = request.GET.get('detection')
    detection = None

    if detection_id:
        detection = Detection.objects.filter(
            id=detection_id,
            user=request.user
        ).first()

    context = {
        'form': form,
        'detection': detection
    }
    
    return render(request, template_name, context)


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