"""
ML Model Trainer for Schedule Optimization
Handles model training and retraining with multiple models and ensemble
"""
import os
import pickle
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Tuple
import numpy as np

from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import xgboost as xgb
import catboost as cb
import lightgbm as lgb

from .config import CONFIG
from .data_store import ScheduleDataStore
from .feature_extractor import FeatureExtractor


class ModelTrainer:
    """Train and manage ML models for schedule optimization"""
    
    def __init__(self, model_dir: Optional[str] = None):
        self.model_dir = Path(model_dir or CONFIG.MODEL_DIR)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        self.data_store = ScheduleDataStore()
        self.feature_extractor = FeatureExtractor()
        
        self.models = {}  # Dictionary of trained models
        self.model_scores = {}  # Performance scores for each model
        self.ensemble_weights = {}  # Weights for ensemble
        self.best_model_name = None
        self.last_trained = None
        self.training_history = []
    
    def _get_model(self, model_name: str):
        """Get model instance by name"""
        if model_name == "gradient_boosting":
            return GradientBoostingRegressor(
                n_estimators=CONFIG.EPOCHS,
                learning_rate=CONFIG.LEARNING_RATE,
                random_state=42
            )
        
        elif model_name == "random_forest":
            return RandomForestRegressor(
                n_estimators=CONFIG.EPOCHS,
                random_state=42,
                n_jobs=-1
            )
        
        elif model_name == "xgboost":
            return xgb.XGBRegressor(
                n_estimators=CONFIG.EPOCHS,
                learning_rate=CONFIG.LEARNING_RATE,
                random_state=42,
                verbosity=0
            )
        
        elif model_name == "lightgbm":
            return lgb.LGBMRegressor(
                n_estimators=CONFIG.EPOCHS,
                learning_rate=CONFIG.LEARNING_RATE,
                random_state=42,
                verbose=-1
            )
        
        elif model_name == "catboost":
            return cb.CatBoostRegressor(
                iterations=CONFIG.EPOCHS,
                learning_rate=CONFIG.LEARNING_RATE,
                random_state=42,
                verbose=False
            )
        
        return None
    
    def should_retrain(self) -> bool:
        """Check if model should be retrained"""
        if not self.last_trained:
            # Never trained
            return True
        
        # Check time since last training
        hours_since_training = (
            datetime.now() - self.last_trained
        ).total_seconds() / 3600
        
        if hours_since_training >= CONFIG.RETRAIN_INTERVAL_HOURS:
            # Check if enough new data
            new_schedules = self.data_store.get_schedules_since(self.last_trained)
            if len(new_schedules) >= CONFIG.MIN_SCHEDULES_FOR_RETRAIN:
                return True
        
        return False
    
    def train(self, force: bool = False) -> Dict:
        """Train or retrain all models"""
        
        if not force and not self.should_retrain():
            return {
                "success": False,
                "reason": "Retraining not needed yet"
            }
        
        # Load data
        schedules = self.data_store.load_schedules()
        
        if len(schedules) < CONFIG.MIN_SCHEDULES_FOR_TRAINING:
            return {
                "success": False,
                "reason": f"Not enough data. Need {CONFIG.MIN_SCHEDULES_FOR_TRAINING}, have {len(schedules)}"
            }
        
        # Prepare dataset
        X, y = self.feature_extractor.prepare_dataset(schedules)
        
        if len(X) == 0:
            return {
                "success": False,
                "error": "No valid features extracted"
            }
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=CONFIG.TRAIN_TEST_SPLIT, random_state=42
        )
        
        # Train all models
        self.models = {}
        self.model_scores = {}
        all_metrics = {}
        
        for model_name in CONFIG.MODEL_TYPES:
            print(f"Training {model_name}...")
            model = self._get_model(model_name)
            
            if model is None:
                print(f"Skipping {model_name} - not available")
                continue
            
            # Train model
            model.fit(X_train, y_train)
            
            # Evaluate
            train_pred = model.predict(X_train)
            test_pred = model.predict(X_test)

            train_r2 = r2_score(y_train, train_pred) # type: ignore
            test_r2 = r2_score(y_test, test_pred)   # type: ignore
            test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))  # type: ignore
            
            self.models[model_name] = model
            self.model_scores[model_name] = test_r2
            
            all_metrics[model_name] = {
                "train_r2": train_r2,
                "test_r2": test_r2,
                "train_rmse": np.sqrt(mean_squared_error(y_train, train_pred)), # type: ignore
                "test_rmse": test_rmse
            }
            
            print(f"  {model_name}: R² = {test_r2:.4f}, RMSE = {test_rmse:.4f}")
        
        # Compute ensemble weights based on performance
        if CONFIG.USE_ENSEMBLE and len(self.models) > 1:
            total_score = sum(self.model_scores.values())
            self.ensemble_weights = {
                name: score / total_score 
                for name, score in self.model_scores.items()
            }
        else:
            self.ensemble_weights = {}
        
        # Find best model
        if self.model_scores:
            self.best_model_name = max(self.model_scores.items(), key=lambda x: x[1])[0]
        
        # Save model
        self.last_trained = datetime.now()
        self.save_model()
        
        # Record training history
        history_entry = {
            "timestamp": self.last_trained.isoformat(),
            "metrics": all_metrics,
            "best_model": self.best_model_name,
            "ensemble_weights": self.ensemble_weights,
            "config": {
                "models_trained": list(self.models.keys()),
                "version": CONFIG.MODEL_VERSION
            }
        }
        self.training_history.append(history_entry)
        self._save_history()
        
        return {
            "success": True,
            "models_trained": list(self.models.keys()),
            "best_model": self.best_model_name,
            "metrics": all_metrics,
            "ensemble_weights": self.ensemble_weights,
            "samples_used": len(X),
            "timestamp": self.last_trained.isoformat()
        }
    
    def predict(self, features: Dict[str, float], use_ensemble: bool = True) -> Tuple[float, float]:
        """Predict schedule quality and confidence"""
        if not self.models:
            self.load_model()
        
        if not self.models:
            return 0.0, 0.0
        
        # Convert features to vector
        feature_vector = np.array([
            [features.get(f, 0.0) for f in CONFIG.FEATURES]
        ])
        
        if use_ensemble and CONFIG.USE_ENSEMBLE and self.ensemble_weights:
            # Ensemble prediction
            prediction = 0.0
            for model_name, weight in self.ensemble_weights.items():
                if model_name in self.models:
                    pred = self.models[model_name].predict(feature_vector)[0]
                    prediction += weight * pred
            
            # Confidence based on ensemble agreement
            predictions = [
                self.models[name].predict(feature_vector)[0]
                for name in self.models.keys()
            ]
            std_dev = np.std(predictions)
            confidence = max(0.5, min(1.0, 1.0 - (std_dev / 50)))  # Higher agreement = higher confidence
        else:
            # Use best single model
            best_model = self.models.get(self.best_model_name)
            if best_model is None:
                best_model = list(self.models.values())[0]
            
            prediction = best_model.predict(feature_vector)[0]
            confidence = min(1.0, 0.8 + (prediction / 100) * 0.2)
        
        return float(prediction), float(confidence)
    
    def save_model(self):
        """Save all models to disk"""
        if not self.models:
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_path = self.model_dir / f"models_{timestamp}.pkl"
        latest_path = self.model_dir / "models_latest.pkl"
        
        model_data = {
            "models": self.models,
            "ensemble_weights": self.ensemble_weights,
            "best_model_name": self.best_model_name,
            "last_trained": self.last_trained,
            "config": {
                "version": CONFIG.MODEL_VERSION,
                "features": CONFIG.FEATURES,
                "models_trained": list(self.models.keys())
            }
        }
        
        with open(model_path, 'wb') as f:
            pickle.dump(model_data, f)
        
        with open(latest_path, 'wb') as f:
            pickle.dump(model_data, f)
    
    def load_model(self) -> bool:
        """Load models from disk"""
        latest_path = self.model_dir / "models_latest.pkl"
        
        if not latest_path.exists():
            return False
        
        try:
            with open(latest_path, 'rb') as f:
                model_data = pickle.load(f)
            
            self.models = model_data["models"]
            self.ensemble_weights = model_data.get("ensemble_weights", {})
            self.best_model_name = model_data.get("best_model_name")
            self.last_trained = model_data.get("last_trained")
            return True
        except Exception as e:
            print(f"Error loading models: {e}")
            return False
    
    def _save_history(self):
        """Save training history"""
        history_path = self.model_dir / "training_history.json"
        with open(history_path, 'w') as f:
            json.dump(self.training_history, f, indent=2, default=str)
    
    def get_model_info(self) -> Dict:
        """Get information about current models"""
        if not self.models:
            self.load_model()
        
        return {
            "models_loaded": list(self.models.keys()) if self.models else [],
            "best_model": self.best_model_name,
            "ensemble_enabled": CONFIG.USE_ENSEMBLE,
            "ensemble_weights": self.ensemble_weights,
            "last_trained": self.last_trained.isoformat() if self.last_trained else None,
            "should_retrain": self.should_retrain(),
            "schedules_available": self.data_store.count_schedules(),
            "training_runs": len(self.training_history)
        }
