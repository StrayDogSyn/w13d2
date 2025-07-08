
## `01_basic.py`: Basic Weather Chart with Matplotlib

### Key Teaching Points:

* **Importing essential libraries**: `matplotlib.pyplot`, `pandas`, `datetime`, and `random` for data visualization and simulation.
* **Function usage**: `create_sample_weather_data()` demonstrates modular coding and function returns.
* **List usage**: Demonstrates how to build and append to multiple parallel lists (dates, temperature, etc.).
* **`datetime` manipulation**: Shows how to generate a sequence of dates with `timedelta`.
* **Random number generation**: Teaches `random.randint()` and `random.uniform()` for simulating realistic weather data.
* **Matplotlib basics**: `plt.plot()`, labels, titles, grid, `xticks` rotation, and `tight_layout()` for clean layout.
* **Displaying plots**: `plt.show()` is critical for viewing output.

---

## `02_imp_geo_svc.py`: Implementing Geocoding Services

### Key Teaching Points:

* **Class-based design**: `SimpleGeocoder` encapsulates geocoding logic cleanly.
* **API usage**: How to construct a URL and send an HTTP GET request with `requests.get()`.
* **Handling HTTP response**: Using `.json()` and status code checking (`response.status_code`).
* **Error handling**: Robust `try`/`except` structure to catch network and parsing errors.
* **Reverse geocoding**: Teaching the concept of going from coordinates → human-readable locations.
* **User-Agent headers**: Importance of setting headers (required by Nominatim) in real-world APIs.
* **Real-world data validation**: Shows how to test inputs (e.g., valid cities vs. nonsense inputs).

---

## `03_complete_loc_svc.py`: Complete Location Service

### Key Teaching Points:

* **Compositional design**: Introduces integration of components: validator, geocoder, cache.
* **Cache implementation**: Teaches how to store and reuse previous API results using dictionaries.
* **Input validation**: Shows how to clean inputs and return user-friendly error messages.
* **User-centric feedback**: Adding suggestions and helpful responses when inputs fail validation or geocoding.
* **Testing flow**: Structured demonstration of functionality with multiple test inputs, including edge cases.
* **Separation of concerns**: Highlights how each method focuses on a specific responsibility (`process_location_request`, `_get_suggestions_for_invalid_input`, etc.).

