from dashboard.models import Detection
from dashboard.utils.images import opencv_image_to_django_file
import cv2 as cv
import numpy as np
from .yolo import (
    process_image_with_yolo,
    draw_bounding_boxes
)


def handle_image_upload(user, cleaned_data):
    uploaded_file = cleaned_data.get('image')

    # convert uploaded file to opencv image
    file_bytes = uploaded_file.read()
    np_array = np.frombuffer(file_bytes, np.uint8)
    image = cv.imdecode(np_array, cv.IMREAD_COLOR)

    class_names, boxes = process_image_with_yolo(image)
    image_with_boxes = draw_bounding_boxes(image, boxes, class_names)
    image_with_boxes = opencv_image_to_django_file(image_with_boxes)

    detection = Detection.objects.create(
        user=user,
        file_name=uploaded_file.name,
        detection_data=','.join(class_names),
        upload_type='upload-imagem',
        quantity=len(class_names),
        detected_classes=class_names,
        image_data=image_with_boxes,
        is_stored_in_db=True
    )

    return detection


def handle_video_upload(user, cleaned_data):
    video = cleaned_data.get('video')
    print(cleaned_data)
    print(video)