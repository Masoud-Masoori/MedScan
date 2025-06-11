# MedScan Technical Documentation

## Frontend-Backend Connection Architecture

### 1. Overview
The MedScan application uses a client-server architecture where:
- Frontend: HTML, CSS, and JavaScript running in the browser
- Backend: Flask server handling API requests and ML operations
- Communication: RESTful API endpoints with JSON data exchange

### 2. Key Components

#### 2.1 Frontend Structure
```
frontend/
├── index.html          # Main landing page
├── scan.html          # Pill scanning interface
├── history.html       # Medication history view
├── reminder.html      # Reminder settings
└── static/
    ├── style.css      # Styling
    └── script.js      # Frontend logic
```

#### 2.2 Backend Structure
```
backend_flask/
├── app.py            # Main Flask application
├── requirements.txt  # Dependencies
└── utils/
    ├── history_manager.py  # Data management
    ├── predict.py         # ML predictions
    └── ocr.py            # Text extraction
```

### 3. API Endpoints and Frontend Integration

#### 3.1 Pill Scanning Flow
```javascript
// Frontend (script.js)
async function scanPill(imageData) {
    try {
        const response = await fetch('/api/scan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: imageData })
        });
        const result = await response.json();
        displayResult(result);
    } catch (error) {
        handleError(error);
    }
}
```

```python
# Backend (app.py)
@app.route('/api/scan', methods=['POST'])
def scan_pill():
    try:
        data = request.get_json()
        image_data = data.get('image')
        # Process image with YOLOv8
        results = model(img)
        # Return detection results
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
```

#### 3.2 History Management
```javascript
// Frontend (script.js)
async function getHistory() {
    const response = await fetch('/api/history');
    const data = await response.json();
    updateHistoryTable(data.history);
}
```

```python
# Backend (app.py)
@app.route('/api/history', methods=['GET'])
def get_history():
    try:
        history = history_manager.get_history()
        return jsonify({'success': True, 'history': history})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
```

### 4. Data Flow

1. **Image Capture to Detection**:
   - User captures image in frontend
   - Image converted to base64
   - Sent to `/api/scan` endpoint
   - Backend processes with YOLOv8
   - Results returned to frontend

2. **History Management**:
   - Frontend requests history via `/api/history`
   - Backend reads from Excel/JSON
   - Data synchronized between formats
   - Results displayed in UI

3. **Reminder System**:
   - Frontend sets reminders
   - Data stored in local storage
   - Notifications handled by browser

### 5. Key Technologies Used

1. **Frontend**:
   - HTML5/CSS3 for UI
   - JavaScript (ES6+) for logic
   - Fetch API for HTTP requests
   - Local Storage for persistence

2. **Backend**:
   - Flask for API server
   - YOLOv8 for pill detection
   - Pandas for data management
   - OpenCV for image processing

3. **Data Storage**:
   - Excel for primary storage
   - JSON for backup
   - Synchronized updates

### 6. Error Handling

1. **Frontend**:
```javascript
function handleError(error) {
    console.error('Error:', error);
    showNotification('Error: ' + error.message, 'error');
}
```

2. **Backend**:
```python
try:
    # Operation code
except Exception as e:
    logger.error(f"Error: {str(e)}")
    return jsonify({'success': False, 'error': str(e)}), 500
```

### 7. Security Considerations

1. **Data Protection**:
   - Local-first architecture
   - No sensitive data transmission
   - Input validation on both ends

2. **Error Prevention**:
   - Input sanitization
   - Type checking
   - Error boundaries

### 8. Testing and Debugging

1. **Frontend Testing**:
   - Browser console for debugging
   - Network tab for API monitoring
   - Local storage inspection

2. **Backend Testing**:
   - Flask debug mode
   - Logging system
   - Error tracking

### 9. Deployment

1. **Local Development**:
```bash
# Start backend
cd backend_flask
python app.py

# Access frontend
http://localhost:5000
```

2. **Production Considerations**:
   - Static file serving
   - CORS configuration
   - Error handling
   - Logging setup

### 10. Future Improvements

1. **Planned Enhancements**:
   - Real-time notifications
   - Offline support
   - Mobile responsiveness
   - Enhanced ML models

2. **Scalability**:
   - Database integration
   - Cloud deployment
   - User authentication
   - Multi-user support

## Common Questions and Answers

### Q1: How does the frontend communicate with the backend?
A: The frontend uses the Fetch API to make HTTP requests to Flask endpoints. Data is exchanged in JSON format.

### Q2: How is data synchronized between Excel and JSON?
A: The HistoryManager class handles synchronization through the `_sync_files` method, ensuring both formats stay updated.

### Q3: How does the pill detection work?
A: The system uses YOLOv8 for object detection. Images are processed through the model, which returns bounding boxes and confidence scores.

### Q4: How is error handling implemented?
A: Both frontend and backend implement comprehensive error handling with try-catch blocks and proper error reporting.

### Q5: How is the application secured?
A: The application uses a local-first approach, input validation, and proper error handling to ensure security.

## Code Examples for Key Features

### 1. Frontend-Backend Connection
```javascript
// Frontend API call
async function callAPI(endpoint, data) {
    const response = await fetch(`/api/${endpoint}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    return await response.json();
}
```

### 2. Data Synchronization
```python
# Backend synchronization
def _sync_files(self, df):
    try:
        # Save to Excel
        df.to_excel(self.history_file, index=False)
        
        # Update JSON backup
        history = df.to_dict('records')
        with open(self.backup_file, 'w') as f:
            json.dump(history, f, indent=2)
        
        return True
    except Exception as e:
        logger.error(f"Error synchronizing files: {str(e)}")
        return False
```

### 3. Error Handling
```python
# Backend error handling
@app.errorhandler(Exception)
def handle_error(error):
    logger.error(f"Unhandled error: {str(error)}")
    return jsonify({
        'success': False,
        'error': str(error)
    }), 500
```

This documentation provides a comprehensive overview of the technical aspects of the MedScan application, focusing on the frontend-backend connection and key implementation details. It should help in explaining the project to your professor and answering any technical questions they might have. 