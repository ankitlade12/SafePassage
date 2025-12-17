"""
Exit Playbook Generator
Creates personalized exit checklists and safe routes
"""

from models import ExitChecklist, ChecklistItem, Route, Location, Contact
from datetime import datetime
from typing import List


class ExitPlaybookGenerator:
    """Generate personalized exit plans"""
    
    def generate_checklist(self, user_location: Location, 
                          fallback_destination: Location,
                          emergency_contacts: List[Contact]) -> ExitChecklist:
        """Generate complete exit checklist"""
        
        items = self._generate_checklist_items(user_location, fallback_destination)
        routes = self._generate_safe_routes(user_location, fallback_destination)
        money_steps = self._generate_money_access_steps()
        embassy_info = self._get_embassy_info(user_location)
        
        return ExitChecklist(
            user_id="user_001",
            location=user_location,
            generated_at=datetime.now(),
            items=items,
            safe_routes=routes,
            emergency_contacts=emergency_contacts,
            money_access_steps=money_steps,
            embassy_info=embassy_info
        )
    
    def _generate_checklist_items(self, location: Location, 
                                  destination: Location) -> List[ChecklistItem]:
        """Generate prioritized checklist items"""
        return [
            ChecklistItem(
                item_id="item_001",
                title="Secure passport and travel documents",
                description="Ensure passport, visa, and ID are accessible",
                priority=1
            ),
            ChecklistItem(
                item_id="item_002",
                title="Contact U.S. Embassy/Consulate",
                description=f"Notify embassy of your situation and location",
                priority=1
            ),
            ChecklistItem(
                item_id="item_003",
                title="Book transportation to safe location",
                description=f"Arrange flight/transport to {destination.city}",
                priority=1
            ),
            ChecklistItem(
                item_id="item_004",
                title="Notify trusted contacts",
                description="Alert emergency contacts of your status",
                priority=2
            ),
            ChecklistItem(
                item_id="item_005",
                title="Withdraw available cash",
                description="Get local currency from ATM if still operational",
                priority=2
            ),
            ChecklistItem(
                item_id="item_006",
                title="Pack essential items only",
                description="Medications, documents, phone charger, cash",
                priority=3
            ),
            ChecklistItem(
                item_id="item_007",
                title="Check travel restrictions",
                description="Verify borders/airports are open",
                priority=2
            ),
            ChecklistItem(
                item_id="item_008",
                title="Backup important data",
                description="Save contacts, documents to cloud",
                priority=3
            )
        ]
    
    def _generate_safe_routes(self, from_loc: Location, 
                             to_loc: Location) -> List[Route]:
        """Generate realistic safe route options based on geography"""
        
        # Calculate approximate distance
        lat_diff = abs(from_loc.latitude - to_loc.latitude)
        lon_diff = abs(from_loc.longitude - to_loc.longitude)
        distance_km = ((lat_diff ** 2 + lon_diff ** 2) ** 0.5) * 111
        
        routes = []
        
        # Flight is always an option for international travel
        if distance_km > 500:  # Long distance - international flight
            flight_hours = int(distance_km / 800)  # Approx 800 km/h
            routes.append(Route(
                from_location=from_loc,
                to_location=to_loc,
                method="flight",
                estimated_time=f"{flight_hours}-{flight_hours+2} hours (including connections)",
                notes=f"International flight from {from_loc.city} to {to_loc.city}. Book earliest available flight. Check visa requirements."
            ))
        else:  # Short distance - direct flight
            routes.append(Route(
                from_location=from_loc,
                to_location=to_loc,
                method="flight",
                estimated_time="2-3 hours",
                notes=f"Direct flight from {from_loc.city} to {to_loc.city}"
            ))
        
        # Add land/sea routes only if geographically feasible
        same_continent = self._same_continent(from_loc, to_loc)
        
        if same_continent and distance_km < 2000:
            # Train/bus for nearby countries
            if distance_km < 1000:
                routes.append(Route(
                    from_location=from_loc,
                    to_location=to_loc,
                    method="train/bus",
                    estimated_time=f"{int(distance_km/80)}-{int(distance_km/60)} hours",
                    notes=f"Overland route via train or bus. Slower but may be available if airports close."
                ))
            
            # Ferry only for coastal cities
            if self._is_coastal_route(from_loc, to_loc):
                routes.append(Route(
                    from_location=from_loc,
                    to_location=to_loc,
                    method="ferry",
                    estimated_time=f"{int(distance_km/40)}-{int(distance_km/30)} hours",
                    notes="Ferry service if available. Check port operations and schedules."
                ))
        
        # If cross-continental, suggest nearby safe country first
        if not same_continent and distance_km > 5000:
            routes.append(Route(
                from_location=from_loc,
                to_location=Location("Nearest Safe City", from_loc.country, from_loc.latitude, from_loc.longitude),
                method="ground transport",
                estimated_time="4-8 hours",
                notes=f"First evacuate to nearest safe city/country, then arrange international flight to {to_loc.city}"
            ))
        
        return routes
    
    def _same_continent(self, loc1: Location, loc2: Location) -> bool:
        """Check if two locations are on the same continent"""
        # Simplified continent detection based on coordinates
        continents = {
            "north_america": (-170, -50, 15, 75),  # (lon_min, lon_max, lat_min, lat_max)
            "europe": (-10, 40, 35, 70),
            "asia": (40, 150, 10, 70),
            "africa": (-20, 55, -35, 37),
            "south_america": (-85, -35, -55, 15),
            "oceania": (110, 180, -50, 0)
        }
        
        def get_continent(loc):
            for cont, (lon_min, lon_max, lat_min, lat_max) in continents.items():
                if lon_min <= loc.longitude <= lon_max and lat_min <= loc.latitude <= lat_max:
                    return cont
            return "unknown"
        
        return get_continent(loc1) == get_continent(loc2)
    
    def _is_coastal_route(self, loc1: Location, loc2: Location) -> bool:
        """Check if route could feasibly use ferry (simplified)"""
        # Very simplified - just check if it's a short distance in Europe/Mediterranean
        # or Asia-Pacific region
        distance = ((loc1.latitude - loc2.latitude) ** 2 + (loc1.longitude - loc2.longitude) ** 2) ** 0.5 * 111
        
        # Mediterranean/Europe
        if 35 <= loc1.latitude <= 45 and -10 <= loc1.longitude <= 40:
            if distance < 500:
                return True
        
        # Asia-Pacific islands
        if 100 <= loc1.longitude <= 150 and -10 <= loc1.latitude <= 40:
            if distance < 300:
                return True
        
        return False
    
    def _generate_money_access_steps(self) -> List[str]:
        """Generate steps to access emergency funds"""
        return [
            "1. Open crypto wallet app on phone",
            "2. Verify funds received (check transaction)",
            "3. Convert to local currency if needed",
            "4. Use crypto ATM or exchange service",
            "5. Keep receipts for audit trail"
        ]
    
    def _get_embassy_info(self, location: Location) -> dict:
        """Get U.S. Embassy information"""
        # Simplified for demo
        embassy_map = {
            "Istanbul": {
                "name": "U.S. Consulate General Istanbul",
                "address": "Kaplicalar Mevkii No. 2, Istanbul",
                "phone": "+90 (212) 335-9000",
                "emergency": "+90 (212) 335-9000"
            },
            "Athens": {
                "name": "U.S. Embassy Athens",
                "address": "91 Vasilisis Sophias Avenue, Athens",
                "phone": "+30 210-721-2951",
                "emergency": "+30 210-721-2951"
            }
        }
        
        return embassy_map.get(location.city, {
            "name": "U.S. Embassy",
            "phone": "Contact State Department",
            "emergency": "+1-888-407-4747"
        })
