"""
API Client for Open-Meteo Weather API.
Handles fetching historical, forecast, and current weather data.
"""

import requests
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, List

from .config import (
    API_BASE_URL,
    API_TIMEOUT,
    API_RETRY_COUNT,
    API_RETRY_DELAY,
    LOCATIONS,
    HOURLY_VARIABLES,
    DAILY_VARIABLES,
    TEMPERATURE_UNIT,
    WIND_SPEED_UNIT,
    PRECIPITATION_UNIT,
    TIMEZONE,
    RAW_HISTORICAL_DIR,
    RAW_FORECAST_DIR,
    RAW_CURRENT_DIR,
)


class OpenMeteoClient:
    """Client for interacting with Open-Meteo API."""
    
    def __init__(self):
        self.base_url = API_BASE_URL
        self.timeout = API_TIMEOUT
        self.retry_count = API_RETRY_COUNT
        self.retry_delay = API_RETRY_DELAY
        
        # Rate limit tracking
        self.call_count = 0
        self.session_start_time = datetime.now()
        self.last_call_time = None
    
    def _check_rate_limits(self):
        """
        Check if we're approaching rate limits and add delays if needed.
        
        Free tier limits:
        - 10,000 calls per day
        - 5,000 calls per hour
        - 600 calls per minute
        """
        now = datetime.now()
        
        # Add small delay between calls (rate limit protection)
        if self.last_call_time:
            time_since_last = (now - self.last_call_time).total_seconds()
            if time_since_last < 1:  # Less than 1 second
                time.sleep(1 - time_since_last)
        
        # Check hourly limit
        elapsed_hours = (now - self.session_start_time).total_seconds() / 3600
        if elapsed_hours > 0:
            calls_per_hour = self.call_count / elapsed_hours
            if calls_per_hour > 4500:  # 90% of 5,000 limit
                print(f"⚠️  Approaching hourly rate limit ({calls_per_hour:.0f} calls/hour)")
                print(f"   Pausing for 1 minute...")
                time.sleep(60)
        
        # Check daily limit
        if self.call_count > 9000:  # 90% of 10,000 limit
            print(f"⚠️  WARNING: Approaching daily rate limit!")
            print(f"   Calls today: {self.call_count}")
            print(f"   Consider stopping and resuming tomorrow.")
        
        # Update tracking
        self.call_count += 1
        self.last_call_time = now
        
        # Log progress every 100 calls
        if self.call_count % 100 == 0:
            elapsed_time = (now - self.session_start_time).total_seconds() / 60
            print(f"📊 API Stats: {self.call_count} calls in {elapsed_time:.1f} minutes")
    
    def _make_request(self, params: Dict) -> Optional[Dict]:
        """
        Make HTTP GET request to API with retry logic.
        
        Args:
            params: Dictionary of URL parameters
        
        Returns:
            JSON response as dict, or None if request fails
        """
        # Check rate limits before making request
        self._check_rate_limits()
        
        for attempt in range(self.retry_count):
            try:
                response = requests.get(
                    self.base_url,
                    params=params,
                    timeout=self.timeout
                )
                response.raise_for_status()  # Raise exception for 4xx/5xx status codes
                return response.json()
            
            except requests.exceptions.Timeout:
                print(f"⚠️  Request timeout (attempt {attempt + 1}/{self.retry_count})")
                if attempt < self.retry_count - 1:
                    time.sleep(self.retry_delay)
            
            except requests.exceptions.RequestException as e:
                print(f"⚠️  Request failed: {e} (attempt {attempt + 1}/{self.retry_count})")
                if attempt < self.retry_count - 1:
                    time.sleep(self.retry_delay)
        
        print(f"❌ Failed to fetch data after {self.retry_count} attempts")
        return None
    
    def fetch_historical_weather(
        self,
        location_code: str,
        start_date: str,
        end_date: str,
        hourly_vars: Optional[List[str]] = None,
        daily_vars: Optional[List[str]] = None
    ) -> Optional[Dict]:
        """
        Fetch historical weather data for a location.
        
        Args:
            location_code: Location identifier (e.g., 'cape_town')
            start_date: Start date in 'YYYY-MM-DD' format
            end_date: End date in 'YYYY-MM-DD' format
            hourly_vars: List of hourly variables to fetch (default: HOURLY_VARIABLES)
            daily_vars: List of daily variables to fetch (default: DAILY_VARIABLES)
        
        Returns:
            JSON response as dictionary, or None if request fails
        
        Example:
            >>> client = OpenMeteoClient()
            >>> data = client.fetch_historical_weather(
            ...     'cape_town',
            ...     '2024-01-01',
            ...     '2024-01-31'
            ... )
        """
        # Get location details
        location = LOCATIONS.get(location_code)
        if not location:
            print(f"❌ Unknown location: {location_code}")
            return None
        
        # Use default variables if not specified
        if hourly_vars is None:
            hourly_vars = HOURLY_VARIABLES
        if daily_vars is None:
            daily_vars = DAILY_VARIABLES
        
        # Build API parameters
        params = {
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "start_date": start_date,
            "end_date": end_date,
            "hourly": ",".join(hourly_vars),
            "daily": ",".join(daily_vars),
            "temperature_unit": TEMPERATURE_UNIT,
            "wind_speed_unit": WIND_SPEED_UNIT,
            "precipitation_unit": PRECIPITATION_UNIT,
            "timezone": TIMEZONE,
        }
        
        print(f"📡 Fetching historical weather for {location['name']}...")
        print(f"   Date range: {start_date} to {end_date}")
        print(f"   Coordinates: {location['latitude']}, {location['longitude']}")
        
        return self._make_request(params)
    
    def fetch_forecast(
        self,
        location_code: str,
        forecast_days: int = 7,
        hourly_vars: Optional[List[str]] = None,
        daily_vars: Optional[List[str]] = None,
        past_days: int = 0
    ) -> Optional[Dict]:
        """
        Fetch weather forecast for a location.
        
        Args:
            location_code: Location identifier
            forecast_days: Number of days to forecast (1-16)
            hourly_vars: List of hourly variables
            daily_vars: List of daily variables
            past_days: Number of past days to include (0-92)
        
        Returns:
            JSON response as dictionary
        """
        location = LOCATIONS.get(location_code)
        if not location:
            print(f"❌ Unknown location: {location_code}")
            return None
        
        if hourly_vars is None:
            hourly_vars = HOURLY_VARIABLES
        if daily_vars is None:
            daily_vars = DAILY_VARIABLES
        
        params = {
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "forecast_days": forecast_days,
            "past_days": past_days,
            "hourly": ",".join(hourly_vars),
            "daily": ",".join(daily_vars),
            "current_weather": True,  # Include current conditions
            "temperature_unit": TEMPERATURE_UNIT,
            "wind_speed_unit": WIND_SPEED_UNIT,
            "precipitation_unit": PRECIPITATION_UNIT,
            "timezone": TIMEZONE,
        }
        
        print(f"📡 Fetching forecast for {location['name']}...")
        print(f"   Forecast days: {forecast_days}, Past days: {past_days}")
        
        return self._make_request(params)
    
    def fetch_current_weather(self, location_code: str) -> Optional[Dict]:
        """
        Fetch current weather conditions for a location.
        
        Args:
            location_code: Location identifier
        
        Returns:
            JSON response with current weather
        """
        location = LOCATIONS.get(location_code)
        if not location:
            print(f"❌ Unknown location: {location_code}")
            return None
        
        params = {
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "current_weather": True,
            "temperature_unit": TEMPERATURE_UNIT,
            "wind_speed_unit": WIND_SPEED_UNIT,
            "timezone": TIMEZONE,
        }
        
        print(f"📡 Fetching current weather for {location['name']}...")
        
        return self._make_request(params)


