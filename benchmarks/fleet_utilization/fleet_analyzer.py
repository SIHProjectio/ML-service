#!/usr/bin/env python3
"""
Fleet Utilization Analysis for Metro Train Scheduling
Analyzes minimum fleet size, coverage efficiency, and train utilization rates.
"""
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime, time, timedelta
import statistics
from dataclasses import dataclass


@dataclass
class FleetUtilizationMetrics:
    """Metrics for fleet utilization analysis"""
    fleet_size: int
    minimum_required_trains: int
    trains_in_service_peak: int
    trains_in_service_offpeak: int
    trains_in_standby: int
    trains_in_maintenance: int
    
    # Coverage metrics
    peak_demand_coverage_percent: float
    offpeak_demand_coverage_percent: float
    overall_coverage_percent: float
    
    # Utilization metrics
    avg_operational_hours_per_train: float
    avg_idle_hours_per_train: float
    utilization_rate_percent: float
    
    # Time distribution
    total_service_hours: float
    peak_hours_duration: float
    offpeak_hours_duration: float
    
    # Efficiency scores
    fleet_efficiency_score: float
    cost_efficiency_score: float


class FleetUtilizationAnalyzer:
    """Analyzes fleet utilization for metro scheduling optimization"""
    
    def __init__(self):
        # Kochi Metro operational parameters
        self.service_start = time(5, 0)  # 5:00 AM
        self.service_end = time(23, 0)   # 11:00 PM
        self.total_service_hours = 18.0   # 18 hours per day
        
        # Peak hours definition
        self.peak_periods = [
            (time(7, 0), time(10, 0)),   # Morning peak: 7-10 AM
            (time(17, 0), time(20, 0)),  # Evening peak: 5-8 PM
        ]
        
        # Target headways (minutes between trains)
        self.peak_headway_target = 5     # 5 minutes during peak
        self.offpeak_headway_target = 10  # 10 minutes during off-peak
        
        # Route parameters (Kochi Metro)
        self.route_length_km = 25.612
        self.avg_speed_kmh = 35
        self.turnaround_time_minutes = 10
        
        # Calculate round trip time
        self.one_way_time = (self.route_length_km / self.avg_speed_kmh) * 60  # minutes
        self.round_trip_time = (self.one_way_time * 2) + (self.turnaround_time_minutes * 2)
        
    def calculate_peak_hours_duration(self) -> float:
        """Calculate total peak hours per day"""
        total_peak_minutes = 0
        for start, end in self.peak_periods:
            start_minutes = start.hour * 60 + start.minute
            end_minutes = end.hour * 60 + end.minute
            total_peak_minutes += (end_minutes - start_minutes)
        return total_peak_minutes / 60.0  # Convert to hours
    
    def calculate_minimum_fleet_size(
        self,
        headway_minutes: int,
        round_trip_minutes: Optional[float] = None
    ) -> int:
        """
        Calculate minimum number of trains needed to maintain headway.
        
        Formula: Minimum Fleet = (Round Trip Time / Headway) + Buffer
        
        Args:
            headway_minutes: Desired minutes between trains
            round_trip_minutes: Optional override for round trip time
            
        Returns:
            Minimum number of trains required
        """
        rtt = round_trip_minutes if round_trip_minutes else self.round_trip_time
        
        # Calculate base requirement
        base_trains = rtt / headway_minutes
        
        # Add buffer for operational flexibility (1 train) and maintenance (10%)
        buffer_trains = 1
        maintenance_buffer = max(1, int(base_trains * 0.1))
        
        minimum_fleet = int(base_trains) + buffer_trains + maintenance_buffer
        
        return minimum_fleet
    
    def calculate_demand_coverage(
        self,
        available_trains: int,
        required_trains_peak: int,
        required_trains_offpeak: int
    ) -> Dict[str, float]:
        """
        Calculate what percentage of demand can be covered.
        
        Args:
            available_trains: Number of trains available for service
            required_trains_peak: Required trains during peak hours
            required_trains_offpeak: Required trains during off-peak hours
            
        Returns:
            Dictionary with coverage percentages
        """
        peak_coverage = min(100.0, (available_trains / required_trains_peak) * 100)
        offpeak_coverage = min(100.0, (available_trains / required_trains_offpeak) * 100)
        
        # Weight by duration
        peak_duration = self.calculate_peak_hours_duration()
        offpeak_duration = self.total_service_hours - peak_duration
        
        overall_coverage = (
            (peak_coverage * peak_duration + offpeak_coverage * offpeak_duration) 
            / self.total_service_hours
        )
        
        return {
            "peak_coverage_percent": round(peak_coverage, 2),
            "offpeak_coverage_percent": round(offpeak_coverage, 2),
            "overall_coverage_percent": round(overall_coverage, 2)
        }
    
    def calculate_train_utilization(
        self,
        trains_in_service: int,
        service_hours: Optional[float] = None
    ) -> Dict[str, float]:
        """
        Calculate average operational hours and utilization per train.
        
        Args:
            trains_in_service: Number of trains actively in service
            service_hours: Total service hours (default: full day)
            
        Returns:
            Dictionary with utilization metrics
        """
        service_hours = service_hours or self.total_service_hours
        
        # Average operational hours per train
        # Assumes trains operate in shifts to cover full service period
        avg_operational_hours = service_hours * 0.9  # 90% active time assumption
        
        # Idle hours
        avg_idle_hours = 24 - avg_operational_hours
        
        # Utilization rate
        utilization_rate = (avg_operational_hours / 24) * 100
        
        return {
            "avg_operational_hours": round(avg_operational_hours, 2),
            "avg_idle_hours": round(avg_idle_hours, 2),
            "utilization_rate_percent": round(utilization_rate, 2)
        }
    
    def calculate_fleet_efficiency_score(
        self,
        fleet_size: int,
        minimum_required: int,
        coverage_percent: float
    ) -> float:
        """
        Calculate overall fleet efficiency score (0-100).
        
        Higher score = better efficiency
        Considers fleet size optimization and coverage
        
        Args:
            fleet_size: Actual fleet size
            minimum_required: Minimum required trains
            coverage_percent: Overall demand coverage percentage
            
        Returns:
            Efficiency score (0-100)
        """
        # Penalty for excess fleet (cost inefficiency)
        excess_ratio = (fleet_size - minimum_required) / minimum_required
        excess_penalty = min(30, excess_ratio * 20)  # Max 30 point penalty
        
        # Reward for coverage (service quality)
        coverage_score = coverage_percent * 0.7  # 70% weight on coverage
        
        # Efficiency score
        efficiency = coverage_score - excess_penalty
        efficiency = max(0, min(100, efficiency))  # Clamp to 0-100
        
        return round(efficiency, 2)
    
    def analyze_fleet_configuration(
        self,
        total_fleet: int,
        trains_in_maintenance: int = 0,
        trains_reserved: int = 0
    ) -> FleetUtilizationMetrics:
        """
        Comprehensive analysis of a fleet configuration.
        
        Args:
            total_fleet: Total number of trains in fleet
            trains_in_maintenance: Trains currently in maintenance
            trains_reserved: Trains reserved/held back
            
        Returns:
            FleetUtilizationMetrics object with complete analysis
        """
        # Calculate available trains
        available_trains = total_fleet - trains_in_maintenance - trains_reserved
        
        # Calculate minimum requirements
        min_fleet_peak = self.calculate_minimum_fleet_size(self.peak_headway_target)
        min_fleet_offpeak = self.calculate_minimum_fleet_size(self.offpeak_headway_target)
        min_fleet_overall = max(min_fleet_peak, min_fleet_offpeak)
        
        # Determine actual service allocation
        trains_in_service_peak = min(available_trains, min_fleet_peak)
        trains_in_service_offpeak = min(available_trains, min_fleet_offpeak)
        trains_in_standby = max(0, available_trains - trains_in_service_peak)
        
        # Coverage analysis
        coverage = self.calculate_demand_coverage(
            available_trains,
            min_fleet_peak,
            min_fleet_offpeak
        )
        
        # Utilization analysis
        utilization = self.calculate_train_utilization(trains_in_service_peak)
        
        # Efficiency scores
        peak_duration = self.calculate_peak_hours_duration()
        offpeak_duration = self.total_service_hours - peak_duration
        
        fleet_efficiency = self.calculate_fleet_efficiency_score(
            total_fleet,
            min_fleet_overall,
            coverage["overall_coverage_percent"]
        )
        
        # Cost efficiency (fewer trains = better cost efficiency, but must meet demand)
        cost_efficiency = (min_fleet_overall / total_fleet) * coverage["overall_coverage_percent"]
        
        return FleetUtilizationMetrics(
            fleet_size=total_fleet,
            minimum_required_trains=min_fleet_overall,
            trains_in_service_peak=trains_in_service_peak,
            trains_in_service_offpeak=trains_in_service_offpeak,
            trains_in_standby=trains_in_standby,
            trains_in_maintenance=trains_in_maintenance,
            peak_demand_coverage_percent=coverage["peak_coverage_percent"],
            offpeak_demand_coverage_percent=coverage["offpeak_coverage_percent"],
            overall_coverage_percent=coverage["overall_coverage_percent"],
            avg_operational_hours_per_train=utilization["avg_operational_hours"],
            avg_idle_hours_per_train=utilization["avg_idle_hours"],
            utilization_rate_percent=utilization["utilization_rate_percent"],
            total_service_hours=self.total_service_hours,
            peak_hours_duration=peak_duration,
            offpeak_hours_duration=offpeak_duration,
            fleet_efficiency_score=fleet_efficiency,
            cost_efficiency_score=round(cost_efficiency, 2)
        )
    
    def compare_fleet_sizes(
        self,
        fleet_sizes: List[int],
        maintenance_rate: float = 0.1
    ) -> Dict[int, FleetUtilizationMetrics]:
        """
        Compare different fleet size configurations.
        
        Args:
            fleet_sizes: List of fleet sizes to analyze
            maintenance_rate: Percentage of fleet in maintenance (default 10%)
            
        Returns:
            Dictionary mapping fleet size to metrics
        """
        results = {}
        
        for size in fleet_sizes:
            maintenance_trains = max(1, int(size * maintenance_rate))
            metrics = self.analyze_fleet_configuration(size, maintenance_trains)
            results[size] = metrics
        
        return results
    
    def find_optimal_fleet_size(
        self,
        min_coverage_required: float = 95.0,
        max_fleet: int = 50
    ) -> Tuple[int, FleetUtilizationMetrics]:
        """
        Find the optimal (smallest) fleet size that meets coverage requirements.
        
        Args:
            min_coverage_required: Minimum acceptable coverage percentage
            max_fleet: Maximum fleet size to consider
            
        Returns:
            Tuple of (optimal_fleet_size, metrics)
        """
        # Start from minimum required and increment
        min_theoretical = self.calculate_minimum_fleet_size(self.peak_headway_target)
        
        for fleet_size in range(min_theoretical, max_fleet + 1):
            maintenance_trains = max(1, int(fleet_size * 0.1))
            metrics = self.analyze_fleet_configuration(fleet_size, maintenance_trains)
            
            if metrics.overall_coverage_percent >= min_coverage_required:
                return fleet_size, metrics
        
        # If no solution found, return largest tested
        metrics = self.analyze_fleet_configuration(max_fleet, int(max_fleet * 0.1))
        return max_fleet, metrics


