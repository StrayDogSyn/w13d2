def demonstrate_weather_integration():
    """Demonstrate how location services integrate with weather APIs"""
    
    location_manager = WeatherLocationManager()
    
    def get_weather_for_location(location_input=None):
        """Simulate getting weather using the location manager"""
        
        # Get location data
        location_result = location_manager.get_location_for_weather(location_input)
        
        if not location_result['success']:
            print(f"✗ Location error: {location_result['error']}")
            return None
        
        location_data = location_result['location_data']
        
        # Simulate weather API call using coordinates
        print(f"🌤  Getting weather for {location_data['name']}...")
        print(f"   Coordinates: ({location_data['latitude']:.4f}, {location_data['longitude']:.4f})")
        
        # This is where you would make the actual weather API call
        simulated_weather = {
            'location': location_data['name'],
            'temperature': 72,
            'condition': 'Partly Cloudy',
            'humidity': 65,
            'coordinates': f"({location_data['latitude']:.4f}, {location_data['longitude']:.4f})"
        }
        
        print(f"   Temperature: {simulated_weather['temperature']}°F")
        print(f"   Condition: {simulated_weather['condition']}")
        print(f"   Humidity: {simulated_weather['humidity']}%")
        
        return simulated_weather
    
    print("\nWeather Integration Demonstration:")
    print("=" * 40)
    
    # Test weather for different location inputs
    test_locations = [
        None,  # Default location
        "Paris, France",
        "Sydney, Australia"
    ]
    
    for location in test_locations:
        if location is None:
            print(f"\nGetting weather for default location:")
        else:
            print(f"\nGetting weather for '{location}':")
        
        weather = get_weather_for_location(location)
        if weather:
            print("✓ Weather retrieved successfully")
        print("-" * 30)

# Run the weather integration demonstration
demonstrate_weather_integration()

