from ultralytics import YOLO
import cv2
import numpy as np

# Load pretrained model
model = YOLO("yolov8n.pt")  

def detect_from_image(image_path:str):
    """
    Takes an image path and returns a list of detected objects 
    with their confidence scores and bounding box coordinates.
    """
    results = model(image_path)
    detections = []

    for result in results:
        for box in result.boxes:
            detections.append({
                "object": result.names[int(box.cls)],
                "confidence": round(float(box.conf), 2),
                "bbox": {
                    "x1": int(box.xyxy[0][0]),
                    "y1": int(box.xyxy[0][1]),
                    "x2": int(box.xyxy[0][2]),
                    "y2": int(box.xyxy[0][3])
                }
            })

    return detections