def save_raw_response(
    response_json: Dict,
    file_path: Path,
    create_dirs: bool = True
) -> bool:
    """
    Save raw JSON response to file.
    
    Args:
        response_json: JSON data to save
        file_path: Path where to save the file
        create_dirs: Create parent directories if they don't exist
    
    Returns:
        True if successful, False otherwise
    """
    try:
        if create_dirs:
            file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(response_json, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved raw data to: {file_path}")
        return True
    
    except Exception as e:
        print(f"❌ Failed to save file: {e}")
        return False


def generate_filename(
    location_code: str,
    data_type: str = "historical",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    timestamp: Optional[datetime] = None
) -> str:
    """
    Generate standardized filename for raw data files.
    
    Args:
        location_code: Location identifier
        data_type: 'historical', 'forecast', or 'current'
        start_date: Start date for historical data
        end_date: End date for historical data
        timestamp: Timestamp for forecast/current data
    
    Returns:
        Filename string
    
    Examples:
        >>> generate_filename('cape_town', 'historical', '2022-01-01', '2024-11-15')
        '2024-11-15_cape_town_2022-01-01_to_2024-11-15.json'
        
        >>> generate_filename('durban', 'forecast', timestamp=datetime(2024, 11, 15))
        '2024-11-15_durban_forecast.json'
    """
    if timestamp is None:
        timestamp = datetime.now()
    
    date_str = timestamp.strftime("%Y-%m-%d")
    
    if data_type == "historical" and start_date and end_date:
        return f"{date_str}_{location_code}_{start_date}_to_{end_date}.json"
    elif data_type == "forecast":
        return f"{date_str}_{location_code}_forecast.json"
    elif data_type == "current":
        time_str = timestamp.strftime("%H-%M")
        return f"{date_str}_{time_str}_{location_code}_current.json"
    else:
        return f"{date_str}_{location_code}_{data_type}.json"


# Convenience function for quick testing
def quick_fetch_test(location_code: str = "cape_town", days: int = 1):
    """
    Quick test function to fetch a small amount of data.
    Useful for testing API connectivity.
    
    Args:
        location_code: Location to test
        days: Number of days to fetch
    """
    client = OpenMeteoClient()
    
    # Get yesterday's date
    end_date = datetime.now() - timedelta(days=1)
    start_date = end_date - timedelta(days=days - 1)
    
    data = client.fetch_historical_weather(
        location_code,
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d")
    )
    
    if data:
        print(f"\n✅ Successfully fetched {days} day(s) of data!")
        print(f"   Data keys: {list(data.keys())}")
        if 'hourly' in data:
            print(f"   Hourly variables: {list(data['hourly'].keys())}")
        if 'daily' in data:
            print(f"   Daily variables: {list(data['daily'].keys())}")
        return data
    else:
        print("\n❌ Failed to fetch data")
        return None


if __name__ == "__main__":
    # Test the API client
    print("Testing Open-Meteo API Client...")
    print("=" * 60)
    quick_fetch_test("cape_town", days=1)
