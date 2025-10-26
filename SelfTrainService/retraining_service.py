"""
Automatic Retraining Service
Background service that retrains model on schedule
"""
import time
import threading
from datetime import datetime, timedelta
from typing import Optional
from .config import CONFIG
from .trainer import ModelTrainer


class RetrainingService:
    """Background service for automatic model retraining"""
    
    def __init__(self, trainer: Optional[ModelTrainer] = None):
        self.trainer = trainer or ModelTrainer()
        self.running = False
        self.thread = None
        self.check_interval_minutes = 60  # Check every hour
    
    def start(self):
        """Start the retraining service"""
        if self.running:
            print("Retraining service already running")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        
        print(f"Retraining service started (check interval: {self.check_interval_minutes} min)")
        print(f"Will retrain every {CONFIG.RETRAIN_INTERVAL_HOURS} hours")
    
    def stop(self):
        """Stop the retraining service"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        print("Retraining service stopped")
    
    def _run_loop(self):
        """Main loop for retraining service"""
        while self.running:
            try:
                # Check if retraining is needed
                if self.trainer.should_retrain():
                    print(f"\n[{datetime.now()}] Starting automatic retraining...")
                    result = self.trainer.train()
                    
                    if result.get("success"):
                        summary = result
                        print(f"✓ Retraining completed successfully")
                        print(f"  - Models trained: {', '.join(summary.get('models_trained', []))}")
                        print(f"  - Best model: {summary.get('best_model', 'N/A')}")
                        best_metrics = summary.get('best_metrics', {})
                        print(f"  - Best R²: {best_metrics.get('test_r2', 0):.4f}")
                        print(f"  - Best RMSE: {best_metrics.get('test_rmse', 0):.4f}")
                        if summary.get('ensemble_weights'):
                            print(f"  - Ensemble models: {len(summary['ensemble_weights'])}")
                    else:
                        reason = result.get("reason", result.get("error", "Unknown"))
                        print(f"✗ Retraining skipped: {reason}")
                
            except Exception as e:
                print(f"Error in retraining loop: {e}")
            
            # Sleep until next check
            for _ in range(self.check_interval_minutes * 60):
                if not self.running:
                    break
                time.sleep(1)
    
    def force_retrain(self):
        """Force immediate retraining"""
        print(f"\n[{datetime.now()}] Forcing model retraining...")
        result = self.trainer.train(force=True)
        return result
    
    def get_status(self) -> dict:
        """Get service status"""
        return {
            "running": self.running,
            "check_interval_minutes": self.check_interval_minutes,
            "retrain_interval_hours": CONFIG.RETRAIN_INTERVAL_HOURS,
            "model_info": self.trainer.get_model_info()
        }


# Global service instance
_service = None


def get_retraining_service() -> RetrainingService:
    """Get or create global retraining service"""
    global _service
    if _service is None:
        _service = RetrainingService()
    return _service


def start_retraining_service():
    """Start global retraining service"""
    service = get_retraining_service()
    service.start()
    return service


def stop_retraining_service():
    """Stop global retraining service"""
    global _service
    if _service:
        _service.stop()
        _service = None