def format_metrics_report(metrics: FleetUtilizationMetrics) -> str:
    """Format metrics into a readable report"""
    report = f"""
{'='*70}
FLEET UTILIZATION ANALYSIS REPORT
{'='*70}

Fleet Configuration:
  Total Fleet Size:              {metrics.fleet_size} trains
  Minimum Required:              {metrics.minimum_required_trains} trains
  Excess Capacity:               {metrics.fleet_size - metrics.minimum_required_trains} trains

Service Allocation:
  Peak Service:                  {metrics.trains_in_service_peak} trains
  Off-Peak Service:              {metrics.trains_in_service_offpeak} trains
  Standby:                       {metrics.trains_in_standby} trains
  Maintenance:                   {metrics.trains_in_maintenance} trains

Coverage Efficiency:
  Peak Demand Coverage:          {metrics.peak_demand_coverage_percent:.1f}%
  Off-Peak Demand Coverage:      {metrics.offpeak_demand_coverage_percent:.1f}%
  Overall Coverage:              {metrics.overall_coverage_percent:.1f}%

Train Utilization:
  Avg Operational Hours/Train:   {metrics.avg_operational_hours_per_train:.2f} hours/day
  Avg Idle Hours/Train:          {metrics.avg_idle_hours_per_train:.2f} hours/day
  Utilization Rate:              {metrics.utilization_rate_percent:.1f}%

Time Distribution:
  Total Service Hours:           {metrics.total_service_hours:.1f} hours/day
  Peak Hours:                    {metrics.peak_hours_duration:.1f} hours/day
  Off-Peak Hours:                {metrics.offpeak_hours_duration:.1f} hours/day

Efficiency Scores:
  Fleet Efficiency:              {metrics.fleet_efficiency_score:.1f}/100
  Cost Efficiency:               {metrics.cost_efficiency_score:.1f}/100

{'='*70}
"""
    return report


if __name__ == "__main__":
    # Example usage
    analyzer = FleetUtilizationAnalyzer()
    
    print("Kochi Metro Fleet Utilization Analysis")
    print("=" * 70)
    
    # Analyze specific fleet size
    metrics = analyzer.analyze_fleet_configuration(
        total_fleet=25,
        trains_in_maintenance=2
    )
    
    print(format_metrics_report(metrics))
    
    # Find optimal fleet size
    optimal_size, optimal_metrics = analyzer.find_optimal_fleet_size(
        min_coverage_required=95.0
    )
    
    print(f"\nOptimal Fleet Size: {optimal_size} trains")
    print(f"Coverage: {optimal_metrics.overall_coverage_percent:.1f}%")
    print(f"Efficiency Score: {optimal_metrics.fleet_efficiency_score:.1f}/100")
