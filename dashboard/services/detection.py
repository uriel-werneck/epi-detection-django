from accounts.models import User
from dashboard.constants import TRANSLATIONS
from datetime import datetime, timedelta
from django.db.models import Sum, Count


def get_detected_classes(detections):
    class_counts = {}
    for detection in detections:
        classes = detection.detected_classes.split(',')
        for cls in classes:
            if cls and cls in TRANSLATIONS.values():
                class_counts[cls] = class_counts.get(cls, 0) + 1
    return class_counts
