import re
import requests
import json
from urllib.parse import quote_plus

class LocationValidator:
    """Handles basic location input validation for weather applications"""
    
    def __init__(self):
        # Common location patterns and validations
        self.min_length = 2
        self.max_length = 100
        
        # Characters allowed in location names
        self.allowed_pattern = re.compile(r'^[a-zA-Z\s\-\',\.]+$')
        
        # Common location abbreviations to expand
        self.abbreviations = {
            'nyc': 'New York City',
            'la': 'Los Angeles',
            'sf': 'San Francisco',
            'chi': 'Chicago',
            'philly': 'Philadelphia'
        }
    
    def clean_location_input(self, location):
        """Clean and standardize location input"""
        if not location:
            return None, "Location cannot be empty"
        
        # Remove extra whitespace and convert to title case
        cleaned = location.strip().title()
        
        # Check length
        if len(cleaned) < self.min_length:
            return None, f"Location name too short (minimum {self.min_length} characters)"
        
        if len(cleaned) > self.max_length:
            return None, f"Location name too long (maximum {self.max_length} characters)"
        
        # Check for valid characters
        if not self.allowed_pattern.match(cleaned):
            return None, "Location contains invalid characters. Use only letters, spaces, hyphens, apostrophes, and periods."
        
        # Expand common abbreviations
        location_lower = cleaned.lower()
        if location_lower in self.abbreviations:
            cleaned = self.abbreviations[location_lower]
        
        return cleaned, "Valid location input"
    
    def validate_coordinates(self, latitude, longitude):
        """Validate GPS coordinates"""
        try:
            lat = float(latitude)
            lon = float(longitude)
            
            if not (-90 <= lat <= 90):
                return False, "Latitude must be between -90 and 90 degrees"
            
            if not (-180 <= lon <= 180):
                return False, "Longitude must be between -180 and 180 degrees"
            
            return True, "Valid coordinates"
            
        except (ValueError, TypeError):
            return False, "Coordinates must be valid numbers"

# Demonstrate location validation
validator = LocationValidator()

# Test various location inputs
test_locations = [
    "New York",
    "nyc",
    "san francisco",
    "123 Invalid!",
    "",
    "ThisLocationNameIsWayTooLongToBeValidForOurApplication",
    "Chicago"
]

print("Location Validation Results:")
print("=" * 40)

for location in test_locations:
    cleaned, message = validator.clean_location_input(location)
    if cleaned:
        print(f"✓ '{location}' → '{cleaned}' ({message})")
    else:
        print(f"✗ '{location}' → Error: {message}")

print("\nCoordinate Validation Results:")
print("=" * 40)

test_coordinates = [
    (40.7128, -74.0060),  # New York City
    (91, -74),            # Invalid latitude  
    (40, -181),           # Invalid longitude
    ("invalid", "coords")  # Invalid format
]

for lat, lon in test_coordinates:
    is_valid, message = validator.validate_coordinates(lat, lon)
    print(f"({lat}, {lon}): {message}")
