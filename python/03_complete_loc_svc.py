## Creating a Complete Location Service:
class WeatherLocationService:
    """Complete location service for weather applications"""
    
    def __init__(self):
        self.validator = LocationValidator()
        self.geocoder = SimpleGeocoder()
        self.location_cache = {}  # Simple cache to avoid repeated API calls
    
    def process_location_request(self, user_input):
        """
        Process a complete location request from user input
        
        Returns:
            dict with location data ready for weather API, or error information
        """
        # Step 1: Validate and clean input
        cleaned_location, validation_message = self.validator.clean_location_input(user_input)
        
        if not cleaned_location:
            return {
                'success': False,
                'error': validation_message,
                'suggestions': self._get_suggestions_for_invalid_input(user_input)
            }
        
        # Step 2: Check cache first
        cache_key = cleaned_location.lower()
        if cache_key in self.location_cache:
            cached_result = self.location_cache[cache_key]
            print(f"Using cached result for '{cleaned_location}'")
            return {
                'success': True,
                'location_data': cached_result,
                'source': 'cache'
            }
        
        # Step 3: Geocode the location
        geocode_result = self.geocoder.geocode_location(cleaned_location)
        
        if not geocode_result:
            return {
                'success': False,
                'error': f"Could not find location '{cleaned_location}'",
                'suggestions': self._get_location_suggestions(cleaned_location)
            }
        
        # Step 4: Prepare weather-ready location data
        weather_location = {
            'original_input': user_input,
            'cleaned_input': cleaned_location,
            'display_name': geocode_result['display_name'],
            'latitude': geocode_result['latitude'],
            'longitude': geocode_result['longitude'],
            'type': geocode_result['type']
        }
        
        # Step 5: Cache the result
        self.location_cache[cache_key] = weather_location
        
        return {
            'success': True,
            'location_data': weather_location,
            'source': 'geocoding'
        }
    
    def _get_suggestions_for_invalid_input(self, invalid_input):
        """Provide suggestions for invalid location inputs"""
        suggestions = []
        
        if not invalid_input or len(invalid_input.strip()) < 2:
            suggestions.append("Try entering a city name (e.g., 'New York' or 'London')")
        
        # Check for common typos or issues
        if any(char.isdigit() for char in invalid_input):
            suggestions.append("Remove numbers from location name")
        
        if len(invalid_input) > 50:
            suggestions.append("Try a shorter, more specific location name")
        
        # Add some common location examples
        suggestions.extend([
            "Examples: 'Chicago, IL', 'Paris, France', 'Tokyo, Japan'",
            "Include state or country for better results"
        ])
        
        return suggestions
    
    def _get_location_suggestions(self, location_name):
        """Provide suggestions when location is not found"""
        return [
            f"Check spelling of '{location_name}'",
            "Try including state or country (e.g., 'Springfield, IL')",
            "Use major city names for better results",
            "Try alternative name (e.g., 'NYC' for New York City)"
        ]

# Demonstrate complete location service
print("\nComplete Location Service Demonstration:")
print("=" * 50)

location_service = WeatherLocationService()

# Test various user inputs
test_inputs = [
    "chicago",
    "NYC",
    "London, UK",
    "123Invalid!",
    "",
    "NonexistentCity12345",
    "San Francisco"  # Test caching by requesting twice
]

for user_input in test_inputs:
    print(f"\nProcessing: '{user_input}'")
    result = location_service.process_location_request(user_input)
    
    if result['success']:
        location = result['location_data']
        print(f"✓ Success ({result['source']})")
        print(f"  Display: {location['display_name']}")
        print(f"  Coordinates: ({location['latitude']:.4f}, {location['longitude']:.4f})")
    else:
        print(f"✗ Error: {result['error']}")
        if result.get('suggestions'):
            print("  Suggestions:")
            for suggestion in result['suggestions'][:3]:  # Show first 3 suggestions
                print(f"    • {suggestion}")

# Test caching by requesting San Francisco again
print(f"\nTesting cache - requesting 'San Francisco' again:")
result = location_service.process_location_request("San Francisco")
print(f"Result source: {result.get('source', 'unknown')}")
