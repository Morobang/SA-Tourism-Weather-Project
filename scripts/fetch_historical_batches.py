"""
Batch Historical Data Fetching Script

Fetches ALL available weather data for SA locations and saves as CSV files.
Data APPENDS to existing CSV files (safe to re-run).

Usage:
    python scripts/fetch_historical_batches.py
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

# Data directories - RAW data from API goes to data/raw/historical
data_dir = project_root / "data" / "raw" / "historical"
hourly_dir = data_dir / "hourly"
daily_dir = data_dir / "daily"
hourly_dir.mkdir(parents=True, exist_ok=True)
daily_dir.mkdir(parents=True, exist_ok=True)

# ALL HOURLY VARIABLES from Archive API
HOURLY_VARIABLES = [
    "temperature_2m", "relative_humidity_2m", "dew_point_2m",
    "apparent_temperature", "precipitation", "rain", "snowfall",
    "snow_depth", "weather_code", "pressure_msl", "surface_pressure",
    "cloud_cover", "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high",
    "et0_fao_evapotranspiration", "vapour_pressure_deficit", "wind_gusts_10m",
    "wind_direction_100m", "wind_direction_10m", "wind_speed_100m", "wind_speed_10m",
    "soil_temperature_0_to_7cm", "soil_temperature_7_to_28cm",
    "soil_temperature_28_to_100cm", "soil_temperature_100_to_255cm",
    "soil_moisture_0_to_7cm", "soil_moisture_7_to_28cm",
    "soil_moisture_28_to_100cm", "soil_moisture_100_to_255cm",
    "sunshine_duration", "shortwave_radiation"  # ADDED: Tourism-relevant solar variables
]

# ALL DAILY VARIABLES from Archive API
DAILY_VARIABLES = [
    "weather_code", "temperature_2m_mean", "temperature_2m_max", "temperature_2m_min",
    "apparent_temperature_mean", "apparent_temperature_max", "apparent_temperature_min",
    "sunshine_duration", "daylight_duration", "sunset", "sunrise",
    "precipitation_sum", "rain_sum", "snowfall_sum", "precipitation_hours",
    "et0_fao_evapotranspiration", "shortwave_radiation_sum",
    "wind_direction_10m_dominant", "wind_gusts_10m_max", "wind_speed_10m_max",
    "cloud_cover_mean", "cloud_cover_max", "cloud_cover_min",
    "dew_point_2m_mean", "dew_point_2m_max", "dew_point_2m_min",
    "pressure_msl_min", "pressure_msl_max", "pressure_msl_mean",
    "snowfall_water_equivalent_sum",
    "relative_humidity_2m_min", "relative_humidity_2m_max", "et0_fao_evapotranspiration_sum",
    "relative_humidity_2m_mean", "surface_pressure_mean", "surface_pressure_max", "surface_pressure_min",
    "winddirection_10m_dominant", "wind_gusts_10m_mean", "wind_speed_10m_mean",
    "wind_gusts_10m_min", "wind_speed_10m_min",
    "wet_bulb_temperature_2m_mean", "wet_bulb_temperature_2m_max", "wet_bulb_temperature_2m_min",
    "vapour_pressure_deficit_max",
    "soil_moisture_0_to_100cm_mean", "soil_moisture_0_to_7cm_mean",
    "soil_moisture_28_to_100cm_mean", "soil_moisture_7_to_28cm_mean",
    "soil_temperature_0_to_100cm_mean", "soil_temperature_0_to_7cm_mean",
    "soil_temperature_28_to_100cm_mean", "soil_temperature_7_to_28cm_mean"
]

# Setup Open-Meteo API client with cache and retry
cache_session = requests_cache.CachedSession(str(project_root / '.cache'), expire_after=-1)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

# ============================================================================
# FETCH FUNCTIONS
# ============================================================================

def fetch_location(location_code, start_date, end_date):
    """
    Fetch weather data for one location and save to CSV.
    Just change the location_code or dates to fetch different data!
    
    Args:
        location_code: e.g. 'cape_town', 'johannesburg'
        start_date: "YYYY-MM-DD"
        end_date: "YYYY-MM-DD"
    """
    location = LOCATIONS[location_code]
    print(f"\n📍 Fetching {location['name']} ({start_date} to {end_date})...")
    
    try:
        # API request
        url = "https://archive-api.open-meteo.com/v1/archive"
        params = {
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "start_date": start_date,
            "end_date": end_date,
            "hourly": HOURLY_VARIABLES,
            "daily": DAILY_VARIABLES,
            "timezone": "auto"
        }
        
        responses = openmeteo.weather_api(url, params=params)
        response = responses[0]
        
        print(f"   Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
        print(f"   Elevation: {response.Elevation()} m")
        
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
        
        # Save hourly (append if exists)
        hourly_csv = hourly_dir / f"{location_code}_hourly.csv"
        if hourly_csv.exists():
            hourly_df.to_csv(hourly_csv, mode='a', header=False, index=False)
            print(f"   ✅ Appended {len(hourly_df)} hourly records")
        else:
            hourly_df.to_csv(hourly_csv, index=False)
            print(f"   ✅ Created {hourly_csv.name} with {len(hourly_df)} hourly records")
        
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
        
        # Save daily (append if exists)
        daily_csv = daily_dir / f"{location_code}_daily.csv"
        if daily_csv.exists():
            daily_df.to_csv(daily_csv, mode='a', header=False, index=False)
            print(f"   ✅ Appended {len(daily_df)} daily records")
        else:
            daily_df.to_csv(daily_csv, index=False)
            print(f"   ✅ Created {daily_csv.name} with {len(daily_df)} daily records")
        
        return True
    
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        return False


def fetch_batch(start_date, end_date, batch_name):
    """Loop through all 15 locations and fetch data."""
    print("\n" + "="*70)
    print(f"🚀 BATCH: {batch_name}")
    print(f"   Dates: {start_date} to {end_date}")
    print(f"   Locations: {len(LOCATIONS)}")
    print(f"   Started: {datetime.now().strftime('%H:%M:%S')}")
    print("="*70)
    
    success = 0
    failed = []

    #for i, location_code in enumerate(['franschhoek', 'knysna', 'hermanus'], 1):
    for i, location_code in enumerate(LOCATIONS.keys(), 1):
        print(f"\n[{i}/{len(LOCATIONS)}]", end=" ")
        
        if fetch_location(location_code, start_date, end_date):
            success += 1
        else:
            failed.append(location_code)
        
        # Wait 2 seconds between locations
        if i < len(LOCATIONS):
            time.sleep(2)
    
    # Summary
    print("\n" + "="*70)
    print(f"✅ DONE: {success}/{len(LOCATIONS)} successful")
    if failed:
        print(f"   ⚠️  Failed: {', '.join(failed)}")
    print("="*70 + "\n")
    
    return success, failed


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main entry point for batch fetching."""
    
    print("\n" + "🌍 SA TOURISM WEATHER PROJECT - HISTORICAL DATA COLLECTION")
    print("="*70)
    print("This script will fetch weather data for 15 SA locations")
    print("Data will be APPENDED to CSV files (safe to re-run)")
    print("="*70)
    
    # Ask user which batch to run
    print("\nSelect batch to fetch:")
    print("  1. Batch 1: 2020-2021 (~3,900 calls)")
    print("  2. Batch 2: 2022-2023 (~3,900 calls)")
    print("  3. Batch 3: 2024 YTD (~1,950 calls)")
    print("  4. ALL BATCHES in one go (~9,750 calls)")
    print("  5. Custom date range")
    print("  0. Exit")
    
    choice = input("\nEnter choice (0-5): ").strip()
    
    if choice == "0":
        print("👋 Goodbye!")
        return
    
    start_time = datetime.now()
    
    try:
        if choice == "1":
            fetch_batch("2020-01-01", "2021-12-31", "2020-2021")
        
        elif choice == "2":
            fetch_batch("2022-01-01", "2023-12-31", "2022-2023")
        
        elif choice == "3":
            fetch_batch("2024-01-01", "2024-11-14", "2024")
        
        elif choice == "4":
            print("\n🚀 Running ALL batches sequentially...")
            print("This will take approximately 30-45 minutes.\n")
            
            confirm = input("Continue? (yes/no): ").strip().lower()
            if confirm != "yes":
                print("❌ Cancelled.")
                return
            
            # Batch 1
            fetch_batch("2020-01-01", "2021-12-31", "2020-2021")
            print("\n⏸️  5-minute break before next batch...")
            time.sleep(300)
            
            # Batch 2
            fetch_batch("2022-01-01", "2023-12-31", "2022-2023")
            print("\n⏸️  5-minute break before next batch...")
            time.sleep(300)
            
            # Batch 3
            fetch_batch("2024-01-01", "2024-11-14", "2024")
        
        elif choice == "5":
            start_date = input("Start date (YYYY-MM-DD): ").strip()
            end_date = input("End date (YYYY-MM-DD): ").strip()
            batch_name = f"{start_date}_to_{end_date}"
            fetch_batch(start_date, end_date, batch_name)
        
        else:
            print("❌ Invalid choice. Exiting.")
            return
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user. Exiting gracefully...")
        print("Note: Partially fetched data is already saved to CSV files.")
        return
    
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return
    
    elapsed = datetime.now() - start_time
    hours = int(elapsed.total_seconds() // 3600)
    minutes = int((elapsed.total_seconds() % 3600) // 60)
    seconds = int(elapsed.total_seconds() % 60)
    
    print("\n" + "="*70)
    print(f"✅ ALL DONE!")
    print(f"   Total time: {hours}h {minutes}m {seconds}s")
    print(f"   Hourly data: {hourly_dir}")
    print(f"   Daily data: {daily_dir}")
    print("="*70)


if __name__ == "__main__":
    main()
