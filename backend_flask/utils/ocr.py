import pytesseract
import cv2
import numpy as np

def extract_text_from_image(image_path):
    """Extract text from prescription image using Tesseract OCR."""
    try:
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not read image")
        
        # Preprocess image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        
        # Extract text
        text = pytesseract.image_to_string(thresh)
        
        # Process text to extract relevant information
        lines = text.split('\n')
        prescription_info = {
            'medication': '',
            'dosage': '',
            'frequency': '',
            'duration': ''
        }
        
        # Common frequency patterns
        frequency_patterns = {
            'daily': ['daily', 'once a day', '1x daily', 'qd'],
            'twice': ['twice daily', '2x daily', 'bid'],
            'three times': ['three times daily', '3x daily', 'tid'],
            'four times': ['four times daily', '4x daily', 'qid'],
            'weekly': ['weekly', 'once a week', 'qw'],
            'monthly': ['monthly', 'once a month']
        }
        
        for line in lines:
            line = line.strip().lower()
            if not line:
                continue
                
            # Extract medication name (usually the first non-empty line)
            if not prescription_info['medication'] and len(line) > 3:
                prescription_info['medication'] = line.title()
            
            # Extract dosage
            if 'mg' in line or 'ml' in line or 'g' in line:
                prescription_info['dosage'] = line
            
            # Extract frequency
            for freq, patterns in frequency_patterns.items():
                if any(pattern in line for pattern in patterns):
                    prescription_info['frequency'] = freq
                    break
            
            # Extract duration
            if any(word in line for word in ['days', 'weeks', 'months']):
                prescription_info['duration'] = line
        
        return prescription_info
        
    except Exception as e:
        print(f"Error extracting text: {str(e)}")
        return {
            'medication': 'Error',
            'dosage': 'Unknown',
            'frequency': 'Unknown',
            'duration': 'Unknown'
        } 