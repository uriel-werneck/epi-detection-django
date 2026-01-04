from .forms import ImageUploadForm, VideoUploadForm
from .services.upload import (
    handle_image_upload,
    handle_video_upload
)

UPLOAD_CONFIG = {
    'upload-imagem': {
        'form': ImageUploadForm,
        'template_name': 'dashboard/upload/upload-imagem.html',
        'service': handle_image_upload
    },
    'upload-video': {
        'form': VideoUploadForm,
        'template_name': 'dashboard/upload/upload-video.html',
        'service': handle_video_upload
    }
}