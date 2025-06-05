import torch
from ultralytics import YOLO
import cv2
import numpy as np

def load_model(model_path):
    """Load the YOLOv8 model."""
    try:
        model = YOLO(model_path)
        return model
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        raise

def predict_pill(model, image_path):
    """Predict pill type and dosage from image."""
    try:
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not read image")
        
        # Run prediction
        results = model(image)
        
        # Process results
        if len(results) > 0 and len(results[0].boxes) > 0:
            # Get the highest confidence prediction
            boxes = results[0].boxes
            best_idx = boxes.conf.argmax().item()
            
            # Get class name and confidence
            class_id = int(boxes.cls[best_idx].item())
            confidence = float(boxes.conf[best_idx].item())
            
            # Map class ID to pill name and dosage
            # This is a placeholder - you should replace with your actual class mapping
            pill_classes = {
                0: {"name": "Aspirin", "dosage": "100mg"},
                1: {"name": "Ibuprofen", "dosage": "200mg"},
                2: {"name": "Acetaminophen", "dosage": "500mg"},
                # Add more classes as needed
            }
            
            if class_id in pill_classes:
                return {
                    "pill": pill_classes[class_id]["name"],
                    "dosage": pill_classes[class_id]["dosage"],
                    "confidence": confidence
                }
            else:
                return {
                    "pill": "Unknown",
                    "dosage": "Unknown",
                    "confidence": confidence
                }
        else:
            return {
                "pill": "No pill detected",
                "dosage": "Unknown",
                "confidence": 0.0
            }
            
    except Exception as e:
        print(f"Error predicting pill: {str(e)}")
        return {
            "pill": "Error",
            "dosage": "Unknown",
            "confidence": 0.0
        } 