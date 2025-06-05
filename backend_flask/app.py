from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image
import io
import os
import torch
from utils.history_manager import HistoryManager

# Path setup to locate frontend folder
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))

app = Flask(__name__, static_folder=frontend_path, static_url_path='')
CORS(app)

# Initialize history manager
history_manager = HistoryManager()

device = torch.device('cpu')
model = YOLO("best.pt")

@app.route('/')
def index():
    return send_from_directory(frontend_path, 'index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if "image" not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        image = request.files["image"]
        img = Image.open(io.BytesIO(image.read()))

        results = model(img, device='cpu')
        predictions = results[0].boxes
        names = model.names

        labels = []
        for box in predictions:
            cls_id = int(box.cls[0])
            labels.append(names[cls_id])

        return jsonify({"predictions": list(set(labels))})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        history = history_manager.get_history()
        return jsonify({
            'success': True,
            'history': history
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/history/mark-taken', methods=['POST'])
def mark_as_taken():
    try:
        data = request.json
        timestamp = data.get('timestamp')
        if not timestamp:
            return jsonify({
                'success': False,
                'error': 'Timestamp is required'
            }), 400
        
        success = history_manager.mark_as_taken(timestamp)
        return jsonify({
            'success': success
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/history/export', methods=['GET'])
def export_history():
    try:
        # Get the Excel file path
        excel_path = history_manager.history_file
        
        # Send the file
        return send_file(
            excel_path,
            as_attachment=True,
            download_name='medication_history.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/scan', methods=['POST'])
def scan_pill():
    try:
        data = request.json
        image_data = data.get('image')
        
        # Process the image and get results
        # ... existing image processing code ...
        
        # Add to history
        history_manager.add_entry({
            'pill': result['pill'],
            'dosage': result['dosage'],
            'frequency': result.get('frequency', ''),
            'duration': result.get('duration', ''),
            'notes': result.get('notes', '')
        })
        
        return jsonify({
            'success': True,
            'pill': result['pill'],
            'dosage': result['dosage'],
            'frequency': result.get('frequency', ''),
            'duration': result.get('duration', ''),
            'confidence': result['confidence']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
