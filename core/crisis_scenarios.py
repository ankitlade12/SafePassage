"""
Crisis Scenarios Library
Pre-built realistic crisis scenarios for demo
"""

from models import RiskAlert, RiskType, Location
from datetime import datetime
from typing import Dict, List


class CrisisScenario:
    """Pre-built crisis scenario"""
    
    def __init__(self, name: str, location: Location, risk_type: RiskType,
                 severity: int, description: str, headline: str, 
                 detailed_info: str):
        self.name = name
        self.location = location
        self.risk_type = risk_type
        self.severity = severity
        self.description = description
        self.headline = headline
        self.detailed_info = detailed_info
    
    def to_alert(self) -> RiskAlert:
        """Convert scenario to RiskAlert"""
        return RiskAlert(
            alert_id=f"scenario_{self.name.lower().replace(' ', '_')}",
            location=self.location,
            risk_type=self.risk_type,
            severity=self.severity,
            source="Scenario Simulation",
            timestamp=datetime.now(),
            title=self.headline,
            description=self.description,
            affected_radius_km=50
        )


class CrisisScenarioLibrary:
    """Library of pre-built crisis scenarios"""
    
    def __init__(self):
        self.scenarios = self._create_scenarios()
    
    def _create_scenarios(self) -> Dict[str, CrisisScenario]:
        """Create all scenarios"""
        
        scenarios = {}
        
        # Istanbul Political Unrest
        scenarios["Istanbul Political Unrest"] = CrisisScenario(
            name="Istanbul Political Unrest",
            location=Location("Istanbul", "Turkey", 41.0082, 28.9784),
            risk_type=RiskType.POLITICAL_UNREST,
            severity=9,
            description="Major protests and civil unrest reported in Istanbul. Banks and ATMs closing. Payment systems disrupted. Immediate action recommended for travelers.",
            headline="🚨 BREAKING: Mass protests in Istanbul - Payment systems disrupted",
            detailed_info="""
**Situation Update:**
- Widespread protests in central Istanbul
- Banks implementing emergency closures
- ATM network experiencing outages
- Public transportation disrupted
- Airport operations affected

**Recommendations:**
- Activate emergency fund immediately
- Move to safe location
- Contact embassy
- Book earliest available flight
            """
        )
        
        # Beirut Banking Crisis
        scenarios["Beirut Banking Crisis"] = CrisisScenario(
            name="Beirut Banking Crisis",
            location=Location("Beirut", "Lebanon", 33.8886, 35.4955),
            risk_type=RiskType.PAYMENT_DISRUPTION,
            severity=8,
            description="Banking sector collapse. Capital controls in effect. Severe restrictions on cash withdrawals. Foreign currency unavailable.",
            headline="💰 ALERT: Lebanese banks impose strict withdrawal limits",
            detailed_info="""
**Situation Update:**
- Banks limiting withdrawals to $200/week
- Capital controls preventing transfers
- Foreign currency exchange suspended
- Long queues at banks and ATMs
- Black market exchange rates surging

**Recommendations:**
- Use crypto or mobile money for liquidity
- Avoid local banking system
- Secure alternative payment methods
- Plan exit if situation worsens
            """
        )
        
        # Tokyo Earthquake
        scenarios["Tokyo Earthquake"] = CrisisScenario(
            name="Tokyo Earthquake",
            location=Location("Tokyo", "Japan", 35.6762, 139.6503),
            risk_type=RiskType.NATURAL_DISASTER,
            severity=7,
            description="Major earthquake hits Tokyo region. Infrastructure damage. Transportation disrupted. Power outages reported.",
            headline="🌊 URGENT: 7.2 magnitude earthquake hits Tokyo region",
            detailed_info="""
**Situation Update:**
- 7.2 magnitude earthquake
- Aftershocks continuing
- Train services suspended
- Some buildings damaged
- Power outages in affected areas
- No tsunami warning

**Recommendations:**
- Move to designated safe zones
- Avoid damaged buildings
- Monitor aftershock alerts
- Prepare for potential evacuation
- Ensure emergency supplies
            """
        )
        
        # Kyiv Security Alert
        scenarios["Kyiv Security Alert"] = CrisisScenario(
            name="Kyiv Security Alert",
            location=Location("Kyiv", "Ukraine", 50.4501, 30.5234),
            risk_type=RiskType.SECURITY_THREAT,
            severity=10,
            description="Armed conflict escalating. State Department issues Level 4 - Do Not Travel. Immediate evacuation recommended for all U.S. citizens.",
            headline="⚠️ CRITICAL: State Dept issues Level 4 - Do Not Travel",
            detailed_info="""
**Situation Update:**
- Active armed conflict
- Airspace closed
- Border crossings congested
- Embassy operations limited
- Communication networks unstable

**Recommendations:**
- Evacuate immediately
- Use land routes to Poland/Romania
- Register with embassy
- Activate all emergency protocols
- Maintain low profile
            """
        )
        
        # Cairo Internet Shutdown
        scenarios["Cairo Internet Shutdown"] = CrisisScenario(
            name="Cairo Internet Shutdown",
            location=Location("Cairo", "Egypt", 30.0444, 31.2357),
            risk_type=RiskType.PAYMENT_DISRUPTION,
            severity=6,
            description="Government-ordered internet shutdown. Digital payment systems offline. Cash-only economy.",
            headline="📵 ALERT: Internet shutdown affects digital payments",
            detailed_info="""
**Situation Update:**
- Nationwide internet blackout
- Mobile data services suspended
- Credit card systems offline
- ATMs not functioning
- Cash-only transactions

**Recommendations:**
- Withdraw maximum cash immediately
- Use cash pickup services
- Avoid digital payment reliance
- Maintain physical currency reserves
            """
        )
        
        return scenarios
    
    def get_scenario(self, name: str) -> CrisisScenario:
        """Get scenario by name"""
        return self.scenarios.get(name)
    
    def get_all_scenarios(self) -> List[CrisisScenario]:
        """Get all scenarios"""
        return list(self.scenarios.values())
    
    def get_scenario_names(self) -> List[str]:
        """Get all scenario names"""
        return list(self.scenarios.keys())
    
    def activate_scenario(self, name: str) -> RiskAlert:
        """Activate a scenario and return alert"""
        scenario = self.get_scenario(name)
        if scenario:
            return scenario.to_alert()
        return None
