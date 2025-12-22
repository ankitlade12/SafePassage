"""
Risk Monitoring System
Simulates real-time risk alerts for demo
"""

from models import RiskAlert, RiskType, Location
from datetime import datetime
from typing import List
import random


class RiskMonitor:
    """Monitor and generate risk alerts"""

    def __init__(self):
        self.active_alerts: List[RiskAlert] = []

    def get_current_risk_level(self, location: Location) -> int:
        """Calculate current risk level for location (1-10)"""
        # Check for active alerts near location
        nearby_alerts = self.get_nearby_alerts(location, radius_km=100)

        if not nearby_alerts:
            return random.randint(1, 3)  # Normal baseline

        # Return highest severity from nearby alerts
        return max(alert.severity for alert in nearby_alerts)

    def get_nearby_alerts(
        self, location: Location, radius_km: float = 100
    ) -> List[RiskAlert]:
        """Get alerts within radius of location"""
        # Simplified distance check for demo
        nearby = []
        for alert in self.active_alerts:
            if self._is_nearby(location, alert.location, radius_km):
                nearby.append(alert)
        return nearby

    def _is_nearby(self, loc1: Location, loc2: Location, radius_km: float) -> bool:
        """Simple distance check (for demo)"""
        # Rough approximation: 1 degree ≈ 111 km
        lat_diff = abs(loc1.latitude - loc2.latitude)
        lon_diff = abs(loc1.longitude - loc2.longitude)
        distance_approx = ((lat_diff**2 + lon_diff**2) ** 0.5) * 111
        return distance_approx <= radius_km

    def trigger_crisis_simulation(self, location: Location) -> RiskAlert:
        """Simulate a crisis event (for demo)"""
        alert = RiskAlert(
            alert_id=f"alert_{datetime.now().timestamp()}",
            location=location,
            risk_type=RiskType.POLITICAL_UNREST,
            severity=9,
            source="Reuters",
            timestamp=datetime.now(),
            title=f"Political Unrest in {location.city}",
            description=f"Major protests and civil unrest reported in {location.city}. Banks and ATMs closing. Payment systems disrupted. Immediate action recommended for travelers.",
            affected_radius_km=50,
        )

        self.active_alerts.append(alert)
        return alert

    def generate_sample_alerts(self) -> List[RiskAlert]:
        """Generate sample alerts for demo"""
        alerts = [
            RiskAlert(
                alert_id="alert_001",
                location=Location("Beirut", "Lebanon", 33.8886, 35.4955),
                risk_type=RiskType.PAYMENT_DISRUPTION,
                severity=6,
                source="BBC News",
                timestamp=datetime.now(),
                title="Banking Crisis in Lebanon",
                description="Ongoing banking restrictions and currency controls",
                affected_radius_km=100,
            ),
            RiskAlert(
                alert_id="alert_002",
                location=Location("Kyiv", "Ukraine", 50.4501, 30.5234),
                risk_type=RiskType.SECURITY_THREAT,
                severity=8,
                source="State Department",
                timestamp=datetime.now(),
                title="Security Alert - Ukraine",
                description="Heightened security concerns. Avoid non-essential travel.",
                affected_radius_km=200,
            ),
        ]

        self.active_alerts.extend(alerts)
        return alerts

    def clear_alerts(self):
        """Clear all active alerts"""
        self.active_alerts = []
