from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image
import io
import os
import torch
from utils.history_manager import HistoryManager
from torch.serialization import safe_globals
from ultralytics.nn.tasks import SegmentationModel, DetectionModel
from torch.nn.modules.container import Sequential
from ultralytics.nn.modules.conv import Conv
from ultralytics.nn.modules.block import C2f
from torch.nn.modules.activation import SiLU, ReLU
from torch.nn.modules.conv import Conv2d
from torch.nn.modules.batchnorm import BatchNorm2d
from torch.nn.modules.pooling import MaxPool2d
from torch.nn.modules.upsampling import Upsample
from torch.nn.modules.dropout import Dropout
import base64

# Path setup
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_path = os.path.abspath(os.path.join(current_dir, '..', 'frontend'))
model_path = os.path.abspath(os.path.join(current_dir, '..', 'models', 'yolov8', 'yolov8_model.pt'))

app = Flask(__name__, static_folder=frontend_path, static_url_path='')
CORS(app)

# Initialize history manager
history_manager = HistoryManager()

device = torch.device('cpu')

# Load model with safe_globals context manager
with safe_globals([
    SegmentationModel,
    DetectionModel,
    Conv,
    C2f,
    Sequential,
    torch.nn.Module,
    Conv2d,
    BatchNorm2d,
    ReLU,
    SiLU,
    MaxPool2d,
    Upsample,
    Dropout
]):
    model = YOLO(model_path)

@app.route('/')
def index():
    return send_from_directory(frontend_path, 'index.html')

@app.route('/api/scan', methods=['POST'])
def scan_pill():
    try:
        data = request.get_json()
        image_data = data.get('image')
        if not image_data:
            return jsonify({'success': False, 'error': 'No image data provided'}), 400

        # Decode base64 image
        header, encoded = image_data.split(',', 1)
        img_bytes = base64.b64decode(encoded)
        img = Image.open(io.BytesIO(img_bytes)).convert('RGB')

        # Run YOLOv8 model
        results = model(img)
        boxes = results[0].boxes
        names = model.names

        if not boxes:
            return jsonify({'success': False, 'error': 'No pills detected'}), 200

        # For demo, just use the first detected pill
        box = boxes[0]
        cls_id = int(box.cls[0])
        medication = names[cls_id]
        confidence = f"{box.conf[0]*100:.1f}%"

        result = {
            'success': True,
            'pill': medication,
            'confidence': confidence,
            'dosage': 'Unknown',
            'frequency': 'Unknown',
            'duration': 'Unknown',
            'notes': f'Detected with {confidence} confidence'
        }
        
        if history_manager.add_entry(result):
            return jsonify(result)
        else:
            return jsonify({'success': False, 'error': 'Failed to save to history'}), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        history = history_manager.get_history()
        return jsonify({'success': True, 'history': history})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/history/mark-taken', methods=['POST'])
def mark_as_taken():
    try:
        data = request.json
        timestamp = data.get('timestamp')
        if not timestamp:
            return jsonify({'success': False, 'error': 'Timestamp is required'}), 400
        
        success = history_manager.mark_as_taken(timestamp)
        return jsonify({'success': success})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/history/export', methods=['GET'])
def export_history():
    try:
        return send_file(
            history_manager.history_file,
            as_attachment=True,
            download_name='medication_history.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
