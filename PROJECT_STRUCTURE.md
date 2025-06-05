# MedScan Project Structure

```
medscan/
├── frontend/                    # Frontend application
│   ├── index.html              # Main page
│   ├── scan.html               # Pill scanning page
│   ├── reminder.html           # Reminder settings page
│   ├── history.html            # Medication history page
│   └── static/                 # Static assets
│       ├── style.css           # Main stylesheet
│       └── script.js           # Frontend JavaScript
│
├── backend_flask/              # Flask backend application
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   └── utils/                 # Utility modules
│       ├── predict.py         # Pill detection logic
│       ├── ocr.py            # Prescription text extraction
│       ├── LLM_ocr.py        # LLM-based OCR
│       ├── NER.py            # Named Entity Recognition
│       ├── Trocr.py          # Transformer OCR
│       └── train_yolo.py     # YOLOv8 training script
│
├── models/                    # ML models
│   ├── yolov8/               # YOLOv8 models
│   │   └── yolov8_model.pt   # Trained pill detection model
│   └── ocr/                  # OCR models
│
├── tests/                    # Test suite
│   ├── data/                # Test data
│   ├── unit/               # Unit tests
│   └── integration/        # Integration tests
│
├── memory/                  # Local storage
│   └── reminders.json      # Reminder data
│
├── README.md               # Project documentation
└── PROJECT_STRUCTURE.md    # This file
```

## Directory Descriptions

### Frontend
The frontend directory contains all the web interface files. The application is designed to be senior-friendly with large text, high contrast, and simple navigation.

### Backend
The Flask backend handles all server-side logic, including:
- Pill detection using YOLOv8
- Prescription text extraction using OCR
- Reminder management
- Local data storage

### Models
Contains all machine learning models:
- YOLOv8 model for pill detection
- OCR models for prescription text extraction

### Tests
Organized test suite:
- Unit tests for individual components
- Integration tests for end-to-end functionality
- Test data for model validation

### Memory
Local storage for application data:
- Reminder information
- Temporary files
- User preferences

## Development Guidelines

1. Frontend Development:
   - Use senior-friendly design principles
   - Maintain high contrast and large text
   - Keep navigation simple and intuitive

2. Backend Development:
   - Follow PEP 8 style guide
   - Document all functions and classes
   - Include error handling

3. Testing:
   - Write tests for all new features
   - Maintain test coverage
   - Use test data appropriately

4. Model Management:
   - Keep models in version control
   - Document model versions and performance
   - Maintain training scripts

5. Data Management:
   - Use local storage for user data
   - Implement proper error handling
   - Maintain data integrity 