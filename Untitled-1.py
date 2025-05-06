import pandas as pd
import time
from geopy.geocoders import Nominatim

# Load addresses
df = pd.read_csv("addresses.csv")
df['full_address'] = df.apply(lambda row: f"{row['address']}, {row['city']}, {row['country']}", axis=1)

# Set up Nominatim geocoder
geolocator = Nominatim(user_agent="your_unique_app_name")

# Placeholder for results
cities = []
countries = []
postal_codes = []
latitudes = []
longitudes = []

for address in df['full_address']:
    try:
        print(f"Looking up: {address}")
        location = geolocator.geocode(address)
        if location:
            # Reverse geocode to get detailed address parts
            detailed = geolocator.reverse((location.latitude, location.longitude), language='en', addressdetails=True)
            addr = detailed.raw.get('address', {})
            # Extract data from the detailed address
            city = addr.get('city') or addr.get('town') or addr.get('village') or addr.get('hamlet')
            country = addr.get('country')
            postal_code = addr.get('postcode')
            latitude = location.latitude
            longitude = location.longitude
        else:
            city = country = postal_code = latitude = longitude = None
    except Exception as e:
        print(f"Error for {address}: {e}")
        city = country = postal_code = latitude = longitude = None

    cities.append(city)
    countries.append(country)
    postal_codes.append(postal_code)
    latitudes.append(latitude)
    longitudes.append(longitude)

    # Respect Nominatim's 1 request/second policy
    time.sleep(1)

# Add columns to DataFrame
df['city'] = cities
df['country'] = countries
df['postal_code'] = postal_codes
df['latitude'] = latitudes
df['longitude'] = longitudes

# Save results to a new CSV
df.to_csv("addresses_with_geography_data.csv", index=False)
print("Saved to addresses_with_geography_data.csv")
