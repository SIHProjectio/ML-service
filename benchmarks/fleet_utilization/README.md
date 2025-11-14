# Fleet Utilization Benchmarks

This directory contains tools for analyzing fleet utilization metrics for the metro train scheduling system.

## Overview

Fleet utilization analysis provides critical data for the **Results** section of your research paper, specifically:

1. **Minimum Fleet Size**: Calculate the minimum number of trains required to maintain service frequency
2. **Coverage Efficiency**: Measure percentage of peak vs. off-peak demand covered
3. **Train Utilization Rate**: Analyze average operational hours per train vs. idle time

## Components

### 1. `fleet_analyzer.py`
Core analysis module with the `FleetUtilizationAnalyzer` class.

**Key Features:**
- Calculate minimum fleet size based on headway requirements
- Analyze demand coverage (peak vs. off-peak)
- Compute train utilization rates
- Generate efficiency scores
- Find optimal fleet configurations

**Key Classes:**
- `FleetUtilizationAnalyzer`: Main analysis engine
- `FleetUtilizationMetrics`: Data class for results

### 2. `benchmark_fleet_utilization.py`
Comprehensive benchmarking script for research paper data collection.

**Features:**
- Test multiple fleet sizes
- Comparative analysis
- Statistical summaries
- JSON and text report generation

## Usage

### Quick Start

```bash
# Run comprehensive benchmark
python benchmark_fleet_utilization.py
```

This will:
- Analyze fleet sizes from 10-40 trains
- Calculate minimum requirements
- Measure coverage efficiency
- Compute utilization rates
- Generate JSON data and text report

### Custom Analysis

```python
from fleet_analyzer import FleetUtilizationAnalyzer

analyzer = FleetUtilizationAnalyzer()

# Analyze specific fleet size
metrics = analyzer.analyze_fleet_configuration(
    total_fleet=25,
    trains_in_maintenance=2
)

print(f"Coverage: {metrics.overall_coverage_percent:.1f}%")
print(f"Utilization: {metrics.utilization_rate_percent:.1f}%")

# Find optimal fleet size
optimal_size, optimal_metrics = analyzer.find_optimal_fleet_size(
    min_coverage_required=95.0
)
print(f"Optimal Fleet: {optimal_size} trains")
```

### Programmatic Benchmark

```python
from benchmark_fleet_utilization import FleetUtilizationBenchmark

benchmark = FleetUtilizationBenchmark()

# Run custom analysis
benchmark.run_comprehensive_analysis(
    fleet_sizes=[15, 20, 25, 30, 35],
    maintenance_rate=0.1
)

# Save results
benchmark.save_results("my_results.json")
benchmark.generate_report("my_report.txt")
```

## Kochi Metro Configuration

The analyzer uses real Kochi Metro parameters:

- **Route Length**: 25.612 km
- **Average Speed**: 35 km/h (operating speed)
- **Service Hours**: 5:00 AM - 11:00 PM (18 hours)
- **Peak Hours**: 
  - Morning: 7:00-10:00 AM
  - Evening: 5:00-8:00 PM
- **Target Headways**:
  - Peak: 5 minutes
  - Off-Peak: 10 minutes
- **Turnaround Time**: 10 minutes

## Output Files

### JSON Results (`fleet_utilization_benchmark_*.json`)
Complete data structure with:
- Metadata and configuration
- Detailed metrics for each fleet size
- Comparative statistics
- Optimal fleet configuration

### Text Report (`fleet_utilization_report_*.txt`)
Human-readable report with:
- Executive summary
- Optimal fleet configuration
- Comparative analysis
- Detailed results for each fleet size

## Metrics Explained

### 1. Minimum Fleet Size
**Formula**: `(Round Trip Time / Headway) + Buffer + Maintenance Reserve`

- Accounts for route travel time
- Includes operational buffers
- Considers maintenance requirements

**Research Paper Usage:**
> "Analysis revealed that a minimum fleet of 18 trains is required to maintain the target 5-minute headway during peak hours on the 25.612 km route."

### 2. Coverage Efficiency

**Metrics:**
- Peak demand coverage (%)
- Off-peak demand coverage (%)
- Overall weighted coverage (%)

**Research Paper Usage:**
> "A fleet of 25 trains achieved 100% peak demand coverage and 98.5% overall coverage across the 18-hour service period."

### 3. Train Utilization Rate

**Metrics:**
- Average operational hours per train
- Average idle hours per train
- Utilization rate percentage

**Formula**: `Utilization % = (Operational Hours / 24) × 100`

**Research Paper Usage:**
> "Fleet utilization analysis demonstrated an average of 16.2 operational hours per train (67.5% utilization rate), with 7.8 hours of scheduled idle time for charging and maintenance."

