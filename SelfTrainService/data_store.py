"""
Data Storage and Management for Self-Training
Handles schedule data collection and storage
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from .config import CONFIG


class ScheduleDataStore:
    """Store and manage schedule data for training"""
    
    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = Path(data_dir or CONFIG.DATA_DIR)
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def save_schedule(self, schedule: Dict, metadata: Optional[Dict] = None) -> str:
        """Save a schedule to storage"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        schedule_id = schedule.get("schedule_id", f"schedule_{timestamp}")
        filename = f"{schedule_id}_{timestamp}.json"
        filepath = self.data_dir / filename
        
        data = {
            "schedule": schedule,
            "metadata": metadata or {},
            "saved_at": datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        return str(filepath)
    
    def load_schedules(self, limit: Optional[int] = None) -> List[Dict]:
        """Load schedules from storage"""
        schedules = []
        files = sorted(self.data_dir.glob("*.json"), reverse=True)
        
        if limit:
            files = files[:limit]
        
        for filepath in files:
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    schedules.append(data)
            except Exception as e:
                print(f"Error loading {filepath}: {e}")
        
        return schedules
    
    def count_schedules(self) -> int:
        """Count total schedules in storage"""
        return len(list(self.data_dir.glob("*.json")))
    
    def get_schedules_since(self, since: datetime) -> List[Dict]:
        """Get schedules created after a specific time"""
        schedules = []
        
        for filepath in self.data_dir.glob("*.json"):
            if os.path.getmtime(filepath) > since.timestamp():
                try:
                    with open(filepath, 'r') as f:
                        schedules.append(json.load(f))
                except Exception as e:
                    print(f"Error loading {filepath}: {e}")
        
        return schedules
    
    def clear_old_schedules(self, keep_count: int = 1000):
        """Keep only the most recent schedules"""
        files = sorted(self.data_dir.glob("*.json"), reverse=True)
        
        for filepath in files[keep_count:]:
            try:
                filepath.unlink()
            except Exception as e:
                print(f"Error deleting {filepath}: {e}")
