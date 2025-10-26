"""
SelfTrainService - ML-based Schedule Optimization
Automatically improves scheduling through machine learning
"""

from .config import CONFIG, TrainingConfig
from .data_store import ScheduleDataStore
from .feature_extractor import FeatureExtractor
from .trainer import ModelTrainer
from .hybrid_scheduler import HybridScheduler
from .retraining_service import (
    RetrainingService,
    get_retraining_service,
    start_retraining_service,
    stop_retraining_service
)

__all__ = [
    'CONFIG',
    'TrainingConfig',
    'ScheduleDataStore',
    'FeatureExtractor',
    'ModelTrainer',
    'HybridScheduler',
    'RetrainingService',
    'get_retraining_service',
    'start_retraining_service',
    'stop_retraining_service',
]

__version__ = '1.0.0'
