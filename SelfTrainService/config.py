"""
Self-Training Service Configuration
Centralized configuration for model training and retraining
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class TrainingConfig:
    """Configuration for model training"""
    
    # Retraining interval
    RETRAIN_INTERVAL_HOURS: int = 48  # Retrain every 48 hours
    
    # Data requirements
    MIN_SCHEDULES_FOR_TRAINING: int = 100  # Minimum schedules needed
    MIN_SCHEDULES_FOR_RETRAIN: int = 50   # Minimum new schedules for retrain
    
    # Model parameters
    MODEL_VERSION: str = "v1.0.0"
    MODEL_TYPES: list = None  # type: ignore # Will be set in __post_init__
    USE_ENSEMBLE: bool = True  # Use ensemble of best models
    ENSEMBLE_TOP_N: int = 3  # Use top N models for ensemble
    
    # Paths
    DATA_DIR: str = "data/schedules"
    MODEL_DIR: str = "models"
    CHECKPOINT_DIR: str = "checkpoints"
    
    # Training hyperparameters
    TRAIN_TEST_SPLIT: float = 0.2
    VALIDATION_SPLIT: float = 0.1
    EPOCHS: int = 100
    BATCH_SIZE: int = 32
    LEARNING_RATE: float = 0.001
    
    # Feature engineering
    FEATURES: list = None  # type: ignore # Will be set in __post_init__
    TARGET: str = "schedule_quality_score"
    
    # Hybrid mode
    USE_HYBRID: bool = True  # Use both ML and optimization
    ML_CONFIDENCE_THRESHOLD: float = 0.75  # Use ML if confidence > threshold
    
    def __post_init__(self):
        if self.FEATURES is None:
            self.FEATURES = [
                "num_trains",
                "num_available",
                "avg_readiness_score",
                "total_mileage",
                "mileage_variance",
                "maintenance_count",
                "certificate_expiry_count",
                "branding_priority_sum",
                "time_of_day",
                "day_of_week"
            ]
        
        if self.MODEL_TYPES is None:
            self.MODEL_TYPES = [
                "gradient_boosting",
                "random_forest",
                "xgboost",
                "lightgbm",
                "catboost"
            ]


# Global config instance
CONFIG = TrainingConfig()
