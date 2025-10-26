# Metro Train Scheduling Service

This repository maintains two intelligent services that work together to optimize metro train scheduling:

## 1. Optimization Engine (DataService)
Traditional constraint-based optimization using OR-Tools for guaranteed valid schedules.

## 2. Self-Training ML Engine (SelfTrainService)
**Multi-Model Ensemble Learning** that continuously improves from real scheduling data.

### ML Models Included:
- **Gradient Boosting** (scikit-learn)
- **Random Forest** (scikit-learn)
- **XGBoost** - Extreme Gradient Boosting
- **LightGBM** - Microsoft's high-performance gradient boosting
- **CatBoost** - Yandex's categorical boosting

### Ensemble Strategy:
- Trains all 5 models simultaneously
- Uses weighted ensemble voting for predictions
- Weights based on individual model performance (R² score)
- Automatically selects best single model as fallback
- Higher prediction confidence when models agree

## General Flow

**Call a single endpoint** - the hybrid scheduler will internally decide:

1. **ML First**: Try ensemble ML prediction
   - If confidence > 75% → Use ML-generated schedule
   - Models vote weighted by performance
   
2. **Optimization Fallback**: If ML confidence low
   - Falls back to traditional OR-Tools optimization
   - Guaranteed valid schedule

3. **Continuous Learning**: Every 48 hours
   - Automatically retrains all 5 models
   - Uses accumulated real schedule data
   - Updates ensemble weights
   - Identifies new best model

## Key Features

✅ **Multi-Model Ensemble**: 5 state-of-the-art ML models working together  
✅ **Auto-Retraining**: Retrains every 48 hours with new data  
✅ **Confidence-Based**: Uses ML when confident, optimization as safety net  
✅ **Performance Tracking**: Monitors each model's accuracy  
✅ **Weighted Voting**: Better models have more influence  
✅ **Best Model Selection**: Always knows which single model performs best  

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate Initial Training Data
```bash
python SelfTrainService/train_model.py
```

### 3. Start Auto-Retraining Service
```bash
python SelfTrainService/start_retraining.py
```

### 4. Start API Service
```bash
cd DataService
python api.py
```

## Testing

### Test Ensemble System
```bash
python SelfTrainService/test_ensemble.py
```

### Test API Endpoints
```bash
python test_api.py
```

## Model Performance

After training, check model performance:
- **Training summary**: `models/training_summary.json`
- **Training history**: `models/training_history.json`
- **Ensemble weights**: Shows contribution of each model

Example output:
```json
{
  "best_model": "xgboost",
  "ensemble_weights": {
    "gradient_boosting": 0.195,
    "random_forest": 0.187,
    "xgboost": 0.215,
    "lightgbm": 0.208,
    "catboost": 0.195
  }
}
```

## Configuration

Edit `SelfTrainService/config.py`:

```python
RETRAIN_INTERVAL_HOURS = 48  # How often to retrain
MODEL_TYPES = [              # Which models to use
    "gradient_boosting",
    "random_forest", 
    "xgboost",
    "lightgbm",
    "catboost"
]
USE_ENSEMBLE = True          # Enable ensemble voting
ML_CONFIDENCE_THRESHOLD = 0.75  # Min confidence to use ML
```

## Architecture

```
┌─────────────────┐
│   API Request   │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│  Hybrid Scheduler   │
└────────┬────────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐  ┌──────────────┐
│   ML   │  │ Optimization │
│Ensemble│  │   (OR-Tools) │
└───┬────┘  └──────┬───────┘
    │              │
    │ >75%    <75% │
    │ confidence   │
    │              │
    └──────┬───────┘
           │
           ▼
    ┌────────────┐
    │  Schedule  │
    └────────────┘
```

## Ensemble Advantages

1. **Robustness**: Multiple models reduce overfitting risk
2. **Accuracy**: Ensemble typically outperforms single models
3. **Confidence**: Agreement between models indicates reliability
4. **Adaptability**: Different models capture different patterns
5. **Fault Tolerance**: If one model fails, others continue

## Documentation

- **Implementation Details**: See `docs/integrate.md`
- **Multi-Objective Optimization**: See `multi_obj_optimize.md`
- **API Reference**: See `DataService/api.py` docstrings

## Project Structure

```
mlservice/
├── DataService/           # Optimization & API
│   ├── api.py            # FastAPI service
│   ├── metro_models.py   # Data models
│   ├── metro_data_generator.py
│   └── schedule_optimizer.py
├── SelfTrainService/      # ML ensemble
│   ├── config.py         # Configuration
│   ├── trainer.py        # Multi-model training
│   ├── data_store.py     # Data persistence
│   ├── feature_extractor.py
│   ├── hybrid_scheduler.py
│   ├── retraining_service.py
│   ├── train_model.py    # Manual training
│   ├── test_ensemble.py  # Test suite
│   └── start_retraining.py
└── requirements.txt
```

