## Implementing Location Autocomplete:
class LocationAutocomplete:
    """Provides autocomplete suggestions for location searches"""
    
    def __init__(self):
        self.base_url = "https://nominatim.openstreetmap.org/search"
        self.headers = {
            'User-Agent': 'WeatherApp/1.0 (Educational Project)'
        }
        
        # Cache for autocomplete results
        self.autocomplete_cache = {}
        
        # Common locations to prioritize in suggestions
        self.popular_locations = [
            "New York, NY", "Los Angeles, CA", "Chicago, IL", 
            "Houston, TX", "Phoenix, AZ", "Philadelphia, PA",
            "London, UK", "Paris, France", "Tokyo, Japan",
            "Berlin, Germany", "Sydney, Australia", "Toronto, Canada"
        ]
    
    def get_location_suggestions(self, partial_input, max_suggestions=5):
        """
        Get location suggestions based on partial user input
        
        Args:
            partial_input: What the user has typed so far
            max_suggestions: Maximum number of suggestions to return
            
        Returns:
            List of location suggestions with relevant data
        """
        if not partial_input or len(partial_input.strip()) < 2:
            # For very short input, return popular locations
            return self._get_popular_location_suggestions(partial_input, max_suggestions)
        
        cleaned_input = partial_input.strip().lower()
        
        # Check cache first
        cache_key = f"{cleaned_input}_{max_suggestions}"
        if cache_key in self.autocomplete_cache:
            return self.autocomplete_cache[cache_key]
        
        try:
            # API request for autocomplete
            params = {
                'q': partial_input,
                'format': 'json',
                'limit': max_suggestions * 2,  # Get more results to filter
                'addressdetails': 1,
                'extratags': 1
            }
            
            response = requests.get(
                self.base_url, 
                params=params, 
                headers=self.headers,
                timeout=5  # Shorter timeout for autocomplete
            )
            
            if response.status_code == 200:
                results = response.json()
                suggestions = self._process_autocomplete_results(results, max_suggestions)
                
                # Cache the results
                self.autocomplete_cache[cache_key] = suggestions
                
                return suggestions
            else:
                print(f"Autocomplete API error: {response.status_code}")
                return self._get_fallback_suggestions(partial_input, max_suggestions)
                
        except requests.exceptions.RequestException as e:
            print(f"Autocomplete network error: {e}")
            return self._get_fallback_suggestions(partial_input, max_suggestions)
        except Exception as e:
            print(f"Autocomplete error: {e}")
            return []
    
    def _process_autocomplete_results(self, api_results, max_suggestions):
        """Process and rank autocomplete results"""
        suggestions = []
        
        for result in api_results:
            # Filter for appropriate location types
            location_type = result.get('type', '')
            class_type = result.get('class', '')
            
            # Prioritize cities, towns, and administrative areas
            if location_type in ['city', 'town', 'village', 'hamlet'] or \
               class_type in ['place', 'boundary']:
                
                suggestion = {
                    'display_name': result['display_name'],
                    'short_name': self._create_short_name(result),
                    'latitude': float(result['lat']),
                    'longitude': float(result['lon']),
                    'type': location_type,
                    'importance': float(result.get('importance', 0)),
                    'country': result.get('address', {}).get('country', ''),
                    'state': result.get('address', {}).get('state', '')
                }
                
                suggestions.append(suggestion)
        
        # Sort by importance (higher is better)
        suggestions.sort(key=lambda x: x['importance'], reverse=True)
        
        # Remove duplicates and limit results
        unique_suggestions = []
        seen_names = set()
        
        for suggestion in suggestions:
            short_name = suggestion['short_name']
            if short_name not in seen_names:
                unique_suggestions.append(suggestion)
                seen_names.add(short_name)
                
                if len(unique_suggestions) >= max_suggestions:
                    break
        
        return unique_suggestions
    
    def _create_short_name(self, result):
        """Create a short, user-friendly name for display"""
        address = result.get('address', {})
        
        # Try to build: "City, State, Country" format
        components = []
        
        # Add city/town name
        for key in ['city', 'town', 'village', 'hamlet']:
            if key in address:
                components.append(address[key])
                break
        
        # Add state/province if available
        if 'state' in address:
            components.append(address['state'])
        
        # Add country
        if 'country' in address:
            components.append(address['country'])
        
        if components:
            return ', '.join(components)
        else:
            # Fallback to display name, shortened
            display_name = result['display_name']
            parts = display_name.split(',')
            return ', '.join(parts[:3])  # Take first 3 parts
    
    def _get_popular_location_suggestions(self, partial_input, max_suggestions):
        """Return popular locations when input is too short"""
        if not partial_input:
            return [{'short_name': loc, 'display_name': loc, 'type': 'popular'} 
                   for loc in self.popular_locations[:max_suggestions]]
        
        # Filter popular locations that match the partial input
        partial_lower = partial_input.lower()
        matching = [loc for loc in self.popular_locations 
                   if partial_lower in loc.lower()]
        
        return [{'short_name': loc, 'display_name': loc, 'type': 'popular'} 
               for loc in matching[:max_suggestions]]
    
    def _get_fallback_suggestions(self, partial_input, max_suggestions):
        """Provide fallback suggestions when API is unavailable"""
        return [
            {'short_name': f"{partial_input.title()}, USA", 'display_name': f"{partial_input.title()}, United States", 'type': 'fallback'},
            {'short_name': f"{partial_input.title()}, UK", 'display_name': f"{partial_input.title()}, United Kingdom", 'type': 'fallback'},
            {'short_name': f"{partial_input.title()}, Canada", 'display_name': f"{partial_input.title()}, Canada", 'type': 'fallback'}
        ][:max_suggestions]

# Demonstrate autocomplete functionality
print("\nLocation Autocomplete Demonstration:")
print("=" * 45)

autocomplete = LocationAutocomplete()

# Test autocomplete with various inputs
test_inputs = [
    "New",
    "San",
    "Lond",
    "Chi",
    "Par",
    "To"
]

for test_input in test_inputs:
    print(f"\nAutocomplete for '{test_input}':")
    suggestions = autocomplete.get_location_suggestions(test_input, max_suggestions=3)
    
    for i, suggestion in enumerate(suggestions, 1):
        print(f"  {i}. {suggestion['short_name']} ({suggestion['type']})")
        if 'latitude' in suggestion:
            print(f"     Coordinates: ({suggestion['latitude']:.2f}, {suggestion['longitude']:.2f})")

