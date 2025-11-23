# ML Service - Metro Train Scheduling System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)

A comprehensive machine learning and optimization service for metro train scheduling, featuring synthetic data generation, multi-objective optimization, and a RESTful API for integration.

---

## 🎯 Project Overview

This repository maintains **two main services**:

### 1. **DataService** - Data Generation & Scheduling API
FastAPI-based service that generates synthetic metro data and optimizes daily train schedules.

### 2. **Optimization Algorithms** (greedyOptim)
Multiple optimization algorithms for trainset scheduling including genetic algorithms, particle swarm, simulated annealing, and OR-Tools integration.

### 3. **Self-Training ML Engine** (SelfTrainService) - *Coming Soon*
Adaptive machine learning engine that learns from historical schedules and improves over time.

---

## 🚀 Quick Start

### Installation

```bash
# Navigate to project
cd /home/arpbansal/code/sih2025/mlservice

# Install dependencies
pip install -r requirements.txt
```

### Run Demo

```bash
# Comprehensive demo with full output
python demo_schedule.py

# Quick examples
python quickstart.py
```

### Start API Server

```bash
# Start FastAPI service
python run_api.py

# Access at:
# - http://localhost:8000/docs (Interactive API docs)
# - http://localhost:8000/api/v1/schedule/example (Example schedule)
```

---

## 📚 Key Features

✅ **25-40 trainsets** with realistic health statuses (fully healthy, partial, unavailable)  
✅ **Single bidirectional metro line** with 25 stations (Aluva-Pettah)  
✅ **Full-day scheduling**: 5:00 AM to 11:00 PM operation  
✅ **Real-world constraints**:
  - Maintenance windows and job cards
  - Fitness certificates (rolling stock, signalling, telecom)
  - Branding/advertising priorities
  - Mileage balancing across fleet  
✅ **Multi-objective optimization** with configurable weights  
✅ **RESTful API** with OpenAPI/Swagger documentation  
✅ **Multiple optimization algorithms** (GA, PSO, SA, CMA-ES, NSGA-II, OR-Tools)

---

## 📁 Project Structure

```
mlservice/
├── DataService/              # 🆕 FastAPI data generation & scheduling
│   ├── api.py               # REST API endpoints
│   ├── metro_models.py      # Pydantic data models
│   ├── metro_data_generator.py  # Synthetic data generation
│   ├── schedule_optimizer.py    # Schedule optimization engine
│   └── README.md            # Detailed DataService docs
│
├── greedyOptim/             # Optimization algorithms
│   ├── scheduler.py         # Main scheduling interface
│   ├── genetic_algorithm.py # Genetic algorithm
│   ├── advanced_optimizers.py   # CMA-ES, PSO, SA
│   ├── hybrid_optimizers.py     # Multi-objective, ensemble
│   ├── evaluator.py         # Fitness evaluation
│   └── ...
│
├── SelfTrainService/        # ML training service (future)
│
├── demo_schedule.py         # 🆕 Comprehensive demo
├── quickstart.py            # 🆕 Quick examples
├── run_api.py              # 🆕 API startup script
├── requirements.txt         # Dependencies
├── Dockerfile              # 🆕 Docker container
└── docker-compose.yml      # 🆕 Docker compose
```

---

## 📊 Schedule Output Example

The system generates comprehensive daily schedules:

```json
{
  "schedule_id": "KMRL-2025-10-25-DAWN",
  "generated_at": "2025-10-24T23:45:00+05:30",
  "valid_from": "2025-10-25T05:00:00+05:30",
  "valid_until": "2025-10-25T23:00:00+05:30",
  "depot": "Muttom_Depot",
  
  "trainsets": [
    {
      "trainset_id": "TS-001",
      "status": "REVENUE_SERVICE",
      "priority_rank": 1,
      "assigned_duty": "DUTY-A1",
      "service_blocks": [
        {
          "block_id": "BLK-001",
          "departure_time": "05:30",
          "origin": "Aluva",
          "destination": "Pettah",
          "trip_count": 3,
          "estimated_km": 96
        }
      ],
      "daily_km_allocation": 224,
      "cumulative_km": 145620,
      "fitness_certificates": {...},
      "job_cards": {...},
      "branding": {...},
      "readiness_score": 0.98
    }
  ],
  
  "fleet_summary": {
    "total_trainsets": 30,
    "revenue_service": 22,
    "standby": 4,
    "maintenance": 2,
    "cleaning": 2,
    "availability_percent": 93.3
  },
  
  "optimization_metrics": {...},
  "conflicts_and_alerts": [...],
  "decision_rationale": {...}
}
```

