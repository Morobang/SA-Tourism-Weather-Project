"""
Forecast Data Fetching Script

Fetches ALL available forecast weather data for SA locations and saves as CSV files.
Forecast API provides: current conditions + 16 days forecast

Usage:
    python scripts/fetch_forecast.py
"""

import sys
from pathlib import Path
from datetime import datetime
import time
import pandas as pd
import openmeteo_requests
import requests_cache
from retry_requests import retry

# ============================================================================
# SETUP
# ============================================================================

# Project paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

# Import locations from config
from config import LOCATIONS

# Data directories - Forecast data goes to data/raw/forecast
data_dir = project_root / "data" / "raw" / "forecast"
current_dir = data_dir / "current"
hourly_dir = data_dir / "hourly"
daily_dir = data_dir / "daily"
current_dir.mkdir(parents=True, exist_ok=True)
hourly_dir.mkdir(parents=True, exist_ok=True)
daily_dir.mkdir(parents=True, exist_ok=True)

# ALL CURRENT VARIABLES from Forecast API
CURRENT_VARIABLES = [
    "temperature_2m", "relative_humidity_2m", "apparent_temperature", "is_day",
    "precipitation", "rain", "showers", "snowfall", "weather_code",
    "cloud_cover", "pressure_msl", "surface_pressure", "wind_speed_10m",
    "wind_direction_10m", "wind_gusts_10m"
]

# ALL HOURLY VARIABLES from Forecast API (ALL 156 variables!)
HOURLY_VARIABLES = [
    "temperature_2m", "relative_humidity_2m", "dew_point_2m", "apparent_temperature",
    "precipitation_probability", "precipitation", "rain", "showers", "snowfall",
    "snow_depth", "weather_code", "pressure_msl", "surface_pressure", "cloud_cover",
    "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", "visibility",
    "evapotranspiration", "et0_fao_evapotranspiration", "vapour_pressure_deficit",
    "wind_speed_10m", "wind_speed_80m", "wind_speed_120m", "wind_speed_180m",
    "wind_direction_10m", "wind_direction_80m", "wind_direction_120m", "wind_direction_180m",
    "wind_gusts_10m", "temperature_80m", "temperature_120m", "temperature_180m",
    "soil_moisture_0_to_1cm", "soil_moisture_1_to_3cm", "soil_moisture_3_to_9cm",
    "soil_moisture_9_to_27cm", "soil_moisture_27_to_81cm",
    "soil_temperature_0cm", "soil_temperature_6cm", "soil_temperature_18cm", "soil_temperature_54cm",
    "temperature_1000hPa", "temperature_975hPa", "temperature_950hPa", "temperature_925hPa",
    "temperature_900hPa", "temperature_850hPa", "temperature_800hPa", "temperature_700hPa",
    "temperature_600hPa", "temperature_500hPa", "temperature_400hPa", "temperature_300hPa",
    "temperature_250hPa", "temperature_200hPa", "temperature_150hPa", "temperature_100hPa",
    "temperature_70hPa", "temperature_50hPa", "temperature_30hPa",
    "relative_humidity_1000hPa", "relative_humidity_975hPa", "relative_humidity_950hPa",
    "relative_humidity_925hPa", "relative_humidity_900hPa", "relative_humidity_850hPa",
    "relative_humidity_800hPa", "relative_humidity_700hPa", "relative_humidity_600hPa",
    "relative_humidity_500hPa", "relative_humidity_400hPa", "relative_humidity_300hPa",
    "relative_humidity_250hPa", "relative_humidity_200hPa", "relative_humidity_150hPa",
    "relative_humidity_100hPa", "relative_humidity_70hPa", "relative_humidity_50hPa",
    "relative_humidity_30hPa",
    "cloud_cover_1000hPa", "cloud_cover_975hPa", "cloud_cover_950hPa", "cloud_cover_925hPa",
    "cloud_cover_900hPa", "cloud_cover_850hPa", "cloud_cover_800hPa", "cloud_cover_700hPa",
    "cloud_cover_600hPa", "cloud_cover_500hPa", "cloud_cover_400hPa", "cloud_cover_300hPa",
    "cloud_cover_250hPa", "cloud_cover_200hPa", "cloud_cover_150hPa", "cloud_cover_100hPa",
    "cloud_cover_70hPa", "cloud_cover_50hPa", "cloud_cover_30hPa",
    "wind_speed_1000hPa", "wind_speed_975hPa", "wind_speed_950hPa", "wind_speed_925hPa",
    "wind_speed_900hPa", "wind_speed_850hPa", "wind_speed_800hPa", "wind_speed_700hPa",
    "wind_speed_600hPa", "wind_speed_500hPa", "wind_speed_400hPa", "wind_speed_300hPa",
    "wind_speed_250hPa", "wind_speed_200hPa", "wind_speed_150hPa", "wind_speed_100hPa",
    "wind_speed_70hPa", "wind_speed_50hPa", "wind_speed_30hPa",
    "wind_direction_1000hPa", "wind_direction_975hPa", "wind_direction_950hPa",
    "wind_direction_925hPa", "wind_direction_900hPa", "wind_direction_850hPa",
    "wind_direction_800hPa", "wind_direction_700hPa", "wind_direction_600hPa",
    "wind_direction_500hPa", "wind_direction_400hPa", "wind_direction_300hPa",
    "wind_direction_250hPa", "wind_direction_200hPa", "wind_direction_150hPa",
    "wind_direction_100hPa", "wind_direction_70hPa", "wind_direction_50hPa",
    "wind_direction_30hPa",
    "geopotential_height_1000hPa", "geopotential_height_975hPa", "geopotential_height_950hPa",
    "geopotential_height_925hPa", "geopotential_height_900hPa", "geopotential_height_850hPa",
    "geopotential_height_800hPa", "geopotential_height_700hPa", "geopotential_height_600hPa",
    "geopotential_height_500hPa", "geopotential_height_400hPa", "geopotential_height_300hPa",
    "geopotential_height_250hPa", "geopotential_height_200hPa", "geopotential_height_150hPa",
    "geopotential_height_100hPa", "geopotential_height_70hPa", "geopotential_height_50hPa",
    "geopotential_height_30hPa"
]

