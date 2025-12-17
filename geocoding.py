"""
Location Geocoding Helper
Convert city/country names to coordinates
"""

# Simple coordinate database for common cities
CITY_COORDINATES = {
    # USA
    "new york": (40.7128, -74.0060),
    "los angeles": (34.0522, -118.2437),
    "chicago": (41.8781, -87.6298),
    "houston": (29.7604, -95.3698),
    "dallas": (32.7767, -96.7970),
    "miami": (25.7617, -80.1918),
    "san francisco": (37.7749, -122.4194),
    "seattle": (47.6062, -122.3321),
    
    # Europe
    "london": (51.5074, -0.1278),
    "paris": (48.8566, 2.3522),
    "berlin": (52.5200, 13.4050),
    "rome": (41.9028, 12.4964),
    "madrid": (40.4168, -3.7038),
    "athens": (37.9838, 23.7275),
    
    # Middle East
    "istanbul": (41.0082, 28.9784),
    "dubai": (25.2048, 55.2708),
    "beirut": (33.8886, 35.4955),
    "cairo": (30.0444, 31.2357),
    
    # Asia
    "tokyo": (35.6762, 139.6503),
    "beijing": (39.9042, 116.4074),
    "singapore": (1.3521, 103.8198),
    "bangkok": (13.7563, 100.5018),
    "mumbai": (19.0760, 72.8777),
    
    # Other
    "sydney": (-33.8688, 151.2093),
    "toronto": (43.6532, -79.3832),
    "mexico city": (19.4326, -99.1332),
}


def get_coordinates(city: str, country: str = None):
    """Get coordinates for a city"""
    city_lower = city.lower().strip()
    
    # Try exact match
    if city_lower in CITY_COORDINATES:
        return CITY_COORDINATES[city_lower]
    
    # Try with country
    if country:
        key = f"{city_lower}, {country.lower()}"
        if key in CITY_COORDINATES:
            return CITY_COORDINATES[key]
    
    # Default to approximate location based on country
    country_defaults = {
        "usa": (39.8283, -98.5795),
        "united states": (39.8283, -98.5795),
        "uk": (51.5074, -0.1278),
        "united kingdom": (51.5074, -0.1278),
        "turkey": (41.0082, 28.9784),
        "japan": (35.6762, 139.6503),
        "france": (48.8566, 2.3522),
        "germany": (52.5200, 13.4050),
    }
    
    if country:
        country_lower = country.lower().strip()
        if country_lower in country_defaults:
            return country_defaults[country_lower]
    
    # Ultimate fallback
    return (0.0, 0.0)
