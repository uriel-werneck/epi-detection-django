from dashboard.services.detection import get_detection_stats
from accounts.models import User
from datetime import date, datetime, timedelta

from dashboard.services.detection import count_detected_classes, get_time_series_data

'''

def relatorios():
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    show_all = request.args.get('show_all') == 'true'
    media_type = request.args.get('media_type', 'all')  
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    using_custom_filter = False
    
    if show_all:
        start_date = datetime(2000, 1, 1)  
        end_date = datetime.now()
        using_custom_filter = False
    elif start_date_str and end_date_str:
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            end_date = end_date.replace(hour=23, minute=59, second=59)
            using_custom_filter = True
        except ValueError:
            flash('Formato de data inválido. Use YYYY-MM-DD.', 'error')
    
    print(f"DEBUG: Date filter - start_date: {start_date}, end_date: {end_date}")
    print(f"DEBUG: Using custom filter: {using_custom_filter}, show_all: {show_all}")
    print(f"DEBUG: Media type filter: {media_type}")
    
    query = Detection.query.filter(
        Detection.user_id == current_user.id,
        Detection.timestamp >= start_date,
        Detection.timestamp <= end_date
    )
    
    if media_type == 'image':
        query = query.filter(Detection.upload_type == 'upload-imagem')
    elif media_type == 'video':
        query = query.filter(Detection.upload_type == 'upload-video')
    
    detections = query.all()
    
    print(f"DEBUG: Found {len(detections)} detections in date range with media type filter: {media_type}")
    
    video_query = query.filter(Detection.upload_type == 'upload-video')
    video_count = video_query.count()
    
    time_series_data = get_time_series_data(current_user.id, start_date, end_date)
    
    detection_stats = {
        "total_images": len(detections),
        "video_count": video_count,
        "detected_classes": get_detected_classes(detections),
        "time_series_data": time_series_data,
        "date_filter": {
            "start_date": start_date.strftime('%Y-%m-%d'),
            "end_date": end_date.strftime('%Y-%m-%d'),
            "is_custom": using_custom_filter,
            "show_all": show_all
        },
        "media_type": media_type  
    }
    
    now = datetime.now()
    
    return render_template("dashboard/relatorios.html", detection_stats=detection_stats, now=now)

'''

# def get_report_stats(user: User, end_date: date, start_date: date, show_all: bool, media_type: str):
#     report_stats = get_detection_stats(user)
#     report_stats['media_type'] = media_type
#     report_stats['date_filter'] = {
#         'end_date': end_date,
#         'start_date': start_date,
#         'show_all': show_all,
#         'media_type': media_type
#     }
#     return report_stats


# def get_report_data(user, filters):
#     detections = get_detection_stats(user)


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