---

## 🔌 API Endpoints

### Generate Schedule

```bash
# Quick generation with defaults
curl -X POST "http://localhost:8000/api/v1/generate/quick?date=2025-10-25&num_trains=30"

# Custom parameters
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2025-10-25",
    "num_trains": 30,
    "num_stations": 25,
    "min_service_trains": 22,
    "min_standby_trains": 3
  }'
```

### Other Endpoints

```bash
# Get example schedule
GET /api/v1/schedule/example

# Get route information
GET /api/v1/route/{num_stations}

# Get train health data
GET /api/v1/trains/health/{num_trains}

# Get depot layout
GET /api/v1/depot/layout

# Health check
GET /health
```

**Full API Documentation**: http://localhost:8000/docs

---

## 🧠 Optimization Algorithms

### Available Methods

| Algorithm | Code | Best For |
|-----------|------|----------|
| Genetic Algorithm | `ga` | General purpose, balanced |
| Particle Swarm | `pso` | Fast convergence |
| Simulated Annealing | `sa` | Avoiding local optima |
| CMA-ES | `cmaes` | Continuous optimization |
| NSGA-II | `nsga2` | Multi-objective |
| Ensemble | `ensemble` | Best overall results |
| OR-Tools CP-SAT | `cp-sat` | Constraint satisfaction |

### Usage Example

```python
from greedyOptim.scheduler import TrainsetSchedulingOptimizer

optimizer = TrainsetSchedulingOptimizer(data, config)
result = optimizer.optimize(method='ga')
```

---

## 🐳 Docker Deployment

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

Or use Docker directly:

```bash
docker build -t metro-scheduler .
docker run -p 8000:8000 metro-scheduler
```

---

## 💡 Use Cases

1. **Daily Operations**: Generate optimized schedules for metro operations
2. **Maintenance Planning**: Balance service and maintenance requirements
3. **Fleet Management**: Optimize train utilization and mileage balancing
4. **Advertising**: Maximize branded train exposure
5. **What-if Analysis**: Test different scenarios and constraints
6. **Data Generation**: Create synthetic data for ML model training

---

## 🎯 General Backend Flow

**Single Endpoint Strategy** (Future Enhancement):

```
User Request
    ↓
Main Endpoint
    ↓
    ├→ Try ML Engine (SelfTrainService)
    │   └→ If available & confident → Return ML prediction
    │
    └→ Fallback to Optimization Algo (greedyOptim)
        └→ Return optimized schedule
```

Users can also explicitly choose:
- ML-based prediction
- Optimization algorithms
- Hybrid approach

---

## 📖 Documentation

- **DataService API**: See [DataService/README.md](DataService/README.md)
- **Optimization**: See [docs/integrate.md](docs/integrate.md)
- **Quick Examples**: Run `python quickstart.py`
- **Full Demo**: Run `python demo_schedule.py`

---

## 🔧 Configuration

### Key Parameters

```python
{
    "num_trains": 25-40,           # Fleet size
    "num_stations": 25,            # Route stations
    "min_service_trains": 20,      # Min active trains
    "min_standby_trains": 2,       # Min standby
    "max_daily_km_per_train": 300, # Max km/train/day
    "balance_mileage": true,       # Enable balancing
    "prioritize_branding": true    # Prioritize ads
}
```

### Optimization Weights

```python
{
    "service_readiness": 0.35,    # 35%
    "mileage_balancing": 0.25,    # 25%
    "branding_priority": 0.20,    # 20%
    "operational_cost": 0.20      # 20%
}
```

---

## 🧪 Testing

```bash
# Run comprehensive demo
python demo_schedule.py

# Run quick examples
python quickstart.py

# Run unit tests
python test_optimization.py
```

---

## 📦 Dependencies

```
fastapi>=0.104.1
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
ortools>=9.14.6206
python-multipart>=0.0.6
```

Install with:
```bash
pip install -r requirements.txt
```

---

