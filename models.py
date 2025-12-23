"""
Safe-Passage Data Models
Core data structures for emergency liquidity system
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class RiskType(Enum):
    """Types of risk events"""
    POLITICAL_UNREST = "political_unrest"
    NATURAL_DISASTER = "natural_disaster"
    PAYMENT_DISRUPTION = "payment_disruption"
    HEALTH_EMERGENCY = "health_emergency"
    SECURITY_THREAT = "security_threat"


class PayoutMethod(Enum):
    """Available payout methods"""
    CRYPTO_WALLET = "crypto_wallet"
    WIRE_TRANSFER = "wire_transfer"
    CASH_PICKUP = "cash_pickup"
    MOBILE_MONEY = "mobile_money"


class FundStatus(Enum):
    """Exit fund status"""
    ACTIVE = "active"
    TRIGGERED = "triggered"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class Location:
    """Geographic location"""
    city: str
    country: str
    latitude: float
    longitude: float
    
    def __str__(self):
        return f"{self.city}, {self.country}"


@dataclass
class Contact:
    """Emergency contact"""
    name: str
    relationship: str
    phone: str
    email: str
    notify_on_trigger: bool = True


@dataclass
class ExitFund:
    """Pre-funded emergency liquidity"""
    user_id: str
    amount: float
    currency: str
    payout_methods: List[PayoutMethod]
    trusted_contacts: List[Contact]
    fallback_destinations: List[Location]
    status: FundStatus
    created_at: datetime
    triggered_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    def get_payout_eta(self, method: PayoutMethod) -> str:
        """Estimate time to access funds"""
        eta_map = {
            PayoutMethod.CRYPTO_WALLET: "15 minutes",
            PayoutMethod.MOBILE_MONEY: "30 minutes",
            PayoutMethod.CASH_PICKUP: "2-4 hours",
            PayoutMethod.WIRE_TRANSFER: "2-3 business days"
        }
        return eta_map.get(method, "Unknown")


@dataclass
class RiskAlert:
    """Risk event alert"""
    alert_id: str
    location: Location
    risk_type: RiskType
    severity: int  # 1-10 scale
    source: str
    timestamp: datetime
    title: str
    description: str
    affected_radius_km: float
    
    def is_critical(self) -> bool:
        """Check if alert is critical (severity >= 7)"""
        return self.severity >= 7
    
    def get_severity_label(self) -> str:
        """Get human-readable severity"""
        if self.severity >= 9:
            return "EXTREME"
        elif self.severity >= 7:
            return "HIGH"
        elif self.severity >= 5:
            return "MODERATE"
        else:
            return "LOW"


@dataclass
class ChecklistItem:
    """Item in exit checklist"""
    item_id: str
    title: str
    description: str
    priority: int  # 1 (highest) to 5 (lowest)
    completed: bool = False
    
    def __lt__(self, other):
        return self.priority < other.priority


@dataclass
class Route:
    """Safe route option"""
    from_location: Location
    to_location: Location
    method: str  # "flight", "train", "car", "ferry"
    estimated_time: str
    notes: str


@dataclass
class ExitChecklist:
    """Personalized exit plan"""
    user_id: str
    location: Location
    generated_at: datetime
    items: List[ChecklistItem]
    safe_routes: List[Route]
    emergency_contacts: List[Contact]
    money_access_steps: List[str]
    embassy_info: Optional[dict] = None
    
    def get_critical_items(self) -> List[ChecklistItem]:
        """Get priority 1-2 items"""
        return sorted([item for item in self.items if item.priority <= 2])
    
    def completion_percentage(self) -> float:
        """Calculate completion percentage"""
        if not self.items:
            return 0.0
        completed = sum(1 for item in self.items if item.completed)
        return (completed / len(self.items)) * 100


@dataclass
class UserProfile:
    """User profile and preferences"""
    user_id: str
    name: str
    email: str
    phone: str
    current_location: Location
    home_country: str
    passport_country: str
    notification_preferences: dict
    exit_fund: Optional[ExitFund] = None
    
    def has_active_fund(self) -> bool:
        """Check if user has active exit fund"""
        return self.exit_fund is not None and self.exit_fund.status == FundStatus.ACTIVE


@dataclass
class EmergencyActivation:
    """Record of emergency activation"""
    activation_id: str
    user_id: str
    triggered_by_alert: str
    timestamp: datetime
    payout_method: PayoutMethod
    payout_amount: float
    payout_currency: str
    status: str  # "initiated", "processing", "completed", "failed"
    completion_time: Optional[datetime] = None
    notes: str = ""
    
    def get_audit_log(self) -> dict:
        """Generate audit log entry"""
        return {
            "activation_id": self.activation_id,
            "user_id": self.user_id,
            "trigger": self.triggered_by_alert,
            "timestamp": self.timestamp.isoformat(),
            "payout": {
                "method": self.payout_method.value,
                "amount": self.payout_amount,
                "currency": self.payout_currency
            },
            "status": self.status,
            "completed_at": self.completion_time.isoformat() if self.completion_time else None
        }


# Sample data for demo
def create_sample_profile() -> UserProfile:
    """Create sample user profile with high-risk location for impactful demo"""
    # HIGH-RISK current location for demo impact
    kyiv = Location(
        city="Kyiv",
        country="Ukraine",
        latitude=50.4501,
        longitude=30.5234
    )
    
    # SAFE fallback destination
    lisbon = Location(
        city="Lisbon",
        country="Portugal",
        latitude=38.7223,
        longitude=-9.1393
    )
    
    contacts = [
        Contact(
            name="John Smith",
            relationship="Emergency Contact",
            phone="+1-999-999-9999",
            email="john@example.com"
        )
    ]
    
    exit_fund = ExitFund(
        user_id="user_001",
        amount=5000.0,
        currency="USD",
        payout_methods=[
            PayoutMethod.CRYPTO_WALLET, 
            PayoutMethod.WIRE_TRANSFER,
            PayoutMethod.CASH_PICKUP,
            PayoutMethod.MOBILE_MONEY
        ],
        trusted_contacts=contacts,
        fallback_destinations=[lisbon],
        status=FundStatus.ACTIVE,
        created_at=datetime.now()
    )
    
    return UserProfile(
        user_id="user_001",
        name="Sarah Johnson",
        email="user@gmail.com",
        phone="+1-999-999-9999",
        current_location=kyiv,
        home_country="United States",
        passport_country="United States",
        notification_preferences={
            "email": True,
            "sms": True,
            "push": True
        },
        exit_fund=exit_fund
    )
