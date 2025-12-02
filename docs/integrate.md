 
# GreedyOptim API Integration Guide

## Endpoints

### GET /health

Response:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-25T00:17:15.053513",
  "service": "greedyoptim-api"
}
```

---

### GET /methods

Response:
```json
{
  "available_methods": {
    "ga": {
      "name": "Genetic Algorithm",
      "description": "Evolutionary optimization using selection, crossover, and mutation",
      "typical_time": "medium",
      "solution_quality": "high"
    },
    "cmaes": {
      "name": "CMA-ES",
      "description": "Covariance Matrix Adaptation Evolution Strategy",
      "typical_time": "medium-high",
      "solution_quality": "very high"
    },
    "pso": {
      "name": "Particle Swarm Optimization",
      "description": "Swarm intelligence-based optimization",
      "typical_time": "medium",
      "solution_quality": "high"
    },
    "sa": {
      "name": "Simulated Annealing",
      "description": "Probabilistic optimization inspired by metallurgy",
      "typical_time": "medium",
      "solution_quality": "medium-high"
    },
    "nsga2": {
      "name": "NSGA-II",
      "description": "Non-dominated Sorting Genetic Algorithm (multi-objective)",
      "typical_time": "high",
      "solution_quality": "very high"
    },
    "adaptive": {
      "name": "Adaptive Optimizer",
      "description": "Automatically selects best algorithm",
      "typical_time": "high",
      "solution_quality": "very high"
    },
    "ensemble": {
      "name": "Ensemble Optimizer",
      "description": "Runs multiple algorithms in parallel",
      "typical_time": "high",
      "solution_quality": "highest"
    }
  },
  "default_method": "ga",
  "recommended_for_speed": "ga",
  "recommended_for_quality": "ensemble"
}
```

---

## POST /schedule - Full Schedule Response Structure

The `/schedule` endpoint returns a comprehensive schedule with service blocks and timing details.

### Response Structure Overview

```
FullScheduleResponse
├── schedule_id: string
├── generated_at: string (ISO datetime)
├── valid_from: string (ISO datetime)
├── valid_until: string (ISO datetime)
├── depot: string
├── trainsets: TrainsetScheduleResponse[]
├── fleet_summary: FleetSummaryResponse
├── optimization_metrics: OptimizationMetricsResponse
└── alerts: AlertResponse[]
```

---

### TrainsetScheduleResponse

Each trainset in the schedule has the following structure:

| Field | Type | Description |
|-------|------|-------------|
| `trainset_id` | string | Unique identifier (e.g., "TS-001") |
| `status` | string | Current status: `REVENUE_SERVICE`, `STANDBY`, `MAINTENANCE` |
| `readiness_score` | float | Score from 0.0 to 1.0 indicating operational readiness |
| `daily_km_allocation` | float | Planned kilometers for the day |
| `cumulative_km` | float | Total kilometers accumulated |
| `assigned_duty` | string? | Duty assignment identifier |
| `priority_rank` | int? | Priority ranking for service assignment |
| `service_blocks` | ServiceBlockResponse[]? | List of assigned service blocks (for REVENUE_SERVICE) |
| `stabling_bay` | string? | Assigned stabling bay (for STANDBY) |
| `standby_reason` | string? | Reason for standby status |
| `maintenance_type` | string? | Type of maintenance: `PREVENTIVE`, `CORRECTIVE`, `OVERHAUL` |
| `ibl_bay` | string? | IBL bay assignment (for MAINTENANCE) |
| `estimated_completion` | string? | Estimated maintenance completion time |
| `alerts` | string[]? | List of alerts for this trainset |

---

### ServiceBlockResponse

Service blocks represent scheduled work periods for a trainset:

| Field | Type | Description |
|-------|------|-------------|
| `block_id` | string | Unique block identifier (e.g., "BLK-001") |
| `departure_time` | string | Block start time (HH:MM format) |
| `origin` | string | Starting station |
| `destination` | string | Ending station |
| `trip_count` | int | Number of trips in this block |
| `estimated_km` | float | Total kilometers for this block |
| `journey_time_minutes` | float? | Total journey time in minutes |
| `period` | string? | Time period: `EARLY_MORNING`, `MORNING_PEAK`, `MIDDAY`, `EVENING_PEAK`, `LATE_EVENING` |
| `is_peak` | bool | Whether this is a peak hour block |
| `trips` | TripResponse[]? | Detailed trip information |

---

### TripResponse

Each trip within a service block:

| Field | Type | Description |
|-------|------|-------------|
| `trip_id` | string | Unique trip identifier |
| `trip_number` | int | Sequential trip number |
| `direction` | string | Direction: `UP` or `DOWN` |
| `origin` | string | Origin station |
| `destination` | string | Destination station |
| `departure_time` | string | Departure time (HH:MM) |
| `arrival_time` | string | Arrival time (HH:MM) |
| `stops` | StationStopResponse[] | List of all station stops |

---

### StationStopResponse

Each station stop within a trip:

| Field | Type | Description |
|-------|------|-------------|
| `station_code` | string | Station code (e.g., "ALV") |
| `station_name` | string | Full station name (e.g., "Aluva") |
| `arrival_time` | string? | Arrival time at this station |
| `departure_time` | string? | Departure time from this station |
| `distance_from_origin_km` | float | Distance from trip origin in km |
| `platform` | int? | Platform number |

---

### FleetSummaryResponse

| Field | Type | Description |
|-------|------|-------------|
| `total_trainsets` | int | Total number of trainsets in fleet |
| `revenue_service` | int | Number in revenue service |
| `standby` | int | Number on standby |
| `maintenance` | int | Number in maintenance |
| `availability_percent` | float | Fleet availability percentage |

---

### OptimizationMetricsResponse

| Field | Type | Description |
|-------|------|-------------|
| `fitness_score` | float | Overall optimization fitness score |
| `method` | string | Optimization method used (ga, pso, cmaes, etc.) |
| `mileage_variance_coefficient` | float | Variance in mileage distribution |
| `total_planned_km` | float | Total planned kilometers for the day |
| `optimization_runtime_ms` | int | Time taken for optimization in milliseconds |

---

### AlertResponse

| Field | Type | Description |
|-------|------|-------------|
| `trainset_id` | string | Trainset this alert relates to |
| `severity` | string | Alert severity: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL` |
| `alert_type` | string | Type of alert |
| `message` | string | Human-readable alert message |