# ALL DAILY VARIABLES from Forecast API (61 variables!)
DAILY_VARIABLES = [
    "weather_code", "temperature_2m_max", "temperature_2m_min", "apparent_temperature_max",
    "apparent_temperature_min", "sunrise", "sunset", "daylight_duration", "sunshine_duration",
    "uv_index_max", "uv_index_clear_sky_max", "rain_sum", "showers_sum", "snowfall_sum",
    "precipitation_sum", "precipitation_hours", "precipitation_probability_max",
    "wind_speed_10m_max", "wind_gusts_10m_max", "wind_direction_10m_dominant",
    "shortwave_radiation_sum", "et0_fao_evapotranspiration", "temperature_2m_mean",
    "apparent_temperature_mean", "cape_mean", "cape_max", "cape_min", "cloud_cover_mean",
    "cloud_cover_max", "cloud_cover_min", "dew_point_2m_mean", "dew_point_2m_max",
    "dew_point_2m_min", "pressure_msl_min", "pressure_msl_max", "pressure_msl_mean",
    "snowfall_water_equivalent_sum", "relative_humidity_2m_min", "relative_humidity_2m_max",
    "relative_humidity_2m_mean", "precipitation_probability_min", "precipitation_probability_mean",
    "leaf_wetness_probability_mean", "growing_degree_days_base_0_limit_50",
    "et0_fao_evapotranspiration_sum", "surface_pressure_mean", "surface_pressure_max",
    "surface_pressure_min", "updraft_max", "visibility_mean", "visibility_min", "visibility_max",
    "winddirection_10m_dominant", "wind_gusts_10m_mean", "wind_speed_10m_mean",
    "wind_gusts_10m_min", "wind_speed_10m_min", "wet_bulb_temperature_2m_mean",
    "wet_bulb_temperature_2m_max", "wet_bulb_temperature_2m_min", "vapour_pressure_deficit_max"
]

