import time
from geopy.geocoders import Nominatim


# Initialize the geolocator once
geolocator = Nominatim(user_agent="app_to_get_postal_codes_and_coordinates_obs_v1")

def get_postal_code(full_address):
    try:
        print(f"Looking up: {full_address}")
        location = geolocator.geocode(full_address)

        if location:
            # Reverse geocode for detailed info
            detailed = geolocator.reverse((location.latitude, location.longitude), language='en', addressdetails=True)
            addr = detailed.raw.get('address', {})

            city = addr.get('city') or addr.get('town') or addr.get('village') or addr.get('hamlet')
            country = addr.get('country')
            postal_code = addr.get('postcode')
            latitude = location.latitude
            longitude = location.longitude
        else:
            city = country = postal_code = latitude = longitude = None

    except Exception as e:
        print(f"Error: {e}")
        city = country = postal_code = latitude = longitude = None

    # Optional: delay to respect rate limit
    time.sleep(1)

    return {
        'city': city,
        'country': country,
        'postal_code': postal_code,
        'latitude': latitude,
        'longitude': longitude
    }