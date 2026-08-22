from datetime import datetime

def detection_schema(filename, detections):
    return {
        "filename": filename,
        "total_objects": len(detections),
        "detections": detections,
        "timestamp": datetime.utcnow()
    }