## 🛠️ Development

### Setup

```bash
# Clone repository
git clone [repository-url]
cd mlservice

# Install dependencies
pip install -r requirements.txt

# Run in development mode
uvicorn DataService.api:app --reload
```

### Adding New Features

1. Data models: Edit `DataService/metro_models.py`
2. Optimization: Add to `greedyOptim/`
3. API endpoints: Edit `DataService/api.py`

---

## 🐛 Troubleshooting

**Port already in use**:
```bash
# Use different port
uvicorn DataService.api:app --port 8001
```

**Import errors**:
```bash
# Add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**Package conflicts**:
```bash
# Use virtual environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📈 Performance

- **Optimization time**: ~300-500ms for 30 trains
- **API response time**: <1s for full schedule generation
- **Memory usage**: ~50-100MB
- **Scalability**: Tested up to 40 trains

---

## 🏆 Built For

**Smart India Hackathon 2025** 🇮🇳

This project demonstrates:
- Real-world metro scheduling optimization
- Modern API design with FastAPI
- Multiple AI/ML algorithms
- Production-ready architecture
- Comprehensive documentation

---

## 👥 Team

- [Add team member names]

---

## 📞 Contact & Support

- **GitHub**: SIHProjectio/ML-service
- **Issues**: [GitHub Issues]
- **Docs**: http://localhost:8000/docs (when running)

---

## 📄 License

[Add license information]

---

**Last Updated**: October 24, 2025

**Version**: 1.0.0

4. Constraint Satisfaction
Maintenance Window Compliance: How well schedules accommodate required maintenance slots
Turnaround Time Adherence: Success rate in meeting minimum turnaround requirements
Battery/Energy Constraints: If applicable, energy consumption profiles
5. Multi-Objective Optimization Trade-offs
Pareto Front Analysis: Trade-offs between minimizing fleet size vs. maximizing service quality
Cost vs. Service Level: Operating cost reduction while maintaining service standards
Passenger Satisfaction vs. Operational Efficiency: Balance achieved
6. Scalability Analysis
Performance with Route Length: How algorithms perform with different numbers of stations (13-25 stations tested)
Fleet Size Scaling: Results for 5, 10, 15, 20, 25 train fleets
Time Complexity: Algorithm runtime growth with problem size
7. Comparative Analysis
Baseline Comparison: Your optimized schedules vs. current Kochi Metro schedules
Algorithm Comparison:
Greedy optimizer results
Genetic algorithm results
OR-Tools CP-SAT results
Hybrid approach results
Best Performing Method: Identify which optimizer works best for different scenarios
8. Real-World Applicability
Kochi Metro Specifications Met:
Average operating speed: 35 km/h maintained
Maximum speed: 80 km/h respected
Route distance: 25.612 km covered
22 stations serviced
Operational Hours: 5:00 AM to 11:00 PM coverage achieved
Peak Hour Performance: 5-7 minute headways during rush hours
9. Data Generation Validation
Synthetic Data Realism: Statistical comparison with actual metro operations
Distribution Analysis: Passenger demand patterns, breakdown frequencies, delay distributions
Sensor Data Accuracy: GPS coordinates, speed profiles match real-world patterns
10. API Performance
Response Times: Average API latency for schedule generation requests
Throughput: Requests handled per second
Success Rate: Percentage of valid schedules generated
Quantitative Metrics You Can Report:
Schedule generation time: X seconds for Y trains
Fleet size reduction: Z% fewer trains needed vs. baseline
Total operating cost reduction: ₹X per day
Passenger wait time improvement: Y% reduction
Algorithm success rate: X% of runs produce valid schedules
Average headway variance: ±X minutes
Coverage percentage: Y% of demand satisfied
Energy efficiency: X kWh per km improvement
Visualization Opportunities:
Gantt charts of optimized train schedules
Fleet utilization timelines
Headway consistency graphs (peak vs. off-peak)
Algorithm performance comparison tables
Pareto fronts for multi-objective optimization
Cost-benefit analysis charts
Convergence plots for genetic algorithm
Scalability curves (runtime vs. problem size)
You should present these results with:

Tables showing comparative metrics
Graphs visualizing schedule quality and optimization performance
Statistical analysis proving improvements are significant
Real test cases using Kochi Metro parameters
