"""
Hybrid Scheduler - Combines ML and Optimization
Uses ML when confident, falls back to optimization
"""
from typing import Dict, Optional, Tuple
from datetime import datetime

from .config import CONFIG
from .trainer import ModelTrainer


class HybridScheduler:
    """Combine ML predictions with optimization algorithms"""
    
    def __init__(self):
        self.trainer = ModelTrainer()
        self.trainer.load_model()
    
    def should_use_ml(self, features: Dict[str, float]) -> Tuple[bool, float]:
        """Determine if ML should be used based on confidence"""
        if not CONFIG.USE_HYBRID:
            return False, 0.0
        
        if not self.trainer.models:
            return False, 0.0
        
        # Get prediction and confidence
        _, confidence = self.trainer.predict(features)
        
        use_ml = confidence >= CONFIG.ML_CONFIDENCE_THRESHOLD
        return use_ml, confidence
    
    def get_schedule_recommendation(
        self,
        schedule_request: Dict,
        ml_available: bool = True
    ) -> Dict:
        """Get scheduling recommendation with method selection"""
        
        # Extract basic features from request
        features = {
            "num_trains": schedule_request.get("num_trains", 25),
            "time_of_day": datetime.now().hour,
            "day_of_week": datetime.now().weekday(),
        }
        
        # Determine which method to use
        use_ml, confidence = self.should_use_ml(features)
        
        recommendation = {
            "use_ml": use_ml and ml_available,
            "confidence": confidence,
            "threshold": CONFIG.ML_CONFIDENCE_THRESHOLD,
            "method": "ml" if (use_ml and ml_available) else "optimization",
            "reason": self._get_reason(use_ml, ml_available, confidence)
        }
        
        return recommendation
    
    def _get_reason(self, use_ml: bool, ml_available: bool, confidence: float) -> str:
        """Get human-readable reason for method selection"""
        if not ml_available:
            return "ML model not available, using optimization"
        
        if not CONFIG.USE_HYBRID:
            return "Hybrid mode disabled, using optimization"
        
        if use_ml:
            return f"ML confidence ({confidence:.2f}) above threshold ({CONFIG.ML_CONFIDENCE_THRESHOLD})"
        else:
            return f"ML confidence ({confidence:.2f}) below threshold ({CONFIG.ML_CONFIDENCE_THRESHOLD}), using optimization"
    
    def record_schedule_feedback(self, schedule: Dict, quality_score: Optional[float] = None):
        """Record schedule for future training"""
        from .data_store import ScheduleDataStore
        
        store = ScheduleDataStore()
        metadata = {
            "recorded_at": datetime.now().isoformat(),
            "quality_score": quality_score
        }
        store.save_schedule(schedule, metadata)