# Setup Open-Meteo API client with cache and retry
cache_session = requests_cache.CachedSession(str(project_root / '.cache'), expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# ============================================================================
# FETCH FUNCTIONS
# ============================================================================

def fetch_forecast(location_code):
    """
    Fetch forecast data for one location and save to CSV.
    
    Args:
        location_code: e.g. 'cape_town', 'johannesburg'
    """
    location = LOCATIONS[location_code]
    print(f"\n📍 Fetching forecast for {location['name']}...")
    
    try:
        # API request - Forecast API (16 days ahead)
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "current": CURRENT_VARIABLES,
            "hourly": HOURLY_VARIABLES,
            "daily": DAILY_VARIABLES,
            "timezone": "auto",
            "start_date": "2025-08-16",
            "end_date": "2025-11-30"
        }
        
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]
        
        print(f"   Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
        print(f"   Elevation: {response.Elevation()} m")
        
        # ===== CURRENT DATA =====
        current = response.Current()
        current_data = {
            "timestamp": [pd.to_datetime(current.Time(), unit="s", utc=True)],
            "location_code": [location_code],
            "location_name": [location["name"]]
        }
        
        # Add all current variables
        for i, var in enumerate(CURRENT_VARIABLES):
            current_data[var] = [current.Variables(i).Value()]
        
        current_df = pd.DataFrame(data=current_data)
        
        # Save current (REPLACE - always get latest)
        current_csv = current_dir / f"{location_code}_current.csv"
        current_df.to_csv(current_csv, index=False)
        print(f"   ✅ Saved current conditions to {current_csv.name}")
        
        # ===== HOURLY DATA =====
        hourly = response.Hourly()
        hourly_data = {
            "date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            ),
            "location_code": location_code,
            "location_name": location["name"]
        }
        
        # Add all hourly variables
        for i, var in enumerate(HOURLY_VARIABLES):
            hourly_data[var] = hourly.Variables(i).ValuesAsNumpy()
        
        hourly_df = pd.DataFrame(data=hourly_data)
        
        # Save hourly (REPLACE - forecast changes)
        hourly_csv = hourly_dir / f"{location_code}_hourly.csv"
        hourly_df.to_csv(hourly_csv, index=False)
        print(f"   ✅ Saved {len(hourly_df)} hourly forecast records to {hourly_csv.name}")
        
        # ===== DAILY DATA =====
        daily = response.Daily()
        daily_data = {
            "date": pd.date_range(
                start=pd.to_datetime(daily.Time(), unit="s", utc=True),
                end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=daily.Interval()),
                inclusive="left"
            ),
            "location_code": location_code,
            "location_name": location["name"]
        }
        
        # Add all daily variables
        for i, var in enumerate(DAILY_VARIABLES):
            if var in ["sunset", "sunrise"]:
                daily_data[var] = daily.Variables(i).ValuesInt64AsNumpy()
            else:
                daily_data[var] = daily.Variables(i).ValuesAsNumpy()
        
        daily_df = pd.DataFrame(data=daily_data)
        
        # Save daily (REPLACE - forecast changes)
        daily_csv = daily_dir / f"{location_code}_daily.csv"
        daily_df.to_csv(daily_csv, index=False)
        print(f"   ✅ Saved {len(daily_df)} daily forecast records to {daily_csv.name}")
        
        return True
    
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False


def fetch_all_forecasts():
    """Fetch forecasts for all 15 locations."""
    print("\n" + "="*70)
    print("🌍 SA TOURISM WEATHER PROJECT - FORECAST DATA COLLECTION")
    print("="*70)
    print(f"Fetching forecasts for {len(LOCATIONS)} locations")
    print(f"Started: {datetime.now().strftime('%H:%M:%S')}")
    print("="*70)
    
    success = 0
    failed = []
    
    for i, location_code in enumerate(LOCATIONS.keys(), 1):
        print(f"\n[{i}/{len(LOCATIONS)}]", end=" ")
        
        if fetch_forecast(location_code):
            success += 1
        else:
            failed.append(location_code)
        
        # Wait 1 second between locations (be nice to API)
        if i < len(LOCATIONS):
            time.sleep(1)
    
    # Summary
    print("\n" + "="*70)
    print(f"✅ DONE: {success}/{len(LOCATIONS)} successful")
    if failed:
        print(f"   ⚠️  Failed: {', '.join(failed)}")
    print(f"   Current data: {current_dir}")
    print(f"   Hourly forecasts: {hourly_dir}")
    print(f"   Daily forecasts: {daily_dir}")
    print("="*70 + "\n")
    
    return success, failed


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main entry point for forecast fetching."""
    
    try:
        fetch_all_forecasts()
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user. Exiting gracefully...")
        return
    
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return


if __name__ == "__main__":
    main()