---

## Example Response (Simplified)

```json
{
  "schedule_id": "SCH-20251202-001",
  "generated_at": "2025-12-02T10:30:00",
  "valid_from": "2025-12-02T05:00:00",
  "valid_until": "2025-12-02T23:30:00",
  "depot": "Muttom Depot",
  
  "trainsets": [
    {
      "trainset_id": "TS-001",
      "status": "REVENUE_SERVICE",
      "readiness_score": 0.95,
      "daily_km_allocation": 280.5,
      "cumulative_km": 125000.0,
      "assigned_duty": "DUTY-A1",
      "priority_rank": 1,
      "service_blocks": [
        {
          "block_id": "BLK-001",
          "departure_time": "06:00",
          "origin": "Aluva",
          "destination": "Pettah",
          "trip_count": 4,
          "estimated_km": 104.8,
          "journey_time_minutes": 180,
          "period": "MORNING_PEAK",
          "is_peak": true,
          "trips": [
            {
              "trip_id": "TRIP-001",
              "trip_number": 1,
              "direction": "DOWN",
              "origin": "Aluva",
              "destination": "Pettah",
              "departure_time": "06:00",
              "arrival_time": "06:45",
              "stops": [
                {
                  "station_code": "ALV",
                  "station_name": "Aluva",
                  "arrival_time": null,
                  "departure_time": "06:00",
                  "distance_from_origin_km": 0.0,
                  "platform": 1
                },
                {
                  "station_code": "PTH",
                  "station_name": "Pettah",
                  "arrival_time": "06:45",
                  "departure_time": null,
                  "distance_from_origin_km": 26.2,
                  "platform": 2
                }
              ]
            }
          ]
        }
      ],
      "alerts": []
    },
    {
      "trainset_id": "TS-015",
      "status": "STANDBY",
      "readiness_score": 0.88,
      "daily_km_allocation": 0.0,
      "cumulative_km": 98000.0,
      "stabling_bay": "BAY-03",
      "standby_reason": "Reserve for peak hours",
      "alerts": []
    },
    {
      "trainset_id": "TS-020",
      "status": "MAINTENANCE",
      "readiness_score": 0.0,
      "daily_km_allocation": 0.0,
      "cumulative_km": 150000.0,
      "maintenance_type": "PREVENTIVE",
      "ibl_bay": "IBL-02",
      "estimated_completion": "2025-12-03T14:00:00",
      "alerts": ["Scheduled wheel profiling"]
    }
  ],
  
  "fleet_summary": {
    "total_trainsets": 25,
    "revenue_service": 18,
    "standby": 4,
    "maintenance": 3,
    "availability_percent": 88.0
  },
  
  "optimization_metrics": {
    "fitness_score": 0.92,
    "method": "ga",
    "mileage_variance_coefficient": 0.08,
    "total_planned_km": 4850.0,
    "optimization_runtime_ms": 1250
  },
  
  "alerts": [
    {
      "trainset_id": "TS-007",
      "severity": "MEDIUM",
      "alert_type": "CERTIFICATE_EXPIRY",
      "message": "Safety certificate expires in 5 days"
    }
  ]
}
```


Why Use Blocks Instead of Individual Trips?
Crew Scheduling - A crew can be assigned to a block, not individual trips
Efficiency - Easier to manage and optimize at block level
Peak Hour Management - Blocks can be marked as is_peak: true to differentiate peak vs off-peak operations
Mileage Tracking - Each block has estimated_km for easy daily mileage calculation