## Example Results

### Minimum Fleet Size Analysis
```
Fleet Size: 25 trains
Minimum Required: 18 trains
Excess Capacity: 7 trains (38.9%)

Peak Service: 15 trains
Off-Peak Service: 8 trains
Standby: 3 trains
Maintenance: 2 trains
```

### Coverage Efficiency
```
Peak Demand Coverage: 100.0%
Off-Peak Demand Coverage: 100.0%
Overall Coverage: 100.0%
```

### Utilization Rates
```
Avg Operational Hours/Train: 16.20 hours/day
Avg Idle Hours/Train: 7.80 hours/day
Utilization Rate: 67.5%
```

## Visualization Tips for Paper

### Suggested Graphs/Tables

1. **Fleet Size vs. Coverage Graph**
   - X-axis: Fleet Size (10-40 trains)
   - Y-axis: Coverage Percentage
   - Show peak and off-peak separately

2. **Utilization Rate Table**
   ```
   Fleet Size | Operational Hours | Idle Hours | Utilization %
   10         | 16.2             | 7.8        | 67.5%
   15         | 16.2             | 7.8        | 67.5%
   ...
   ```

3. **Efficiency Score Comparison**
   - Bar chart showing fleet efficiency vs. cost efficiency
   - Compare different fleet sizes

4. **Optimal Fleet Configuration Diagram**
   - Visual breakdown of train allocation
   - Service / Standby / Maintenance distribution

## Advanced Usage

### Sensitivity Analysis

```python
analyzer = FleetUtilizationAnalyzer()

# Test different maintenance rates
for maintenance_rate in [0.05, 0.10, 0.15, 0.20]:
    metrics = analyzer.analyze_fleet_configuration(
        total_fleet=25,
        trains_in_maintenance=int(25 * maintenance_rate)
    )
    print(f"Maintenance {maintenance_rate*100}%: Coverage {metrics.overall_coverage_percent:.1f}%")
```

### Peak Hour Variations

```python
# Modify peak hours
analyzer.peak_periods = [
    (time(6, 0), time(9, 0)),   # Earlier morning peak
    (time(16, 0), time(19, 0)),  # Earlier evening peak
]

metrics = analyzer.analyze_fleet_configuration(25, 2)
```

## Integration with Other Benchmarks

Combine with schedule generation benchmarks:

```python
from benchmark_schedule_performance import SchedulePerformanceBenchmark
from benchmark_fleet_utilization import FleetUtilizationBenchmark

# Performance benchmark
perf_benchmark = SchedulePerformanceBenchmark()
perf_results = perf_benchmark.run_comprehensive_benchmark(
    fleet_sizes=[15, 20, 25, 30],
    num_runs=5
)

# Fleet utilization benchmark
fleet_benchmark = FleetUtilizationBenchmark()
fleet_benchmark.run_comprehensive_analysis(
    fleet_sizes=[15, 20, 25, 30]
)

# Cross-reference results for comprehensive analysis
```

## Research Paper Templates

### Results Section Template

```markdown
### Fleet Utilization Results

#### Minimum Fleet Size
Analysis of the Kochi Metro route (25.612 km, 22 stations) revealed that a 
minimum fleet of [X] trains is required to maintain target service frequencies. 
This accounts for a [Y]-minute round-trip time, including [Z] minutes of 
turnaround at terminal stations.

#### Coverage Efficiency
Fleet configuration testing demonstrated that:
- Peak demand (7-10 AM, 5-8 PM) requires [N] trains for 5-minute headways
- Off-peak periods require [M] trains for 10-minute headways
- A fleet of [K] trains achieves [P]% overall coverage

#### Train Utilization Rate
Utilization analysis across fleet sizes from 10-40 trains showed:
- Average operational hours: [H] hours per train per day
- Average idle time: [I] hours per train per day  
- Overall utilization rate: [U]%

These metrics indicate [interpretation of efficiency/optimization].
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you're running from the correct directory
   ```bash
   cd /path/to/mlservice
   python benchmarks/fleet_utilization/benchmark_fleet_utilization.py
   ```

2. **Path Issues**: The benchmark automatically handles paths, but if needed:
   ```python
   sys.path.insert(0, '/path/to/mlservice')
   ```

## References

- Kochi Metro operational parameters
- Transit scheduling best practices
- Fleet optimization literature

## Future Enhancements

- [ ] Integration with real-time passenger data
- [ ] Dynamic headway adjustment
- [ ] Multi-line analysis
- [ ] Energy consumption correlation
- [ ] Cost-benefit analysis with operational costs

## Support

For questions or issues, refer to the main project documentation or examine the example usage in `__main__` blocks of each module.
