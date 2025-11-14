# Features Required for Metro Train Scheduling System

**Document Version:** 1.0  
**Last Updated:** November 11, 2025  
**Status:** Ground Truth Data Collection Phase

---

## Executive Summary

This document outlines the data features required for both the **GreedyOptim** (rule-based optimization) and **ML Model** (self-training prediction) components of the metro train scheduling system. Since we currently lack ground truth data, This serves as your complete guide for collecting ground truth data and preparing for ML model training.

---

## Table of Contents

1. [GreedyOptim Features](#greedyoptim-features)
2. [ML Model Features](#ml-model-features)
3. [Data Collection Priority](#data-collection-priority)
4. [Feature Engineering Guidelines](#feature-engineering-guidelines)

---

## GreedyOptim Features

The GreedyOptim system uses constraint-based optimization algorithms (GA, PSO, CMA-ES, etc.) to generate optimal train schedules. It requires operational data to evaluate constraints and objectives.

### 1. Trainset Status Data

| Feature | Description | Priority | Importance | Data Type | Example |
|---------|-------------|----------|------------|-----------|---------|
| `trainset_id` | Unique train identifier | **CRITICAL** | 5/5 | String | "KMRL-01" |
| `operational_status` | Current operational state | **CRITICAL** | 5/5 | Enum | "Available", "Maintenance" |
| `current_location` | Physical location | **HIGH** | 4/5 | String | "Depot-A", "IBL" |
| `last_service_date` | Date of last maintenance | **HIGH** | 4/5 | ISO Date | "2025-10-15" |
| `total_mileage_km` | Cumulative kilometers | **HIGH** | 4/5 | Float | 45000.0 |
| `age_years` | Train age in years | **MEDIUM** | 3/5 | Float | 3.5 |
| `daily_mileage_km` | Average daily travel | **MEDIUM** | 3/5 | Float | 250.0 |
| `operational_hours` | Total operational hours | **MEDIUM** | 3/5 | Float | 12500.0 |
| `base_reliability_score` | Historical reliability | **MEDIUM** | 3/5 | Float (0-1) | 0.92 |
| `manufacturer` | Train manufacturer | **LOW** | 2/5 | String | "Alstom" |
| `capacity_passengers` | Seating/standing capacity | **LOW** | 2/5 | Integer | 360 |
| `energy_efficiency_rating` | Energy efficiency grade | **LOW** | 2/5 | String | "A", "B" |

**Valid Operational Status Values:**
- `Available` - Ready for immediate deployment
- `In-Service` - Currently operating on route
- `Maintenance` - Under scheduled/corrective maintenance
- `Standby` - Reserved/on-call
- `Out-of-Order` - Not operational due to failures

**Why These Matter:**
- **Critical features** directly determine if a train can be scheduled
- **High priority** affects optimization objective functions
- **Medium/Low priority** provide fine-tuning and context

---

### 2. Fitness Certificates

| Feature | Description | Priority | Importance | Data Type | Example |
|---------|-------------|----------|------------|-----------|---------|
| `trainset_id` | Train identifier | **CRITICAL** | 5/5 | String | "KMRL-01" |
| `department` | Certifying department | **CRITICAL** | 5/5 | Enum | "Safety", "Electrical" |
| `status` | Certificate validity status | **CRITICAL** | 5/5 | Enum | "Valid", "Expired" |
| `issue_date` | Certificate issue date | **HIGH** | 4/5 | ISO Date | "2025-01-15" |
| `expiry_date` | Certificate expiry date | **HIGH** | 4/5 | ISO Date | "2026-01-15" |
| `inspector_id` | Certifying inspector | **LOW** | 2/5 | String | "INS-001" |
| `compliance_score` | Compliance rating (0-100) | **MEDIUM** | 3/5 | Integer | 95 |
| `renewal_required` | Renewal flag | **HIGH** | 4/5 | Boolean | true/false |

**Valid Certificate Status Values:**
- `Valid` - Certificate is current and valid
- `Expired` - Certificate has expired (hard constraint)
- `Expiring-Soon` - Expires within 30 days (soft constraint)
- `Suspended` - Certificate suspended due to violation

**Valid Department Values:**
- `Safety` - Safety systems certification
- `Operations` - Operational readiness
- `Technical` - Technical systems
- `Electrical` - Electrical systems
- `Mechanical` - Mechanical systems

**Hard Constraints:**
- Trains with ANY expired certificates CANNOT be scheduled for service
- All departments must have valid certificates for revenue service

---

### 3. Job Cards (Maintenance Work Orders)

| Feature | Description | Priority | Importance | Data Type | Example |
|---------|-------------|----------|------------|-----------|---------|
| `trainset_id` | Train identifier | **CRITICAL** | 5/5 | String | "KMRL-01" |
| `job_id` | Unique job identifier | **CRITICAL** | 5/5 | String | "JOB-12345" |
| `priority` | Job priority level | **CRITICAL** | 5/5 | Enum | "Critical", "High" |
| `status` | Current job status | **CRITICAL** | 5/5 | Enum | "Open", "In-Progress" |
| `job_type` | Type of maintenance | **HIGH** | 4/5 | Enum | "Corrective", "Preventive" |
| `estimated_hours` | Estimated completion time | **HIGH** | 4/5 | Float | 8.0 |
| `created_date` | Job creation date | **MEDIUM** | 3/5 | ISO Date | "2025-11-01" |
| `component` | Affected component | **MEDIUM** | 3/5 | String | "Brakes", "HVAC" |
| `description` | Job description | **LOW** | 2/5 | String | "Brake pad replacement" |
| `assigned_technician` | Assigned tech ID | **LOW** | 2/5 | String | "TECH-101" |
| `cost_estimate` | Estimated cost (₹) | **LOW** | 2/5 | Integer | 25000 |

**Valid Priority Values:**
- `Critical` - Immediate action required (train cannot operate)
- `High` - Urgent but train may operate with restrictions
- `Medium` - Should be addressed within week
- `Low` - Routine maintenance

**Valid Status Values:**
- `Open` - Job created, not started
- `In-Progress` - Work underway
- `Closed` - Work completed
- `Pending-Parts` - Waiting for spare parts

**Valid Job Type Values:**
- `Preventive` - Scheduled maintenance
- `Corrective` - Fix identified issues
- `Breakdown` - Emergency repair
- `Inspection` - Routine inspection
- `Upgrade` - System upgrade

**Constraint Impact:**
- `Critical` + `Open` = Train CANNOT be scheduled
- `High` + `Open` = Train CAN be scheduled but with penalty
- `Medium/Low` + `Open` = Minor penalty only

---

### 4. Component Health

| Feature | Description | Priority | Importance | Data Type | Example |
|---------|-------------|----------|------------|-----------|---------|
| `trainset_id` | Train identifier | **CRITICAL** | 5/5 | String | "KMRL-01" |
| `component` | Component name | **CRITICAL** | 5/5 | String | "Brakes", "Propulsion" |
| `status` | Health status | **CRITICAL** | 5/5 | Enum | "Good", "Warning" |
| `wear_level` | Wear percentage (0-100) | **HIGH** | 4/5 | Float | 65.5 |
| `health_score` | Overall health (0-100) | **HIGH** | 4/5 | Float | 85.0 |
| `last_inspection` | Last inspection date | **MEDIUM** | 3/5 | ISO Date | "2025-10-20" |
| `threshold` | Warning threshold | **HIGH** | 4/5 | Float | 75.0 |
| `next_maintenance_km` | KM until next service | **MEDIUM** | 3/5 | Integer | 5000 |
| `predicted_failure_date` | AI predicted failure | **MEDIUM** | 3/5 | ISO Date | "2026-03-15" |
| `maintenance_urgency` | Urgency indicator | **HIGH** | 4/5 | Enum | "High", "Normal" |

**Valid Component Status Values:**
- `Good` - Component healthy, no issues
- `Fair` - Component acceptable but monitor
- `Warning` - Component approaching threshold
- `Critical` - Component requires immediate attention

**Critical Components (Must be "Good" or "Fair" for service):**
- `Brakes` - Braking system
- `Propulsion` - Traction motors
- `Doors` - Door system
- `Safety_Systems` - Emergency systems

**Important Components:**
- `HVAC` - Climate control
- `Battery` - Auxiliary power
- `Pantograph` - Power collection
- `Compressor` - Air system

**Constraint Rules:**
- Any component in `Critical` status = Train CANNOT operate
- 2+ components in `Warning` status = Train should not be scheduled
- `wear_level > threshold` = Apply scheduling penalty

---

### 5. Optimization Configuration

| Feature | Description | Priority | Importance | Data Type | Default | Range |
|---------|-------------|----------|------------|-----------|---------|-------|
| `required_service_trains` | Min trains in service | **CRITICAL** | 5/5 | Integer | 15 | 10-30 |
| `min_standby` | Min standby trains | **HIGH** | 4/5 | Integer | 2 | 1-5 |
| `population_size` | GA population size | **MEDIUM** | 3/5 | Integer | 50 | 20-200 |
| `generations` | GA iterations | **MEDIUM** | 3/5 | Integer | 100 | 30-500 |
| `mutation_rate` | GA mutation rate | **LOW** | 2/5 | Float | 0.1 | 0.01-0.3 |
| `crossover_rate` | GA crossover rate | **LOW** | 2/5 | Float | 0.8 | 0.5-0.95 |
| `elite_size` | Elite solutions kept | **LOW** | 2/5 | Integer | 5 | 1-10 |

**Why Configuration Matters:**
- `required_service_trains` determines if solution is feasible
- `min_standby` ensures operational flexibility
- Algorithm parameters affect solution quality vs. speed trade-off

---

### 6. Additional Optimization Features

#### Branding Contracts (Optional but Valuable)

| Feature | Description | Priority | Importance |
|---------|-------------|----------|------------|
| `trainset_id` | Train with branding | **MEDIUM** | 3/5 |
| `brand` | Brand/advertiser name | **MEDIUM** | 3/5 |
| `contracted_exposure_hours` | Required monthly hours | **MEDIUM** | 3/5 |
| `daily_target_hours` | Daily exposure target | **MEDIUM** | 3/5 |
| `penalty_per_hour_shortfall` | Penalty per missing hour | **MEDIUM** | 3/5 |
| `route_restrictions` | Preferred routes | **LOW** | 2/5 |
| `minimum_daily_hours` | Min hours per day | **MEDIUM** | 3/5 |

**Objective Function Impact:**
- Meeting branding commitments increases schedule quality score
- Penalties for underdelivery affect optimization objective
- Can be primary or secondary optimization goal

#### IoT Sensor Data (Future Enhancement)

| Feature | Description | Priority | Importance |
|---------|-------------|----------|------------|
| `vibration_levels` | Bogie vibration (mm/s) | **LOW** | 2/5 |
| `temperature_readings` | Motor temperature (°C) | **LOW** | 2/5 |
| `power_consumption` | Energy usage (kWh) | **LOW** | 2/5 |
| `door_cycle_count` | Door operations | **LOW** | 2/5 |

**Use Case:** Real-time condition monitoring to update health scores

---

## ML Model Features

The ML Model learns from historical schedules to predict schedule quality and suggest improvements. It requires both historical data and engineered features.

### 1. Historical Schedule Features

These features are extracted from generated schedules to train the prediction model.

#### Basic Schedule Metrics

| Feature | Description | Priority | Importance | Extraction Method |
|---------|-------------|----------|------------|-------------------|
| `num_trains` | Total trains in fleet | **CRITICAL** | 5/5 | Count from schedule |
| `num_service` | Trains in service | **CRITICAL** | 5/5 | Count by status |
| `num_standby` | Trains on standby | **HIGH** | 4/5 | Count by status |
| `num_maintenance` | Trains in maintenance | **HIGH** | 4/5 | Count by status |
| `availability_percent` | Operational availability % | **CRITICAL** | 5/5 | (service+standby)/total * 100 |

#### Readiness & Health Features

| Feature | Description | Priority | Importance | Extraction Method |
|---------|-------------|----------|------------|-------------------|
| `avg_readiness_score` | Mean train readiness | **CRITICAL** | 5/5 | Mean of all readiness scores |
| `min_readiness_score` | Minimum readiness | **HIGH** | 4/5 | Min readiness score |
| `readiness_variance` | Readiness distribution | **MEDIUM** | 3/5 | Variance of readiness |
| `health_score_avg` | Average health score | **HIGH** | 4/5 | Mean component health |
| `critical_components_count` | Components in critical state | **HIGH** | 4/5 | Count status="Critical" |

#### Mileage & Usage Features

| Feature | Description | Priority | Importance | Extraction Method |
|---------|-------------|----------|------------|-------------------|
| `total_mileage` | Fleet total mileage | **MEDIUM** | 3/5 | Sum all train mileages |
| `avg_mileage` | Average train mileage | **MEDIUM** | 3/5 | Mean mileage |
| `mileage_variance` | Mileage distribution | **HIGH** | 4/5 | Variance (load balancing) |
| `mileage_std_dev` | Mileage std deviation | **HIGH** | 4/5 | Std dev mileage |
| `max_mileage_train` | Highest mileage train | **MEDIUM** | 3/5 | Max mileage value |
| `min_mileage_train` | Lowest mileage train | **MEDIUM** | 3/5 | Min mileage value |

**Why Mileage Variance Matters:**
- High variance = poor load balancing = premature component wear
- Target: Keep all trains within ±10% of mean mileage

#### Certificate & Compliance Features

| Feature | Description | Priority | Importance | Extraction Method |
|---------|-------------|----------|------------|-------------------|
| `certificate_expiry_count` | Certificates expiring soon | **HIGH** | 4/5 | Count status="Expiring-Soon" |
| `expired_certificate_count` | Expired certificates | **CRITICAL** | 5/5 | Count status="Expired" |
| `suspended_certificate_count` | Suspended certificates | **HIGH** | 4/5 | Count status="Suspended" |
| `cert_compliance_percent` | Certificate compliance % | **HIGH** | 4/5 | Valid certs / total * 100 |

#### Job Card Features

| Feature | Description | Priority | Importance | Extraction Method |
|---------|-------------|----------|------------|-------------------|
| `critical_jobs_open` | Open critical jobs | **CRITICAL** | 5/5 | Count priority="Critical" & status="Open" |
| `high_priority_jobs` | Open high priority jobs | **HIGH** | 4/5 | Count priority="High" & status="Open" |
| `total_jobs_open` | All open jobs | **MEDIUM** | 3/5 | Count status="Open" |
| `jobs_in_progress` | Jobs being worked | **MEDIUM** | 3/5 | Count status="In-Progress" |
| `avg_estimated_hours` | Avg job completion time | **LOW** | 2/5 | Mean estimated_hours |

#### Temporal Features

| Feature | Description | Priority | Importance | Extraction Method |
|---------|-------------|----------|------------|-------------------|
| `time_of_day` | Hour of schedule generation | **HIGH** | 4/5 | Extract hour from timestamp |
| `day_of_week` | Day of week (0-6) | **HIGH** | 4/5 | Extract weekday |
| `is_weekend` | Weekend flag | **MEDIUM** | 3/5 | day_of_week >= 5 |
| `is_peak_hour` | Peak hour flag | **HIGH** | 4/5 | hour in [7-10, 17-20] |
| `month` | Month (1-12) | **LOW** | 2/5 | Extract month |
| `season` | Season indicator | **LOW** | 2/5 | Monsoon, Summer, Winter |

**Peak Hour Patterns:**
- Morning: 7:00-10:00 AM
- Evening: 5:00-8:00 PM
- More trains needed during peaks

#### Branding Features (If Available)

| Feature | Description | Priority | Importance | Extraction Method |
|---------|-------------|----------|------------|-------------------|
| `branding_priority_sum` | Total branding priority | **MEDIUM** | 3/5 | Sum priority weights |
| `branded_trains_count` | Trains with contracts | **MEDIUM** | 3/5 | Count branded trains |
| `branding_sla_compliance` | SLA compliance score | **MEDIUM** | 3/5 | Met targets / total * 100 |
| `exposure_shortfall` | Hours under target | **LOW** | 2/5 | Sum shortfalls |

---

### 2. Target Variable (Schedule Quality Score)

**CRITICAL for ML Training:** The target variable must be carefully engineered

| Component | Weight | Description | Calculation |
|-----------|--------|-------------|-------------|
| **Readiness Score** | 30% | How ready trains are | `avg_readiness_score * 0.30` |
| **Availability** | 25% | Fleet availability % | `(availability_percent / 100) * 0.25` |
| **Mileage Balance** | 20% | Load balancing quality | `(1 - mileage_variance_coef) * 0.20` |
| **Certificate Compliance** | 15% | Certificate status | `(valid_certs / total_certs) * 0.15` |
| **Constraint Violations** | 10% | No hard violations | `max(0, 0.10 - violations * 0.02)` |

**Total Score:** 0-100 scale

**Quality Score Formula:**
```python
quality_score = (
    avg_readiness_score * 30 +
    (availability_percent / 100) * 25 +
    max(0, (1 - mileage_variance_coefficient) * 20) +
    (valid_certificates / total_certificates) * 15 +
    max(0, 10 - fitness_violations * 2)
)
```

**Importance:** 5/5 **CRITICAL**

---

### 3. Derived Features for ML

These features require engineering from raw data:

#### Statistical Aggregations

| Feature | Formula | Priority | Importance |
|---------|---------|----------|------------|
| `mileage_variance_coefficient` | `std_dev / mean` | **HIGH** | 4/5 |
| `readiness_dispersion` | `(max - min) / mean` | **MEDIUM** | 3/5 |
| `maintenance_ratio` | `maintenance / total` | **HIGH** | 4/5 |
| `utilization_rate` | `(service + standby) / total` | **HIGH** | 4/5 |

#### Temporal Patterns

| Feature | Description | Priority | Importance |
|---------|-------------|----------|------------|
| `schedules_generated_today` | Count for current day | **MEDIUM** | 3/5 |
| `avg_quality_last_week` | Rolling average quality | **HIGH** | 4/5 |
| `trend_direction` | Quality improving/declining | **HIGH** | 4/5 |
| `days_since_perfect_schedule` | Days since 100% quality | **LOW** | 2/5 |

#### Fleet Health Trends

| Feature | Description | Priority | Importance |
|---------|-------------|----------|------------|
| `deterioration_rate` | Health decline over time | **HIGH** | 4/5 |
| `maintenance_frequency` | Avg days between maintenance | **MEDIUM** | 3/5 |
| `failure_prediction_count` | Trains with predicted failures | **MEDIUM** | 3/5 |

---

### 4. Feature Engineering for ML

#### Normalization & Scaling

| Feature Type | Method | Priority |
|--------------|--------|----------|
| Mileage values | Min-Max scaling [0,1] | **HIGH** |
| Counts (trains, jobs) | StandardScaler (z-score) | **MEDIUM** |
| Percentages | Already [0-100], divide by 100 | **HIGH** |
| Categorical (status) | One-hot encoding | **CRITICAL** |
| Time features | Cyclical encoding (sin/cos) | **HIGH** |

**Cyclical Encoding Example:**
```python
# For hour of day (0-23)
hour_sin = sin(2 * π * hour / 24)
hour_cos = cos(2 * π * hour / 24)

# For day of week (0-6)
dow_sin = sin(2 * π * day_of_week / 7)
dow_cos = cos(2 * π * day_of_week / 7)
```

#### Feature Interactions

| Interaction | Formula | Why Important |
|-------------|---------|---------------|
| `readiness_x_availability` | `readiness * availability` | High readiness + high availability = best |
| `jobs_per_train` | `open_jobs / num_trains` | Maintenance workload per train |
| `expiry_pressure` | `expiring_certs / total_certs` | Certificate renewal urgency |
| `peak_hour_capacity` | `available_trains * is_peak` | Capacity during demand peaks |

---

## Data Collection Priority

### Phase 1: Critical (Start Immediately) - Priority 5/5

**Must-Have for Basic Operation:**

1. **Trainset Status** (All CRITICAL + HIGH priority fields)
   - trainset_id, operational_status, current_location
   - last_service_date, total_mileage_km
   - **Collection Method:** CMMS integration or manual entry
   - **Frequency:** Real-time or hourly updates

2. **Fitness Certificates** (All CRITICAL fields)
   - trainset_id, department, status, expiry_date
   - **Collection Method:** Certification management system
   - **Frequency:** Daily checks, immediate on changes

3. **Job Cards** (CRITICAL + HIGH fields)
   - trainset_id, job_id, priority, status, estimated_hours
   - **Collection Method:** Maintenance management system
   - **Frequency:** Real-time updates on job status changes

4. **Component Health** (CRITICAL fields)
   - trainset_id, component, status, wear_level
   - **Collection Method:** Inspection reports + IoT sensors
   - **Frequency:** Daily for manual, real-time for IoT

**Estimated Time:** 2-4 weeks for manual entry, 1-2 months for system integration

---

### Phase 2: High Priority (Within 2 Months) - Priority 4/5

**Important for Quality:**

1. **Historical Schedules**
   - Save all generated schedules with timestamps
   - Include optimization metrics
   - **Storage:** JSON files or database
   - **Frequency:** Every schedule generation

2. **Temporal Data**
   - Accurate timestamps for all events
   - Peak hour definitions
   - **Collection Method:** Automatic with schedule generation
   - **Frequency:** Continuous

3. **Mileage Tracking**
   - Daily mileage updates per train
   - Route assignments
   - **Collection Method:** GPS + route planning system
   - **Frequency:** Daily

4. **Certificate Compliance Tracking**
   - Track renewals and expirations
   - Department-wise compliance
   - **Collection Method:** Certification system
   - **Frequency:** Weekly reports

**Estimated Time:** 1-2 months

---

### Phase 3: Medium Priority (Within 6 Months) - Priority 3/5

**Enhanced Features:**

1. **Branding Contracts**
   - Contract details and performance
   - Exposure tracking
   - **Collection Method:** Contract management system
   - **Frequency:** Daily exposure logs, monthly reports

2. **Detailed Component Health**
   - All component types
   - Predictive maintenance data
   - **Collection Method:** Enhanced IoT + AI predictions
   - **Frequency:** Real-time for IoT

3. **Performance Metrics**
   - Punctuality, reliability, availability
   - Per-train performance tracking
   - **Collection Method:** Operations management system
   - **Frequency:** Daily

**Estimated Time:** 3-6 months

---

### Phase 4: Low Priority (Future Enhancement) - Priority 2/5

**Nice-to-Have:**

1. **IoT Sensor Streams**
   - Vibration, temperature, power
   - Real-time monitoring
   - **Collection Method:** IoT platform integration
   - **Frequency:** Real-time (every second/minute)

2. **External Factors**
   - Weather data
   - Special events
   - Ridership forecasts
   - **Collection Method:** External APIs + planning systems
   - **Frequency:** Daily

3. **Cost Data**
   - Maintenance costs
   - Operational costs
   - **Collection Method:** Finance system
   - **Frequency:** Monthly

**Estimated Time:** 6+ months

---

## Feature Engineering Guidelines

### For GreedyOptim

1. **Data Validation**
   - Validate all enum values (operational_status, priority, etc.)
   - Check trainset_id consistency across all data sections
   - Ensure date formats (ISO 8601)
   - Validate numerical ranges (wear_level 0-100, etc.)

2. **Constraint Checking**
   ```python
   # Hard constraints
   can_operate = (
       operational_status == "Available" AND
       all_certificates_valid AND
       no_critical_jobs_open AND
       all_components_not_critical
   )
   ```

3. **Soft Constraints & Penalties**
   ```python
   # Penalty calculation
   penalty = 0
   if expiring_certificates > 0:
       penalty += expiring_certificates * 0.1
   if high_priority_jobs > 0:
       penalty += high_priority_jobs * 0.05
   if component_warnings > 0:
       penalty += component_warnings * 0.03
   ```

---

### For ML Model

1. **Feature Matrix Construction**
   ```python
   # Standard feature order (must be consistent)
   FEATURES = [
       "num_trains",
       "num_service",
       "num_standby",
       "num_maintenance",
       "avg_readiness_score",
       "min_readiness_score",
       "total_mileage",
       "avg_mileage",
       "mileage_variance",
       "certificate_expiry_count",
       "critical_jobs_open",
       "time_of_day",
       "day_of_week",
       "branding_priority_sum"
   ]
   ```

2. **Missing Data Handling**
   - **Strategy:** Imputation with domain knowledge
   - mileage: Use fleet average
   - readiness_score: Use 0.8 (safe default)
   - certificates: Assume valid if missing (risky, flag for review)
   - job_cards: Empty list = no pending jobs

3. **Outlier Detection**
   - Mileage > 2,000,000 km → Flag for review
   - Readiness < 0.5 → Investigate data quality
   - Wear level > 100 → Data error

4. **Temporal Features**
   - Use cyclical encoding for hour and day
   - Create lag features (previous day's quality)
   - Rolling averages (7-day, 30-day quality)

---

## Ground Truth Data Requirements

### Minimum Viable Dataset for ML Training

| Requirement | Minimum | Recommended | Ideal |
|-------------|---------|-------------|-------|
| **Historical Schedules** | 100 | 500 | 1000+ |
| **Time Period** | 2 weeks | 2 months | 6+ months |
| **Train Fleet Size** | 20 | 25 | 30+ |
| **Data Quality** | 80% complete | 95% complete | 99% complete |

### Data Collection Strategy

1. **Immediate Actions**
   - Set up automated schedule saving
   - Create database schema for all features
   - Implement data validation pipelines

2. **Short-term (1-3 months)**
   - Manual data entry for missing fields
   - Integration with existing systems (CMMS, etc.)
   - Daily data quality checks

3. **Long-term (3-6 months)**
   - IoT sensor integration
   - Automated feature extraction
   - Continuous model retraining

---

## Data Quality Checklist

### Before Using Data for GreedyOptim

- [ ] All trainset_ids are unique and consistent
- [ ] Operational statuses use valid enum values
- [ ] Certificate expiry dates are in future or flagged as expired
- [ ] Job priorities match actual operational practice
- [ ] Component status reflects real inspection results
- [ ] No missing CRITICAL priority fields

### Before Using Data for ML Training

- [ ] Minimum 100 historical schedules collected
- [ ] Quality scores calculated for all schedules
- [ ] Features extracted consistently
- [ ] Missing values handled appropriately
- [ ] Outliers identified and addressed
- [ ] Train/test split maintains temporal order
- [ ] Feature distributions are reasonable

---

## Implementation Checklist

### Week 1-2: Data Infrastructure

- [ ] Design database schema
- [ ] Set up data validation pipeline
- [ ] Create data entry forms/interfaces
- [ ] Implement automated schedule saving

### Week 3-4: Initial Data Collection

- [ ] Collect trainset status (all trains)
- [ ] Gather fitness certificates (all departments)
- [ ] Document open job cards
- [ ] Record component health statuses

### Month 2: Integration

- [ ] Integrate with CMMS if available
- [ ] Set up certification tracking
- [ ] Implement mileage tracking
- [ ] Begin historical schedule collection

### Month 3-4: Feature Engineering

- [ ] Build feature extraction pipeline
- [ ] Implement quality score calculation
- [ ] Create derived features
- [ ] Validate feature distributions

### Month 5-6: ML Model Development

- [ ] Train initial model on collected data
- [ ] Validate model performance
- [ ] Deploy model for schedule prediction
- [ ] Set up continuous learning pipeline

---

## Appendix A: Data Sources

### Primary Data Sources

1. **CMMS (Computerized Maintenance Management System)**
   - Trainset status
   - Job cards
   - Maintenance schedules
   - Component health (manual inspections)

2. **Certification Management System**
   - Fitness certificates
   - Compliance tracking
   - Inspector assignments

3. **Operations Management System**
   - Current locations
   - Service schedules
   - Performance metrics

4. **IoT Platform** (if available)
   - Real-time sensor data
   - Component health (automated)
   - Vibration, temperature, etc.

5. **Contract Management System**
   - Branding contracts
   - SLA tracking
   - Performance reports

### Alternative Data Sources (If Systems Unavailable)

1. **Manual Entry**
   - Spreadsheets
   - Daily inspection reports
   - Maintenance logs

2. **Synthetic Data Generator**
   - Use `EnhancedMetroDataGenerator`
   - For testing and development only
   - Not for production training

---

## Appendix B: Feature Importance Rankings

### For GreedyOptim (Constraint Satisfaction)

1. (5/5) **Expired Certificates** - Hard constraint
2. (5/5) **Critical Open Jobs** - Hard constraint
3. (5/5) **Critical Component Status** - Hard constraint
4. (5/5) **Operational Status** - Determines availability
5. (4/5) **Required Service Trains** - Feasibility constraint
6. (4/5) **Component Wear Levels** - Soft constraint
7. (4/5) **Expiring Certificates** - Planning constraint
8. (3/5) **Mileage Distribution** - Load balancing objective
9. (3/5) **Branding Targets** - Revenue objective
10. (2/5) **Standby Requirements** - Safety buffer

### For ML Model (Predictive Quality)

1. (5/5) **Average Readiness Score** - Primary quality indicator
2. (5/5) **Availability Percent** - Core operational metric
3. (5/5) **Quality Score (Target)** - Model objective
4. (4/5) **Mileage Variance** - Load balancing quality
5. (4/5) **Critical Jobs Count** - Operational bottleneck
6. (4/5) **Time of Day** - Demand pattern indicator
7. (4/5) **Certificate Compliance** - Regulatory metric
8. (3/5) **Day of Week** - Weekly pattern
9. (3/5) **Maintenance Ratio** - Fleet health
10. (2/5) **Branding Priority** - Revenue optimization

---

### GreedyOptim Minimum

```json
{
  "trainset_status": [
    {"trainset_id": "KMRL-01", "operational_status": "Available"}
  ],
  "fitness_certificates": [
    {"trainset_id": "KMRL-01", "department": "Safety", "status": "Valid", "expiry_date": "2026-01-01"}
  ],
  "job_cards": [
    {"trainset_id": "KMRL-01", "job_id": "JOB-001", "priority": "Low", "status": "Closed"}
  ],
  "component_health": [
    {"trainset_id": "KMRL-01", "component": "Brakes", "status": "Good", "wear_level": 25.0}
  ]
}
```

### ML Model Minimum

```python
# After extracting from 100+ schedules:
X = [
    [25, 15, 2, 3, 0.92, 0.85, 1250000, 50000, 0.05, 1, 0, 8, 2, 0],
    # ... 99 more rows
]
y = [85.3, ...]  # Quality scores
```

---

**END OF DOCUMENT**
