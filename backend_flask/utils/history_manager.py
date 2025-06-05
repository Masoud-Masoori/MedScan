import pandas as pd
import os
from datetime import datetime
import json

class HistoryManager:
    def __init__(self):
        self.history_file = "memory/medication_history.xlsx"
        self.backup_file = "memory/medication_history.json"
        self._ensure_files_exist()

    def _ensure_files_exist(self):
        """Ensure history files exist and create if they don't."""
        os.makedirs("memory", exist_ok=True)
        
        if not os.path.exists(self.history_file):
            # Create new Excel file with headers
            df = pd.DataFrame(columns=[
                'timestamp',
                'medication_name',
                'dosage',
                'frequency',
                'duration',
                'taken',
                'notes'
            ])
            df.to_excel(self.history_file, index=False)
            
            # Create backup JSON file
            with open(self.backup_file, 'w') as f:
                json.dump([], f)

    def add_entry(self, medication_data):
        """Add a new medication entry to history."""
        try:
            # Read existing data
            df = pd.read_excel(self.history_file)
            
            # Add new entry
            new_entry = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'medication_name': medication_data.get('pill', ''),
                'dosage': medication_data.get('dosage', ''),
                'frequency': medication_data.get('frequency', ''),
                'duration': medication_data.get('duration', ''),
                'taken': 'Yes',
                'notes': medication_data.get('notes', '')
            }
            
            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            
            # Save to Excel
            df.to_excel(self.history_file, index=False)
            
            # Update backup JSON
            with open(self.backup_file, 'r') as f:
                history = json.load(f)
            history.append(new_entry)
            with open(self.backup_file, 'w') as f:
                json.dump(history, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error adding history entry: {str(e)}")
            return False

    def get_history(self, limit=50):
        """Get recent medication history."""
        try:
            df = pd.read_excel(self.history_file)
            # Sort by timestamp descending and limit results
            df = df.sort_values('timestamp', ascending=False).head(limit)
            return df.to_dict('records')
        except Exception as e:
            print(f"Error reading history: {str(e)}")
            return []

    def mark_as_taken(self, timestamp):
        """Mark a medication as taken."""
        try:
            df = pd.read_excel(self.history_file)
            df.loc[df['timestamp'] == timestamp, 'taken'] = 'Yes'
            df.to_excel(self.history_file, index=False)
            return True
        except Exception as e:
            print(f"Error marking medication as taken: {str(e)}")
            return False 