"""
Feature Engineering for Schedule ML Model
Extract features from schedule data for training
"""
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime
from .config import CONFIG


class FeatureExtractor:
    """Extract features from schedule data"""
    
    @staticmethod
    def extract_from_schedule(schedule: Dict) -> Dict[str, float]:
        """Extract features from a single schedule"""
        features = {}
        
        # Basic counts
        trainsets = schedule.get("trainsets", [])
        features["num_trains"] = len(trainsets)
        
        # Status counts
        status_counts = {}
        for train in trainsets:
            status = train.get("status", "UNKNOWN")
            status_counts[status] = status_counts.get(status, 0) + 1
        
        features["num_available"] = (
            status_counts.get("REVENUE_SERVICE", 0) + 
            status_counts.get("STANDBY", 0)
        )
        features["maintenance_count"] = status_counts.get("MAINTENANCE", 0)
        
        # Readiness scores
        readiness_scores = [
            t.get("readiness_score", 0.0) for t in trainsets
        ]
        features["avg_readiness_score"] = np.mean(readiness_scores) if readiness_scores else 0.0
        features["min_readiness_score"] = np.min(readiness_scores) if readiness_scores else 0.0
        
        # Mileage statistics
        mileages = [t.get("cumulative_km", 0) for t in trainsets]
        if mileages:
            features["total_mileage"] = sum(mileages)
            features["avg_mileage"] = np.mean(mileages)
            features["mileage_variance"] = np.var(mileages)
        else:
            features["total_mileage"] = 0
            features["avg_mileage"] = 0
            features["mileage_variance"] = 0
        
        # Certificate expiry
        certificate_issues = 0
        for train in trainsets:
            certs = train.get("fitness_certificates", {})
            for cert_type, cert_data in certs.items():
                if isinstance(cert_data, dict):
                    status = cert_data.get("status", "VALID")
                    if status in ["EXPIRED", "EXPIRING_SOON"]:
                        certificate_issues += 1
        features["certificate_expiry_count"] = certificate_issues
        
        # Branding priority
        branding_score = 0
        priority_map = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1, "NONE": 0}
        for train in trainsets:
            branding = train.get("branding", {})
            if isinstance(branding, dict):
                priority = branding.get("exposure_priority", "NONE")
                branding_score += priority_map.get(priority, 0)
        features["branding_priority_sum"] = branding_score
        
        # Time features
        try:
            generated_at = datetime.fromisoformat(
                schedule.get("generated_at", "").replace("+05:30", "")
            )
            features["time_of_day"] = generated_at.hour
            features["day_of_week"] = generated_at.weekday()
        except:
            features["time_of_day"] = 12
            features["day_of_week"] = 0
        
        return features
    
    @staticmethod
    def calculate_target(schedule: Dict) -> float:
        """Calculate quality score (target variable)"""
        metrics = schedule.get("optimization_metrics", {})
        
        # Weighted quality score
        score = 0.0
        
        # Component 1: Readiness (0-30 points)
        avg_readiness = metrics.get("avg_readiness_score", 0.0)
        score += avg_readiness * 30
        
        # Component 2: Availability (0-25 points)
        fleet_summary = schedule.get("fleet_summary", {})
        availability = fleet_summary.get("availability_percent", 0.0)
        score += (availability / 100) * 25
        
        # Component 3: Mileage balance (0-20 points)
        mileage_var = metrics.get("mileage_variance_coefficient", 1.0)
        score += max(0, (1 - mileage_var) * 20)
        
        # Component 4: Branding compliance (0-15 points)
        branding_sla = metrics.get("branding_sla_compliance", 0.0)
        score += branding_sla * 15
        
        # Component 5: No violations (0-10 points)
        violations = metrics.get("fitness_expiry_violations", 0)
        score += max(0, 10 - violations * 2)
        
        return min(100.0, score)
    
    def prepare_dataset(self, schedules: List[Dict]) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare feature matrix and target vector"""
        X = []
        y = []
        
        for schedule_data in schedules:
            schedule = schedule_data.get("schedule", schedule_data)
            
            try:
                features = self.extract_from_schedule(schedule)
                target = self.calculate_target(schedule)
                
                # Convert to feature vector in correct order
                feature_vector = [features.get(f, 0.0) for f in CONFIG.FEATURES] # type: ignore
                
                X.append(feature_vector)
                y.append(target)
            except Exception as e:
                print(f"Error extracting features: {e}")
                continue
        
        return np.array(X), np.array(y)
