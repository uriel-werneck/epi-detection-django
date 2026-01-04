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


def draw_bounding_boxes(image, boxes, class_names=None):
    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = map(int, box)

        if class_names and i < len(class_names):
            class_name = class_names[i]
            label = f"{class_name}"

            cv.rectangle(image, (x1, y1), (x2, y2), COLORS[class_name]['body'], 5)

            (compr_texto, larg_texto), _ = cv.getTextSize(label, cv.FONT_HERSHEY_DUPLEX, 1.5, 2)
            caixa_id = cv.rectangle(image, (x1, y1 - 29), (x1 + compr_texto, y1), COLORS[class_name]['body'], -1)
            cv.putText(caixa_id, label, (x1, y1 - 3), cv.FONT_HERSHEY_DUPLEX, 1.5, COLORS[class_name]['text'], 2)
            
    return image