
class InteractiveLocationSearch:
    """Interactive location search with advanced features"""
    
    def __init__(self):
        self.autocomplete = LocationAutocomplete()
        self.location_service = WeatherLocationService()
        self.search_history = []
        self.favorites = []
    
    def interactive_location_search(self):
        """Run an interactive location search session"""
        print("\n" + "="*50)
        print("INTERACTIVE WEATHER LOCATION SEARCH")
        print("="*50)
        print("Type a location name to get suggestions.")
        print("Commands: 'history', 'favorites', 'clear', 'quit'")
        print("-"*50)
        
        while True:
            try:
                user_input = input("\nEnter location (or command): ").strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() == 'quit':
                    print("Goodbye!")
                    break
                elif user_input.lower() == 'history':
                    self._show_search_history()
                    continue
                elif user_input.lower() == 'favorites':
                    self._show_favorites()
                    continue
                elif user_input.lower() == 'clear':
                    self.search_history.clear()
                    print("Search history cleared.")
                    continue
                
                # Get autocomplete suggestions
                suggestions = self.autocomplete.get_location_suggestions(user_input, max_suggestions=5)
                
                if not suggestions:
                    print(f"No suggestions found for '{user_input}'")
                    continue
                
                # Display suggestions
                print(f"\nSuggestions for '{user_input}':")
                for i, suggestion in enumerate(suggestions, 1):
                    print(f"  {i}. {suggestion['short_name']}")
                
                # Let user select a suggestion
                try:
                    choice = input("\nSelect option (1-5) or press Enter for more typing: ").strip()
                    
                    if choice.isdigit():
                        choice_num = int(choice)
                        if 1 <= choice_num <= len(suggestions):
                            selected = suggestions[choice_num - 1]
                            self._process_selected_location(selected)
                        else:
                            print("Invalid selection.")
                    
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    
            except KeyboardInterrupt:
                print("\nSearch interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"Error during search: {e}")
    
    def _process_selected_location(self, selected_location):
        """Process a user's selected location"""
        print(f"\nSelected: {selected_location['short_name']}")
        
        # Add to search history
        if selected_location['short_name'] not in [item['name'] for item in self.search_history]:
            self.search_history.append({
                'name': selected_location['short_name'],
                'full_name': selected_location['display_name'],
                'timestamp': f"Selected at {self._get_current_time()}"
            })
        
        # Show location details
        if 'latitude' in selected_location:
            print(f"Coordinates: ({selected_location['latitude']:.4f}, {selected_location['longitude']:.4f})")
            print(f"Type: {selected_location['type']}")
            
            # Ask if user wants to add to favorites
            add_favorite = input("Add to favorites? (y/n): ").strip().lower()
            if add_favorite == 'y':
                self._add_to_favorites(selected_location)
            
            # Simulate getting weather for this location
            print(f"🌤  Getting weather for {selected_location['short_name']}...")
            print("    (Weather data would be fetched here using coordinates)")
        
        print("-" * 40)
    
    def _add_to_favorites(self, location):
        """Add location to favorites list"""
        favorite_name = location['short_name']
        
        # Check if already in favorites
        if favorite_name not in [fav['name'] for fav in self.favorites]:
            self.favorites.append({
                'name': favorite_name,
                'full_name': location.get('display_name', favorite_name),
                'latitude': location.get('latitude'),
                'longitude': location.get('longitude'),
                'added_at': self._get_current_time()
            })
            print(f"✓ Added '{favorite_name}' to favorites!")
        else:
            print(f"'{favorite_name}' is already in favorites.")
    
    def _show_search_history(self):
        """Display search history"""
        if not self.search_history:
            print("No search history yet.")
            return
        
        print("\nSearch History:")
        for i, item in enumerate(self.search_history[-10:], 1):  # Show last 10
            print(f"  {i}. {item['name']} - {item['timestamp']}")
    
    def _show_favorites(self):
        """Display favorites list"""
        if not self.favorites:
            print("No favorites yet.")
            return
        
        print("\nFavorite Locations:")
        for i, fav in enumerate(self.favorites, 1):
            coords = ""
            if fav.get('latitude') and fav.get('longitude'):
                coords = f" ({fav['latitude']:.2f}, {fav['longitude']:.2f})"
            print(f"  {i}. {fav['name']}{coords} - Added {fav['added_at']}")
    
    def _get_current_time(self):
        """Get current time as string"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M")

# Create a simple demonstration function
def demonstrate_location_search():
    """Demonstrate the location search functionality without full interactivity"""
    search = InteractiveLocationSearch()
    
    print("Location Search Demonstration")
    print("=" * 40)
    
    # Simulate some searches
    test_searches = ["New York", "London", "Tokyo"]
    
    for search_term in test_searches:
        print(f"\nSearching for: '{search_term}'")
        suggestions = search.autocomplete.get_location_suggestions(search_term, max_suggestions=3)
        
        print("Suggestions:")
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion['short_name']}")
        
        # Simulate selecting the first suggestion
        if suggestions:
            print(f"Simulating selection of: {suggestions[0]['short_name']}")
            search._process_selected_location(suggestions[0])

# Run the demonstration
demonstrate_location_search()

print("\nTo run full interactive search, call: search.interactive_location_search()")
