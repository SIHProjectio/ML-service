"""
Constraint Satisfaction Analysis Engine
Analyzes how well schedules satisfy operational constraints.
"""
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import defaultdict


@dataclass
class ConstraintMetrics:
    """Constraint satisfaction metrics for a schedule."""
    
    # Maintenance Window Compliance
    trains_needing_maintenance: int
    trains_scheduled_maintenance: int
    maintenance_compliance_rate: float  # Percentage of trains properly scheduled
    overdue_maintenance_count: int  # Trains past due for maintenance
    maintenance_window_violations: int  # Trains scheduled but violating time windows
    avg_maintenance_delay_days: float  # Average days past due for overdue trains
    
    # Turnaround Time Adherence
    total_turnarounds: int  # Number of train turnarounds (end-to-start transitions)
    compliant_turnarounds: int  # Turnarounds meeting minimum time requirement
    turnaround_compliance_rate: float  # Percentage meeting requirements
    avg_turnaround_time_minutes: float  # Average turnaround time
    min_turnaround_time_minutes: float  # Shortest turnaround
    turnaround_violations: int  # Count of insufficient turnarounds
    
    # Energy/Battery Constraints (if applicable)
    total_daily_energy_kwh: float  # Total energy consumption
    peak_power_demand_kw: float  # Maximum instantaneous power
    energy_efficiency_score: float  # Energy per km traveled
    battery_range_violations: int  # Trains exceeding battery range
    charging_opportunities: int  # Number of charging windows
    energy_constraint_violations: int  # Total energy constraint failures
    
    # Certificate Constraints
    trains_with_expired_certs: int
    trains_with_expiring_soon_certs: int
    certificate_compliance_rate: float
    
    # Job Card Constraints
    trains_with_critical_jobs: int
    trains_with_blocking_jobs: int
    job_constraint_violations: int
    
    # Component Health Constraints
    trains_with_critical_components: int
    trains_with_warning_components: int
    component_constraint_violations: int
    
    # Overall Scores
    maintenance_score: float  # 0-100
    turnaround_score: float  # 0-100
    energy_score: float  # 0-100
    certificate_score: float  # 0-100
    job_score: float  # 0-100
    component_score: float  # 0-100
    overall_constraint_score: float  # 0-100 weighted average


