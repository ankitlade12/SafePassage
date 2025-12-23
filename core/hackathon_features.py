"""
Hackathon Features Module
Advanced features for Safe-Passage hackathon demo:
- Dead Man's Switch
- Guardian Network
- Shadow Banking Mode
- Proof of Reserves
- Chaos Simulator
"""

import hashlib
import secrets
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class CheckInStatus(Enum):
    """Status of Dead Man's Switch"""
    ACTIVE = "active"
    WARNING = "warning"  # < 1 hour remaining
    EXPIRED = "expired"
    DISABLED = "disabled"


@dataclass
class Guardian:
    """Guardian contact for multi-sig safety"""
    name: str
    phone: str
    email: str
    is_active: bool = True
    notified_at: Optional[datetime] = None


@dataclass
class DeadManSwitch:
    """Timer-based safety check-in system"""
    enabled: bool = False
    interval_hours: int = 8
    last_checkin: datetime = field(default_factory=datetime.now)
    auto_payout_enabled: bool = True
    
    def check_in(self) -> None:
        """Record a check-in"""
        self.last_checkin = datetime.now()
    
    def get_time_remaining(self) -> timedelta:
        """Get time until switch triggers"""
        deadline = self.last_checkin + timedelta(hours=self.interval_hours)
        remaining = deadline - datetime.now()
        return max(remaining, timedelta(0))
    
    def get_status(self) -> CheckInStatus:
        """Get current status"""
        if not self.enabled:
            return CheckInStatus.DISABLED
        
        remaining = self.get_time_remaining()
        if remaining.total_seconds() <= 0:
            return CheckInStatus.EXPIRED
        elif remaining.total_seconds() < 3600:  # < 1 hour
            return CheckInStatus.WARNING
        else:
            return CheckInStatus.ACTIVE
    
    def format_remaining(self) -> str:
        """Format remaining time as string"""
        remaining = self.get_time_remaining()
        hours = int(remaining.total_seconds() // 3600)
        minutes = int((remaining.total_seconds() % 3600) // 60)
        return f"{hours}h {minutes}m"


class GuardianNetwork:
    """Multi-sig safety contact management"""
    
    def __init__(self, guardians: List[Guardian] = None):
        self.guardians = guardians or []
        self.alert_threshold = 7  # Risk level to trigger alerts (matches user preference)
    
    def add_guardian(self, name: str, phone: str, email: str) -> Guardian:
        """Add a new guardian"""
        if len(self.guardians) >= 3:
            raise ValueError("Maximum 3 guardians allowed")
        
        guardian = Guardian(name=name, phone=phone, email=email)
        self.guardians.append(guardian)
        return guardian
    
    def remove_guardian(self, index: int) -> None:
        """Remove guardian by index"""
        if 0 <= index < len(self.guardians):
            self.guardians.pop(index)
    
    def notify_all(self) -> List[dict]:
        """Simulate notifying all active guardians"""
        notifications = []
        for guardian in self.guardians:
            if guardian.is_active:
                guardian.notified_at = datetime.now()
                notifications.append({
                    "guardian": guardian.name,
                    "phone": guardian.phone,
                    "email": guardian.email,
                    "notified_at": guardian.notified_at.isoformat(),
                    "message": f"🚨 ALERT: Your protected contact has triggered a safety alert. Risk level is CRITICAL."
                })
        return notifications
    
    def should_alert(self, risk_level: int) -> bool:
        """Check if guardians should be alerted"""
        return risk_level >= self.alert_threshold and len(self.guardians) > 0


@dataclass
class ShadowBankingCode:
    """One-time offline redemption code"""
    code: str
    verification_hash: str
    amount: float
    currency: str
    created_at: datetime
    expires_at: datetime
    redeemed: bool = False
    
    @classmethod
    def generate(cls, amount: float, currency: str, valid_hours: int = 72) -> "ShadowBankingCode":
        """Generate a new one-time code"""
        # Generate a secure random code
        code_part = secrets.token_hex(4).upper()
        code = f"SP-{code_part[:4]}-{code_part[4:]}"
        
        # Create verification hash
        hash_input = f"{code}{amount}{currency}{datetime.now().isoformat()}"
        verification_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16].upper()
        
        now = datetime.now()
        return cls(
            code=code,
            verification_hash=verification_hash,
            amount=amount,
            currency=currency,
            created_at=now,
            expires_at=now + timedelta(hours=valid_hours)
        )
    
    def is_valid(self) -> bool:
        """Check if code is still valid"""
        return not self.redeemed and datetime.now() < self.expires_at


class ShadowBankingMode:
    """Offline emergency fund access system"""
    
    # Partner network with realistic details
    PARTNER_AGENTS = [
        {"name": "Wise (TransferWise)", "type": "Digital Transfer", "locations": "80+ currencies, instant"},
        {"name": "Western Union", "type": "Cash Pickup", "locations": "500K+ locations globally"},
        {"name": "Binance P2P", "type": "Crypto → Local", "locations": "Available in Ukraine"},
        {"name": "PrivatBank", "type": "Local ATM Network", "locations": "Ukraine & Poland"},
    ]
    
    def __init__(self):
        self.active_codes: List[ShadowBankingCode] = []
    
    def generate_offline_code(self, amount: float, currency: str) -> ShadowBankingCode:
        """Generate a new offline redemption code"""
        code = ShadowBankingCode.generate(amount, currency)
        self.active_codes.append(code)
        return code
    
    def get_qr_data(self, code: ShadowBankingCode) -> dict:
        """Get data for QR code generation"""
        return {
            "type": "SAFE_PASSAGE_OFFLINE",
            "code": code.code,
            "hash": code.verification_hash,
            "amount": code.amount,
            "currency": code.currency,
            "expires": code.expires_at.isoformat(),
        }
    
    def get_partner_agents(self) -> List[dict]:
        """Get list of partner agents"""
        return self.PARTNER_AGENTS


@dataclass
class ProofOfReserves:
    """Simulated blockchain verification for exit fund"""
    
    # Mock blockchain data
    vault_address: str = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"
    chain_name: str = "Base"
    chain_id: int = 8453
    
    def __init__(self, amount: float = 5000.0, currency: str = "USDC"):
        self.amount = amount
        self.currency = currency
        self.last_verified = datetime.now()
        self.tx_hash = self._generate_tx_hash()
    
    def _generate_tx_hash(self) -> str:
        """Generate a realistic-looking transaction hash"""
        return "0x" + secrets.token_hex(32)
    
    def get_verification_data(self) -> dict:
        """Get on-chain verification display data"""
        return {
            "vault_address": self.vault_address,
            "short_address": f"{self.vault_address[:6]}...{self.vault_address[-4:]}",
            "chain": self.chain_name,
            "chain_id": self.chain_id,
            "balance": f"{self.amount:,.2f} {self.currency}",
            "last_verified": self.last_verified.strftime("%Y-%m-%d %H:%M"),
            "tx_hash": self.tx_hash,
            "short_tx": f"{self.tx_hash[:10]}...{self.tx_hash[-6:]}",
            "explorer_url": f"https://basescan.org/address/{self.vault_address}",
            "verified": True
        }
    
    def refresh_verification(self) -> None:
        """Simulate refreshing on-chain verification"""
        self.last_verified = datetime.now()
        self.tx_hash = self._generate_tx_hash()


class ChaosSimulator:
    """Demo chaos simulator for live risk adjustment"""
    
    CHAOS_LEVELS = {
        0: {"label": "Peace", "emoji": "🕊️", "description": "All systems normal"},
        1: {"label": "Low", "emoji": "🟢", "description": "Minor activity detected"},
        2: {"label": "Low", "emoji": "🟢", "description": "Elevated monitoring"},
        3: {"label": "Low", "emoji": "🟢", "description": "Some concerns noted"},
        4: {"label": "Low", "emoji": "🟡", "description": "Regional news activity"},
        5: {"label": "Moderate", "emoji": "🟡", "description": "Travel advisory active"},
        6: {"label": "Moderate", "emoji": "🟡", "description": "Exercise caution advised"},
        7: {"label": "High", "emoji": "🟠", "description": "Significant instability"},
        8: {"label": "High", "emoji": "🔴", "description": "Capital controls possible"},
        9: {"label": "Extreme", "emoji": "🚨", "description": "Evacuation recommended"},
        10: {"label": "Extreme", "emoji": "⚔️", "description": "Immediate action required"},
    }
    
    def __init__(self):
        self.current_level = 2  # Default starting level
        self.alerts = []  # Store real alerts for network effect calculation
    
    def set_level(self, level: int) -> None:
        """Set chaos level (0-10)"""
        self.current_level = max(0, min(10, level))
    
    def set_alerts(self, alerts: list) -> None:
        """Set real alerts from GDELT/USGS/State Dept"""
        self.alerts = alerts or []
    
    def get_level_info(self) -> dict:
        """Get current level information"""
        return self.CHAOS_LEVELS.get(self.current_level, self.CHAOS_LEVELS[5])
    
    def get_network_effects(self) -> dict:
        """Get network effects - uses real alert data if available, otherwise based on level"""
        # If we have real alerts, analyze them
        if self.alerts:
            return self._analyze_alerts_for_network_effects()
        
        # Otherwise, use level-based simulation
        return self._get_level_based_effects()
    def _analyze_alerts_for_network_effects(self) -> dict:
        """
        Realistic network status based on actual alert types and severity.
        """
        # Default: all networks online
        status = {
            "banking": "ONLINE",
            "atm": "ONLINE",
            "crypto": "ONLINE",
            "mobile_money": "ONLINE",
            "cash_pickup": "ONLINE",
        }
        
        if not self.alerts:
            return status
        
        for alert in self.alerts:
            risk_type = getattr(alert, 'risk_type', None)
            severity = getattr(alert, 'severity', 0)
            description = getattr(alert, 'description', '').lower()
            title = getattr(alert, 'title', '').lower()
            
            if not risk_type:
                continue
            
            risk_value = risk_type.value if hasattr(risk_type, 'value') else str(risk_type)
            
            # NATURAL DISASTERS affect infrastructure
            if 'natural' in risk_value or 'disaster' in risk_value or 'earthquake' in title:
                if severity >= 7:
                    status["atm"] = "OFFLINE"
                    status["mobile_money"] = "RESTRICTED"
                elif severity >= 5:
                    status["atm"] = "CONGESTED"
                    status["mobile_money"] = "CONGESTED"
            
            # PAYMENT DISRUPTIONS affect banking
            if 'payment' in risk_value or 'disruption' in risk_value:
                if severity >= 7:
                    status["banking"] = "OFFLINE"
                    status["atm"] = "OFFLINE"
                elif severity >= 5:
                    status["banking"] = "CONGESTED"
            
            # SECURITY THREATS / ARMED CONFLICT - HIGH SEVERITY (8+) affects networks
            if 'security' in risk_value or 'conflict' in description or 'armed' in description:
                if severity >= 9:
                    # Level 4 "Do Not Travel" - severe impact
                    status["banking"] = "RESTRICTED"
                    status["atm"] = "OFFLINE"
                    status["cash_pickup"] = "OFFLINE"
                    status["mobile_money"] = "RESTRICTED"
                elif severity >= 7:
                    status["banking"] = "CONGESTED"
                    status["atm"] = "RESTRICTED"
                    status["cash_pickup"] = "CONGESTED"
            
            # POLITICAL UNREST at high severity
            if 'political' in risk_value or 'unrest' in risk_value:
                if severity >= 8:
                    status["banking"] = "CONGESTED"
                    status["atm"] = "CONGESTED"
                    status["cash_pickup"] = "CONGESTED"
        
        # Crypto stays most resilient (only internet needed)
        if status["banking"] == "OFFLINE":
            status["crypto"] = "CONGESTED"  # Slight impact in extreme scenarios
        else:
            status["crypto"] = "ONLINE"
        
        return status
    
    def _get_level_based_effects(self) -> dict:
        """Get simulated network effects based on chaos level (fallback)"""
        level = self.current_level
        
        if level <= 2:
            return {
                "banking": "ONLINE",
                "atm": "ONLINE",
                "crypto": "ONLINE",
                "mobile_money": "ONLINE",
                "cash_pickup": "ONLINE",
            }
        elif level <= 5:
            return {
                "banking": "CONGESTED",
                "atm": "ONLINE",
                "crypto": "ONLINE",
                "mobile_money": "ONLINE",
                "cash_pickup": "CONGESTED",
            }
        elif level <= 7:
            return {
                "banking": "RESTRICTED",
                "atm": "RESTRICTED",
                "crypto": "CONGESTED",
                "mobile_money": "ONLINE",
                "cash_pickup": "RESTRICTED",
            }
        else:
            return {
                "banking": "OFFLINE",
                "atm": "OFFLINE",
                "crypto": "ONLINE",
                "mobile_money": "RESTRICTED",
                "cash_pickup": "OFFLINE",
            }

