import pandas as pd
import os
from datetime import datetime
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HistoryManager:
    def __init__(self):
        self.history_file = "memory/medication_history.xlsx"
        self.backup_file = "memory/medication_history.json"
        self._ensure_files_exist()

    def _ensure_files_exist(self):
        """Ensure history files exist and create if they don't."""
        try:
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
                logger.info("Created new history files")
        except Exception as e:
            logger.error(f"Error creating history files: {str(e)}")
            raise

    def _sync_files(self, df):
        """Synchronize Excel and JSON files."""
        try:
            # Save to Excel
            df.to_excel(self.history_file, index=False)
            
            # Update backup JSON
            history = df.to_dict('records')
            with open(self.backup_file, 'w') as f:
                json.dump(history, f, indent=2)
            
            logger.info("Successfully synchronized history files")
            return True
        except Exception as e:
            logger.error(f"Error synchronizing files: {str(e)}")
            return False

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
                'taken': 'No',  # Default to 'No' when first added
                'notes': medication_data.get('notes', '')
            }
            
            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            
            # Synchronize files
            if self._sync_files(df):
                logger.info("Successfully added new history entry")
                return True
            return False
        except Exception as e:
            logger.error(f"Error adding history entry: {str(e)}")
            return False

    def get_history(self, limit=50):
        """Get recent medication history."""
        try:
            df = pd.read_excel(self.history_file)
            # Sort by timestamp descending and limit results
            df = df.sort_values('timestamp', ascending=False).head(limit)
            return df.to_dict('records')
        except Exception as e:
            logger.error(f"Error reading history: {str(e)}")
            return []

    def mark_as_taken(self, timestamp):
        """Mark a medication as taken."""
        try:
            df = pd.read_excel(self.history_file)
            mask = df['timestamp'] == timestamp
            if not any(mask):
                logger.warning(f"No entry found with timestamp: {timestamp}")
                return False
                
            df.loc[mask, 'taken'] = 'Yes'
            
            # Synchronize files
            if self._sync_files(df):
                logger.info(f"Successfully marked medication as taken for timestamp: {timestamp}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error marking medication as taken: {str(e)}")
            return False 