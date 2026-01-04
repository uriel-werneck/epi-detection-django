from ultralytics import YOLO
from django.conf import settings

model = YOLO(settings.YOLO_MODEL_PATH)