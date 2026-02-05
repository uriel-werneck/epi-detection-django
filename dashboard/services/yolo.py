from dashboard.constants import TRANSLATIONS, COLORS
import cv2 as cv
from .yolo_model import model
import os
import datetime


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


def process_video_with_classes(video_path: str, output_path: str) -> dict:
    '''Detecta objetos em um vídeo usando YOLO, gera o vídeo anotado e retorna as estatísticas de detecção.'''

    creation_time = os.path.getctime(video_path)
    formatted_date = datetime.datetime.fromtimestamp(creation_time).strftime('%d/%m/%Y %H:%M:%S')

    # open video file using OpenCV
    cap = cv.VideoCapture(video_path)
    if not cap.isOpened():
        return None

    # Read metadata needed to create the output video
    width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv.CAP_PROP_FPS))

    # configure video writer
    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    out = cv.VideoWriter(output_path, fourcc, fps, (width, height))

    # used to select the frame with the most detections
    frame_info = []  
    frame_idx = 0

    # iterate over all frames in the video
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # convert frame to rgb and run model detection on it
        frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        results = model(frame_rgb, verbose=False)

        if results[0].boxes:
            class_ids = results[0].boxes.cls.cpu().numpy().astype(int)
    
            # translate class names to PT-BR and get boxes
            class_names = [TRANSLATIONS.get(model.names[class_id].lower(), model.names[class_id].lower()) for class_id in class_ids]
            boxes = results[0].boxes.xyxy.cpu().numpy() if results[0].boxes else []
        else:
            class_names = []
            boxes = []

        # draw bounding boxes and labels on the original frame
        frame_with_boxes = draw_bounding_boxes(frame, boxes, class_names)

        # store frame data
        frame_info.append({
            'frame': frame_with_boxes,
            'num_objects': len(class_names),
            'class_names': class_names
        })

        # write processed frame to output video
        out.write(frame_with_boxes)
        frame_idx += 1

    # release video resourses
    cap.release()
    out.release()

    # sort frames by number of detected classes (descending)
    frame_info.sort(key=lambda x: x['num_objects'], reverse=True)

    # return empty data if no frames were processed
    if not frame_info:
        return {
            'detected_classes': [],
            'max_objects': 0,
            'frame_image_bytes': None,
            'frame_filename': None,
            'total_frames': frame_idx,
            'creation_date': formatted_date
        }
    
    # maximum number of objects detected among all frames
    max_objects = frame_info[0]['num_objects']

    # get the frame with the most number of detections
    max_frames = [frame for frame in frame_info if frame['num_objects'] == max_objects]
    selected_frame = max_frames[-1] if max_frames else None
    
    # extract image and detected classes from the selected frame
    selected_image = selected_frame['frame']
    selected_classes = selected_frame['class_names']

    # encode selected frame as JPEG
    _, buffer = cv.imencode('.jpg', selected_image)
    frame_image_bytes = buffer.tobytes()

    # select filename
    frame_filename = f"{os.path.basename(video_path).split('.')[0]}_max_objects_frame.jpg"
    
    # result object
    return {
        'detected_classes': selected_classes,
        'max_objects': max_objects,
        'frame_image_bytes': frame_image_bytes,
        'frame_filename': frame_filename,
        'total_frames': frame_idx,
        'creation_date': formatted_date
    }