class ConstraintAnalyzer:
    """Analyzes constraint satisfaction in train schedules."""
    
    # Operational constraints
    MIN_TURNAROUND_TIME_MINUTES = 30  # Minimum time between service blocks
    MAX_DAILY_KM = 400  # Maximum km per train per day
    AVG_SPEED_KMH = 35.0  # Kochi Metro average speed
    ROUTE_LENGTH_KM = 25.612
    
    # Energy parameters (Kochi Metro - electric)
    ENERGY_PER_KM_KWH = 2.5  # Approximate energy consumption per km
    BATTERY_CAPACITY_KWH = 150.0  # Battery capacity (if applicable)
    MAX_RANGE_KM = 60.0  # Maximum range on battery (for degraded mode)
    
    # Maintenance requirements
    MAINTENANCE_INTERVAL_KM = 10000  # Km between maintenance
    MAINTENANCE_OVERDUE_THRESHOLD_KM = 11000  # When maintenance becomes critical
    
    def __init__(self):
        """Initialize constraint analyzer."""
        pass
    
    def analyze_schedule(self, schedule: Dict, data: Dict) -> ConstraintMetrics:
        """Analyze constraint satisfaction in a schedule.
        
        Args:
            schedule: Schedule dictionary from optimizer
            data: Original metro data with trainset status, certs, jobs, etc.
            
        Returns:
            ConstraintMetrics with all measurements
        """
        trainsets = schedule.get('trainsets', schedule.get('schedule', {}).get('trainsets', []))
        
        # Analyze maintenance constraints
        maintenance_metrics = self._analyze_maintenance_constraints(trainsets, data)
        
        # Analyze turnaround time constraints
        turnaround_metrics = self._analyze_turnaround_constraints(trainsets)
        
        # Analyze energy constraints
        energy_metrics = self._analyze_energy_constraints(trainsets)
        
        # Analyze certificate constraints
        cert_metrics = self._analyze_certificate_constraints(trainsets, data)
        
        # Analyze job card constraints
        job_metrics = self._analyze_job_constraints(trainsets, data)
        
        # Analyze component health constraints
        component_metrics = self._analyze_component_constraints(trainsets, data)
        
        # Calculate scores
        scores = self._calculate_scores(
            maintenance_metrics, turnaround_metrics, energy_metrics,
            cert_metrics, job_metrics, component_metrics
        )
        
        return ConstraintMetrics(
            # Maintenance
            trains_needing_maintenance=maintenance_metrics['needing'],
            trains_scheduled_maintenance=maintenance_metrics['scheduled'],
            maintenance_compliance_rate=maintenance_metrics['compliance_rate'],
            overdue_maintenance_count=maintenance_metrics['overdue'],
            maintenance_window_violations=maintenance_metrics['violations'],
            avg_maintenance_delay_days=maintenance_metrics['avg_delay'],
            
            # Turnaround
            total_turnarounds=turnaround_metrics['total'],
            compliant_turnarounds=turnaround_metrics['compliant'],
            turnaround_compliance_rate=turnaround_metrics['compliance_rate'],
            avg_turnaround_time_minutes=turnaround_metrics['avg_time'],
            min_turnaround_time_minutes=turnaround_metrics['min_time'],
            turnaround_violations=turnaround_metrics['violations'],
            
            # Energy
            total_daily_energy_kwh=energy_metrics['total_energy'],
            peak_power_demand_kw=energy_metrics['peak_power'],
            energy_efficiency_score=energy_metrics['efficiency'],
            battery_range_violations=energy_metrics['range_violations'],
            charging_opportunities=energy_metrics['charging_windows'],
            energy_constraint_violations=energy_metrics['violations'],
            
            # Certificates
            trains_with_expired_certs=cert_metrics['expired'],
            trains_with_expiring_soon_certs=cert_metrics['expiring_soon'],
            certificate_compliance_rate=cert_metrics['compliance_rate'],
            
            # Jobs
            trains_with_critical_jobs=job_metrics['critical'],
            trains_with_blocking_jobs=job_metrics['blocking'],
            job_constraint_violations=job_metrics['violations'],
            
            # Components
            trains_with_critical_components=component_metrics['critical'],
            trains_with_warning_components=component_metrics['warning'],
            component_constraint_violations=component_metrics['violations'],
            
            # Scores
            maintenance_score=scores['maintenance'],
            turnaround_score=scores['turnaround'],
            energy_score=scores['energy'],
            certificate_score=scores['certificate'],
            job_score=scores['job'],
            component_score=scores['component'],
            overall_constraint_score=scores['overall']
        )
    
    def _analyze_maintenance_constraints(self, trainsets: List[Dict], data: Dict) -> Dict:
        """Analyze maintenance window compliance."""
        trainset_status_map = {ts['trainset_id']: ts for ts in data.get('trainset_status', [])}
        
        needing_maintenance = 0
        scheduled_maintenance = 0
        overdue = 0
        violations = 0
        delay_days = []
        
        for train in trainsets:
            ts_id = train.get('trainset_id')
            status = train.get('status')
            ts_data = trainset_status_map.get(ts_id, {})
            
            mileage = ts_data.get('total_mileage_km', 0)
            last_service_str = ts_data.get('last_service_date', '')
            
            # Calculate if maintenance is needed
            km_since_service = mileage % self.MAINTENANCE_INTERVAL_KM
            is_overdue = mileage > 0 and km_since_service > (self.MAINTENANCE_OVERDUE_THRESHOLD_KM % self.MAINTENANCE_INTERVAL_KM)
            needs_maintenance = km_since_service > (self.MAINTENANCE_INTERVAL_KM * 0.9)  # Within 90% of interval
            
            if needs_maintenance:
                needing_maintenance += 1
                
                if status == 'MAINTENANCE':
                    scheduled_maintenance += 1
                elif is_overdue:
                    overdue += 1
                    # Calculate delay
                    try:
                        last_service = datetime.fromisoformat(last_service_str.replace('+05:30', ''))
                        days_since = (datetime.now() - last_service).days
                        expected_days = self.MAINTENANCE_INTERVAL_KM / (300)  # Assume 300 km/day avg
                        delay = max(0, days_since - expected_days)
                        delay_days.append(delay)
                    except:
                        pass
                
                # Check if scheduled but in wrong window (e.g., scheduled for service but still marked as in service)
                if status == 'REVENUE_SERVICE' and is_overdue:
                    violations += 1
        
        compliance_rate = (scheduled_maintenance / needing_maintenance * 100) if needing_maintenance > 0 else 100.0
        avg_delay = np.mean(delay_days) if delay_days else 0.0
        
        return {
            'needing': needing_maintenance,
            'scheduled': scheduled_maintenance,
            'compliance_rate': compliance_rate,
            'overdue': overdue,
            'violations': violations,
            'avg_delay': avg_delay
        }
    
    def _analyze_turnaround_constraints(self, trainsets: List[Dict]) -> Dict:
        """Analyze turnaround time adherence."""
        total_turnarounds = 0
        compliant_turnarounds = 0
        violations = 0
        turnaround_times = []
        
        for train in trainsets:
            service_blocks = train.get('service_blocks', [])
            
            if len(service_blocks) < 2:
                continue
            
            # Sort blocks by departure time
            sorted_blocks = sorted(service_blocks, key=lambda b: b.get('departure_time', '00:00'))
            
            for i in range(1, len(sorted_blocks)):
                prev_block = sorted_blocks[i-1]
                curr_block = sorted_blocks[i]
                
                try:
                    # Parse times
                    prev_time_str = prev_block.get('departure_time', '00:00')
                    curr_time_str = curr_block.get('departure_time', '00:00')
                    
                    prev_hour, prev_min = map(int, prev_time_str.split(':'))
                    curr_hour, curr_min = map(int, curr_time_str.split(':'))
                    
                    # Calculate estimated end time of previous block
                    prev_trip_count = prev_block.get('trip_count', 1)
                    prev_duration_hours = (prev_trip_count * self.ROUTE_LENGTH_KM * 2) / self.AVG_SPEED_KMH
                    
                    prev_end_minutes = prev_hour * 60 + prev_min + (prev_duration_hours * 60)
                    curr_start_minutes = curr_hour * 60 + curr_min
                    
                    # Turnaround time
                    turnaround = curr_start_minutes - prev_end_minutes
                    
                    if turnaround > 0:  # Only count positive turnarounds
                        total_turnarounds += 1
                        turnaround_times.append(turnaround)
                        
                        if turnaround >= self.MIN_TURNAROUND_TIME_MINUTES:
                            compliant_turnarounds += 1
                        else:
                            violations += 1
                except:
                    continue
        
        compliance_rate = (compliant_turnarounds / total_turnarounds * 100) if total_turnarounds > 0 else 100.0
        avg_time = np.mean(turnaround_times) if turnaround_times else 0.0
        min_time = min(turnaround_times) if turnaround_times else 0.0
        
        return {
            'total': total_turnarounds,
            'compliant': compliant_turnarounds,
            'compliance_rate': compliance_rate,
            'violations': violations,
            'avg_time': avg_time,
            'min_time': min_time
        }
    
    def _analyze_energy_constraints(self, trainsets: List[Dict]) -> Dict:
        """Analyze energy and battery constraints."""
        total_energy = 0.0
        peak_power = 0.0
        range_violations = 0
        charging_windows = 0
        violations = 0
        total_km = 0
        
        for train in trainsets:
            service_blocks = train.get('service_blocks', [])
            daily_km = train.get('daily_km_allocation', 0)
            
            # Calculate energy consumption
            for block in service_blocks:
                block_km = block.get('estimated_km', 0)
                block_energy = block_km * self.ENERGY_PER_KM_KWH
                total_energy += block_energy
                total_km += block_km
                
                # Estimate peak power (during acceleration)
                block_duration_hours = block.get('trip_count', 1) * (self.ROUTE_LENGTH_KM * 2) / self.AVG_SPEED_KMH
                if block_duration_hours > 0:
                    avg_power = block_energy / block_duration_hours
                    peak_power = max(peak_power, avg_power * 1.5)  # Peak is ~1.5x average
                
                # Check battery range violations (if block is too long without charging)
                if block_km > self.MAX_RANGE_KM:
                    range_violations += 1
                    violations += 1
            
            # Count charging opportunities (gaps between blocks)
            if len(service_blocks) > 1:
                charging_windows += len(service_blocks) - 1
            
            # Check daily energy limits
            if daily_km > self.MAX_DAILY_KM:
                violations += 1
        
        # Calculate efficiency
        efficiency = (total_energy / total_km) if total_km > 0 else 0.0
        
        return {
            'total_energy': total_energy,
            'peak_power': peak_power,
            'efficiency': efficiency,
            'range_violations': range_violations,
            'charging_windows': charging_windows,
            'violations': violations
        }
    
    def _analyze_certificate_constraints(self, trainsets: List[Dict], data: Dict) -> Dict:
        """Analyze fitness certificate constraints."""
        cert_map = defaultdict(list)
        for cert in data.get('fitness_certificates', []):
            cert_map[cert.get('trainset_id')].append(cert)
        
        expired = 0
        expiring_soon = 0
        total_service = 0
        
        for train in trainsets:
            if train.get('status') != 'REVENUE_SERVICE':
                continue
            
            total_service += 1
            ts_id = train.get('trainset_id')
            certs = cert_map.get(ts_id, [])
            
            has_expired = any(c.get('status') == 'Expired' for c in certs)
            has_expiring = any(c.get('status') == 'Expiring-Soon' for c in certs)
            
            if has_expired:
                expired += 1
            elif has_expiring:
                expiring_soon += 1
        
        compliance_rate = ((total_service - expired) / total_service * 100) if total_service > 0 else 100.0
        
        return {
            'expired': expired,
            'expiring_soon': expiring_soon,
            'compliance_rate': compliance_rate
        }
    
    def _analyze_job_constraints(self, trainsets: List[Dict], data: Dict) -> Dict:
        """Analyze job card constraints."""
        job_map = defaultdict(list)
        for job in data.get('job_cards', []):
            job_map[job.get('trainset_id')].append(job)
        
        critical = 0
        blocking = 0
        violations = 0
        
        for train in trainsets:
            if train.get('status') != 'REVENUE_SERVICE':
                continue
            
            ts_id = train.get('trainset_id')
            jobs = job_map.get(ts_id, [])
            
            critical_jobs = [j for j in jobs if j.get('priority') == 'Critical' and j.get('status') == 'Open']
            blocking_jobs = [j for j in jobs if j.get('status') in ['Open', 'In-Progress'] and j.get('priority') in ['Critical', 'High']]
            
            if critical_jobs:
                critical += 1
                violations += len(critical_jobs)
            
            if blocking_jobs:
                blocking += 1
        
        return {
            'critical': critical,
            'blocking': blocking,
            'violations': violations
        }
    
    def _analyze_component_constraints(self, trainsets: List[Dict], data: Dict) -> Dict:
        """Analyze component health constraints."""
        component_map = defaultdict(list)
        for comp in data.get('component_health', []):
            component_map[comp.get('trainset_id')].append(comp)
        
        critical = 0
        warning = 0
        violations = 0
        
        for train in trainsets:
            if train.get('status') != 'REVENUE_SERVICE':
                continue
            
            ts_id = train.get('trainset_id')
            components = component_map.get(ts_id, [])
            
            critical_comps = [c for c in components if c.get('status') == 'Critical']
            warning_comps = [c for c in components if c.get('status') == 'Warning']
            
            if critical_comps:
                critical += 1
                violations += len(critical_comps)
            
            if warning_comps:
                warning += 1
        
        return {
            'critical': critical,
            'warning': warning,
            'violations': violations
        }
    
    def _calculate_scores(self, maintenance: Dict, turnaround: Dict, energy: Dict,
                         cert: Dict, job: Dict, component: Dict) -> Dict:
        """Calculate constraint satisfaction scores (0-100)."""
        
        # Maintenance score
        maint_score = maintenance['compliance_rate']
        if maintenance['overdue'] > 0:
            maint_score -= maintenance['overdue'] * 10
        maint_score = max(0, min(100, maint_score))
        
        # Turnaround score
        turnaround_score = turnaround['compliance_rate']
        turnaround_score = max(0, min(100, turnaround_score))
        
        # Energy score
        energy_score = 100.0
        if energy['violations'] > 0:
            energy_score -= energy['violations'] * 15
        if energy['efficiency'] > self.ENERGY_PER_KM_KWH * 1.2:  # 20% over expected
            energy_score -= 10
        energy_score = max(0, min(100, energy_score))
        
        # Certificate score
        cert_score = cert['compliance_rate']
        cert_score = max(0, min(100, cert_score))
        
        # Job score
        job_score = 100.0
        if job['violations'] > 0:
            job_score -= job['violations'] * 20
        job_score = max(0, min(100, job_score))
        
        # Component score
        comp_score = 100.0
        if component['violations'] > 0:
            comp_score -= component['violations'] * 15
        comp_score = max(0, min(100, comp_score))
        
        # Overall weighted score
        overall = (
            maint_score * 0.25 +
            turnaround_score * 0.20 +
            energy_score * 0.15 +
            cert_score * 0.20 +
            job_score * 0.10 +
            comp_score * 0.10
        )
        
        return {
            'maintenance': maint_score,
            'turnaround': turnaround_score,
            'energy': energy_score,
            'certificate': cert_score,
            'job': job_score,
            'component': comp_score,
            'overall': overall
        }
