export interface ServiceBlock {
  block_id: string;
  departure_time: string;
  origin: string;
  destination: string;
  trip_count: number;
  estimated_km: number;
}

export interface Trainset {
  trainset_id: string;
  status: 'REVENUE_SERVICE' | 'STANDBY' | 'MAINTENANCE';
  readiness_score: number;
  daily_km_allocation: number;
  cumulative_km: number;
  assigned_duty: string | null;
  priority_rank: number | null;
  service_blocks: ServiceBlock[] | null;
  stabling_bay: string | null;
  standby_reason: string | null;
  maintenance_type: string | null;
  ibl_bay: string | null;
  estimated_completion: string | null;
  alerts: string[];
}

export interface FleetSummary {
  total_trainsets: number;
  revenue_service: number;
  standby: number;
  maintenance: number;
  availability_percent: number;
}

export interface OptimizationMetrics {
  fitness_score: number;
  method: string;
  mileage_variance_coefficient: number;
  total_planned_km: number;
  optimization_runtime_ms: number;
}

export interface GlobalAlert {
  trainset_id: string;
  severity: 'LOW' | 'MEDIUM' | 'HIGH';
  alert_type: string;
  message: string;
}

export interface ScheduleData {
  schedule_id: string;
  generated_at: string;
  valid_from: string;
  valid_until: string;
  depot: string;
  trainsets: Trainset[];
  fleet_summary: FleetSummary;
  optimization_metrics: OptimizationMetrics;
  alerts: GlobalAlert[];
}
