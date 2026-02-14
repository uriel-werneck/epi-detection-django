from dashboard.models import Detection
from dashboard.utils.images import opencv_image_to_django_file
import cv2 as cv
import numpy as np
from .yolo import (
    process_image_with_yolo,
    draw_bounding_boxes,
    process_video_with_classes
)
import tempfile
import os
from uuid import uuid4
from django.conf import settings
from django.core.files.base import ContentFile, File


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
    '''Orquestra o upload, processamento YOLO e persistência de vídeos no banco de dados.'''

    video = cleaned_data.get('video')
    if not video:
        raise ValueError('Video not provided')
        
    # save uploaded video to a temp folder
    temp_dir = tempfile.mkdtemp()
    temp_video_path = os.path.join(temp_dir, video.name)

    with open(temp_video_path, 'wb+') as destination:
        for chunk in video.chunks():
            destination.write(chunk)

    # prepare output video path
    unique_id = str(uuid4())
    name, extension = os.path.splitext(video.name)
    output_filename = f'processed_{name}_{unique_id}{extension}'
    output_dir = tempfile.mkdtemp()
    output_path = os.path.join(output_dir, output_filename)

    # process video
    result_info = process_video_with_classes(
        video_path=temp_video_path,
        output_path=output_path
    )

    if not result_info:
        raise RuntimeError('Error processing video!')
    
    # create detection instance
    detection = Detection(
        user=user,
        file_name=video.name,
        detection_data=result_info['detected_classes'],
        upload_type='upload-video',
        quantity = result_info['max_objects'],
        detected_classes=result_info['detected_classes'],
        is_stored_in_db = True
    )

    # attach processed video
    with open(output_path, 'rb') as f:
        detection.video_data.save(
            output_filename,
            File(f),
            save=False
        )

    # attach frame image
    if result_info.get('frame_image_bytes'):
        detection.image_data.save(
            result_info['frame_filename'],
            ContentFile(result_info['frame_image_bytes']),
            save=False
        )

    detection.save()

    # cleanup
    try:
        os.remove(temp_video_path)
        os.remove(output_path)
        os.rmdir(temp_dir)
        os.rmdir(output_dir)
    except OSError:
        pass

    return detection