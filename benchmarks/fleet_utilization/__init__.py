"""
Fleet Utilization Analysis Module

Provides tools for analyzing metro train fleet utilization including:
- Minimum fleet size calculations
- Coverage efficiency metrics
- Train utilization rate analysis
"""

from .fleet_analyzer import (
    FleetUtilizationAnalyzer,
    FleetUtilizationMetrics,
    format_metrics_report
)

from .benchmark_fleet_utilization import FleetUtilizationBenchmark

__all__ = [
    'FleetUtilizationAnalyzer',
    'FleetUtilizationMetrics',
    'FleetUtilizationBenchmark',
    'format_metrics_report'
]

__version__ = '1.0.0'
