from accounts.models import User
from datetime import datetime, timedelta
from dashboard.services.detection import count_detected_classes, get_time_series_data


def get_relatorios_data(user: User, params: dict) -> dict:
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    using_custom_filter = False
    show_all = params.get('show_all') == 'true'
    media_type = params.get('media_type', 'all')
    start_date_str = params.get('start_date')
    end_date_str = params.get('end_date')

    if show_all:
        start_date = datetime(2000, 1, 1)
        end_date = datetime.now()
    elif start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
            using_custom_filter = True
        except ValueError:
            pass

    queryset = user.detections.filter(
        timestamp__gte=start_date,
        timestamp__lte=end_date,
    )

    if media_type == 'image':
        queryset = queryset.filter(upload_type='upload-imagem')
    elif media_type == 'video':
        queryset = queryset.filter(upload_type='upload-video')

    return {
        "total_images": queryset.filter(upload_type='upload-imagem').count(),
        "video_count": queryset.filter(upload_type='upload-video').count(),
        "detected_classes": count_detected_classes(queryset),
        "time_series_data": get_time_series_data(queryset, start_date.date(), end_date.date()),
        "date_filter": {
            "start_date": start_date.strftime('%Y-%m-%d'),
            "end_date": end_date.strftime('%Y-%m-%d'),
            "is_custom": using_custom_filter,
            "show_all": show_all,
        },
        "media_type": media_type,
    }