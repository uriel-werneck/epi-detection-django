from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .services.detection import get_detection_stats
from .upload_config import UPLOAD_CONFIG
from .models import Detection
from django.urls import reverse
from urllib.parse import urlencode
from django.core.paginator import Paginator
from .utils.pagination import iter_pages
from .utils.pagination import get_detection_data


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
            path = reverse('dashboard:upload', kwargs={'type': type})
            query = urlencode({'detection': detection.id})
            return redirect(f'{path}?{query}')
    else:
        form = form_class()

    detection_id = request.GET.get('detection')
    detection = None
    if detection_id:
        detection = get_object_or_404(
            Detection,
            id=detection_id,
            user=request.user
        )

    context = {
        'form': form,
        'detection': detection
    }
    
    return render(request, template_name, context)


@login_required
def minhas_deteccoes(request):
    all_objects = request.user.detections.all().order_by('-timestamp')

    page_number = request.GET.get('page') or 1
    date_filter = request.GET.get('date')
    class_filter = request.GET.get('class')

    paginator = Paginator(all_objects, 9)
    page_obj = paginator.get_page(page_number)

    pagination = page_obj
    all_classes = None
    date_filter = None
    class_filter = None
    pagination_list = iter_pages(int(page_number), paginator.num_pages)

    context = {
        'detection_data': get_detection_data(page_obj),
        'pagination': pagination,
        'all_classes': all_classes,
        'current_date_filter': date_filter,
        'current_class_filter': class_filter,
        'iter_pages': pagination_list
    }

    return render(request, 'dashboard/minhas-deteccoes.html', context)


@login_required
def relatorios(request):
    return render(request, 'dashboard/relatorios.html')


@login_required
def get_detection_image(request, detection_id):
    context = {}
    return render(request, 'dashboard/minhas-deteccoes.html', context)


@login_required
def download_image(request, detection_id):
    detection = get_object_or_404(
        Detection,
        user=request.user,
        id=detection_id,
    )

    if not detection.image_data:
        raise Http404('File not found')
    
    return FileResponse(
        detection.image_data.open('rb'),
        as_attachment=True,
        filename=detection.file_name
    )