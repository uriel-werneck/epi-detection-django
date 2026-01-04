from dashboard.constants import TRANSLATIONS, COLORS
import cv2 as cv
from .yolo_model import model


def process_image_with_yolo(image):
    image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    results = model(image_rgb, conf=0.12)
    if not results or not results[0].boxes:
        return [], []
    boxes = results[0].boxes.xyxy.cpu().numpy() if results[0].boxes else []
    classes = results[0].boxes.cls.cpu().numpy().astype(int) if results[0].boxes else []
    class_names = [TRANSLATIONS.get(model.names[cls].lower(), model.names[cls].lower()) for cls in classes]
    return class_names, boxes


