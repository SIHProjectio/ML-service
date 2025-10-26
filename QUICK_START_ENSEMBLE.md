# Quick Reference - Ensemble ML System

## What Was Added

🎯 **5 Machine Learning Models** working together:
1. Gradient Boosting (scikit-learn)
2. Random Forest (scikit-learn)  
3. XGBoost (Extreme Gradient Boosting)
4. LightGBM (Microsoft's fast GB)
5. CatBoost (Yandex's categorical GB)

🎯 **Ensemble Voting**: All models vote, weighted by performance

🎯 **Auto-Retraining**: Every 48 hours with new data

🎯 **Simplified Code**: No library availability checks (assumes installed)

## Installation

```bash
# Install all ML libraries
pip install -r requirements.txt
```

This installs:
- `xgboost==2.0.3`
- `lightgbm==4.1.0`  
- `catboost==1.2.2`
- Plus existing: scikit-learn, numpy, fastapi, etc.

## Usage

### 1️⃣ Train All Models (First Time)

```bash
python SelfTrainService/train_model.py
```

This will:
- Generate 150 sample schedules
- Train all 5 models
- Show performance metrics
- Save models to `models/` directory

Example output:
```
Training gradient_boosting...
  gradient_boosting: R² = 0.8234, RMSE = 13.45

Training xgboost...
  xgboost: R² = 0.8543, RMSE = 12.34

Best model: xgboost
Ensemble weights:
  gradient_boosting: 0.195
  xgboost: 0.215
  ...
```

### 2️⃣ Start Auto-Retraining Service

```bash
python SelfTrainService/start_retraining.py
```

This will:
- Run in background
- Retrain every 48 hours
- Update ensemble weights
- Keep models fresh

### 3️⃣ Start API Service

```bash
cd DataService
python api.py
```

API runs on `http://localhost:8000`

### 4️⃣ Test Ensemble System

```bash
python SelfTrainService/test_ensemble.py
```

Tests:
- Configuration
- Model initialization
- Data generation
- Feature extraction
- Training pipeline
- Predictions

## How It Works

### Ensemble Prediction

When you request a schedule:

1. **Hybrid Scheduler** checks ML confidence
2. If **confidence > 75%**: Use ensemble ML
   - All 5 models make predictions
   - Weighted average (better models weighted more)
   - Return prediction + confidence
3. If **confidence < 75%**: Use optimization fallback
   - Traditional OR-Tools optimization
   - Guaranteed valid schedule

### Ensemble Weights

Models weighted by R² score:

```
xgboost: 0.215 (best, highest weight)
lightgbm: 0.208
gradient_boosting: 0.195
catboost: 0.195
random_forest: 0.187
```

Better models = more influence on final prediction

### Confidence Calculation

**Ensemble Mode**:
- High agreement between models = high confidence
- Low agreement = low confidence
- Formula: `confidence = 1.0 - (std_dev / 50)`

**Single Model Mode**:
- Based on prediction value
- Higher quality predictions = higher confidence

## Key Files

### Configuration
- `SelfTrainService/config.py` - All settings

### Training
- `SelfTrainService/trainer.py` - Multi-model training
- `SelfTrainService/train_model.py` - Manual training script

### Service
- `SelfTrainService/retraining_service.py` - Background retraining
- `SelfTrainService/start_retraining.py` - Service starter

### Testing
- `SelfTrainService/test_ensemble.py` - Test suite

### Integration
- `SelfTrainService/hybrid_scheduler.py` - ML + Optimization decision

## Configuration Options

Edit `SelfTrainService/config.py`:

```python
# Which models to use
MODEL_TYPES = [
    "gradient_boosting",
    "random_forest",
    "xgboost",
    "lightgbm",
    "catboost"
]

# Ensemble settings
USE_ENSEMBLE = True  # Use weighted voting
ENSEMBLE_TOP_N = 3   # Use top N models (if needed)

# Retraining
RETRAIN_INTERVAL_HOURS = 48  # Every 2 days
MIN_SCHEDULES_FOR_TRAINING = 100  # Need 100 schedules

# Hybrid mode
ML_CONFIDENCE_THRESHOLD = 0.75  # Use ML if > 75% confidence
```

## Checking Model Performance

After training, check files in `models/`:

**Latest training results**:
```bash
cat models/training_summary.json
```

**All training history**:
```bash
cat models/training_history.json
```

**Model info**:
```python
from SelfTrainService.trainer import ModelTrainer
trainer = ModelTrainer()
info = trainer.get_model_info()
print(info)
```

Output:
```json
{
  "models_loaded": ["gradient_boosting", "random_forest", "xgboost", "lightgbm", "catboost"],
  "best_model": "xgboost",
  "ensemble_enabled": true,
  "ensemble_weights": {...},
  "last_trained": "2024-01-15T10:30:00",
  "should_retrain": false
}
```

## API Endpoints

All endpoints from `DataService/api.py` work as before:

```bash
# Generate schedule (uses hybrid scheduler internally)
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "num_trains": 30,
    "start_hour": 5,
    "end_hour": 23
  }'
```

The hybrid scheduler will:
1. Try ML ensemble prediction
2. Check confidence
3. Use ML if confident, otherwise optimization

## Troubleshooting

### Models not training?
```bash
# Check if enough data
python -c "from SelfTrainService.data_store import ScheduleDataStore; print(ScheduleDataStore().count_schedules())"

# Need at least 100 schedules
python SelfTrainService/train_model.py
```

### Import errors?
```bash
# Install dependencies
pip install -r requirements.txt

# Verify installations
python -c "import xgboost, lightgbm, catboost; print('All installed!')"
```

### Check if models trained?
```bash
ls -la models/
# Should see: models_latest.pkl, training_history.json
```

## Benefits

✅ **Better Accuracy**: 5 models > 1 model  
✅ **Robustness**: Less overfitting  
✅ **Confidence**: Model agreement shows reliability  
✅ **Adaptability**: Weights update with retraining  
✅ **Safety**: Falls back to optimization if needed  

## What Changed from Single Model

**Before** (single model):
```python
model = GradientBoostingRegressor()
model.fit(X, y)
prediction = model.predict(features)
```

**After** (ensemble):
```python
models = {
    "gradient_boosting": GradientBoostingRegressor(),
    "xgboost": XGBRegressor(),
    "lightgbm": LGBMRegressor(),
    "catboost": CatBoostRegressor(),
    "random_forest": RandomForestRegressor()
}

# Train all
for model in models.values():
    model.fit(X, y)

# Predict with weighted voting
predictions = [model.predict(features) for model in models.values()]
ensemble_prediction = weighted_average(predictions, ensemble_weights)
```

## Complete Workflow

```bash
# 1. Install
pip install -r requirements.txt

# 2. Train initial models
python SelfTrainService/train_model.py

# 3. Test ensemble
python SelfTrainService/test_ensemble.py

# 4. Start auto-retraining (Terminal 1)
python SelfTrainService/start_retraining.py

# 5. Start API (Terminal 2)
cd DataService
python api.py

# 6. Test API (Terminal 3)
python test_api.py
```

## Summary

You now have:
- ✅ 5 ML models working together
- ✅ Ensemble voting for better predictions
- ✅ Auto-retraining every 48 hours
- ✅ Clean code (no availability checks)
- ✅ Best model tracking
- ✅ Performance monitoring
- ✅ Testing suite
- ✅ Complete documentation

Ready to use! 🚀
