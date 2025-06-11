# MedScan - Medication Management System

![Seneca College](https://img.shields.io/badge/Capstone-Seneca%20College-red)

> **Note:** This project is a Capstone Project for Seneca College.
> **Disclaimer:** This software is provided for educational purposes only as part of a student capstone project. It is not intended for medical, diagnostic, or commercial use. Use at your own risk.

MedScan is a local-first medication management application designed to help elderly users manage their medications safely and effectively. The system uses computer vision to identify pills and OCR to read prescription information.

## Features

- 🎯 Pill detection using YOLOv8
- 📝 Prescription text extraction using Tesseract OCR
- ⏰ Medication reminders and scheduling
- 👴 Senior-friendly user interface
- 💾 Local-first operation (no cloud dependencies)
- 📱 Offline functionality
- 📊 Excel-based history tracking with JSON backup
- 📝 Comprehensive logging system
- 🔄 Synchronized data storage

## Project Structure

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
│       ├── history_manager.py # History tracking with sync
│       └── train_yolo.py     # YOLOv8 training script
│
├── models/                    # ML models
│   └── yolov8/               # YOLOv8 models
│
├── memory/                   # Local storage
│   ├── medication_history.xlsx  # Excel history file
│   └── medication_history.json  # JSON backup file
│
└── README.md                # This file
```

## Prerequisites

- Python 3.8 or higher
- Tesseract OCR installed on your system
- Webcam or camera for pill scanning
- Modern web browser

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Masoud-Masoori/MedScan.git
cd MedScan
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
cd backend_flask
pip install -r requirements.txt
```

4. Install Tesseract OCR:
- Windows: Download and install from https://github.com/UB-Mannheim/tesseract/wiki
- Linux: `sudo apt-get install tesseract-ocr`
- macOS: `brew install tesseract`

## Usage

1. Start the Flask server:
```bash
cd backend_flask
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

3. Use the application:
- Click "Scan Pill" to identify a medication
- Set reminders for medication times
- View medication history
- Export history to Excel

## Features in Detail

### Pill Detection
- Uses YOLOv8 for accurate pill identification
- Works with various pill shapes and colors
- Provides confidence scores
- Real-time detection with webcam support

### Prescription OCR
- Extracts text from prescription images
- Identifies medication names, dosages, and instructions
- Supports multiple prescription formats

### Reminder System
- Set custom medication schedules
- Daily, weekly, or custom frequency
- Visual and audio notifications

### History Tracking
- Excel-based storage for medication history
- JSON backup for data redundancy
- Automatic synchronization between storage formats
- Status tracking (taken/pending)
- Export functionality
- Comprehensive logging system for debugging

### Data Synchronization
- Automatic synchronization between Excel and JSON formats
- Backup system to prevent data loss
- Logging system for tracking operations
- Error handling and recovery

## Development

### Logging System
The application includes a comprehensive logging system that tracks:
- Application startup and shutdown
- Pill detection operations
- History management operations
- File synchronization events
- Error conditions and recovery attempts

Logs can be found in the application's console output and can be redirected to a file if needed.

### Error Handling
The application includes robust error handling for:
- File operations
- Data synchronization
- Pill detection
- OCR processing
- History management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- YOLOv8 by Ultralytics
- Tesseract OCR
- Flask framework
- Python logging system 