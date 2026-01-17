from accounts.models import User
from dashboard.constants import TRANSLATIONS
from datetime import datetime, timedelta
from django.db.models import Sum, Count
from dashboard.models import Detection
from typing import Iterable


def count_detected_classes(detections):
    class_counts = {}
    for detection in detections:
        classes = detection.detected_classes
        for cls in classes:
            if cls and cls in TRANSLATIONS.values():
                class_counts[cls] = class_counts.get(cls, 0) + 1
    return class_counts


def get_time_series_data(detections, start_date=None, end_date=None):
    if end_date is None:
        end_date = datetime.now().date()
    if start_date is None:
        start_date = end_date - timedelta(days=6)

    days_diff = max((end_date - start_date).days, 1)

    formatted_dates = [(start_date + timedelta(days=i)).strftime('%d/%m/%Y') for i in range(days_diff + 1)]
    detections_data = [0] * len(formatted_dates)
    uploads_data = [0] * len(formatted_dates)

    queryset = detections.filter(
        timestamp__date__gte=start_date,
        timestamp__date__lte=end_date
    ).values('timestamp__date').annotate(
        total_detections=Sum('quantity'),
        upload_count=Count('id')
    ).order_by('timestamp__date')

    daily_data = {}
    for row in queryset:
        display_date = row['timestamp__date'].strftime('%d/%m/%Y')
        daily_data[display_date] = {
            'detections': row['total_detections'] or 0,
            'uploads': row['upload_count'] or 0
        }

    for i, date_str in enumerate(formatted_dates):
        if date_str in daily_data:
            detections_data[i] = daily_data[date_str]['detections']
            uploads_data[i] = daily_data[date_str]['uploads']

    return {
        "dates": formatted_dates,
        "detections": detections_data,
        "uploads": uploads_data
    }


def get_detection_stats(user: User):
    detections = user.detections.all()

    total_images = detections.filter(upload_type='upload-imagem').count()
    video_count = detections.filter(upload_type='upload-video').count()
    detected_classes = count_detected_classes(detections)
    time_series_data = get_time_series_data(detections)
    
    detection_stats = {
        "total_images": total_images,
        "video_count": video_count,
        "detected_classes": detected_classes,
        "time_series_data": time_series_data
    }
    return detection_stats


def get_all_classes(detections: Iterable[Detection], sort=True) -> list[str]:
    '''Iterate over detections and return a list of all detected classes.'''

    all_classes = set()

    for detection in detections:
        all_classes.update(detection.detected_classes)

    result = list(all_classes)
    return sorted(result) if sort else result