from django.core.files.base import ContentFile
import numpy as np
import cv2 as cv
import uuid


def opencv_image_to_django_file(image: np.ndarray):
    success, buffer = cv.imencode('.jpg', image)
    if not success:
        raise ValueError('Failed to encode image')
    
    return ContentFile(
        content=buffer,
        name=f'{uuid.uuid4()}.jpg'
    )