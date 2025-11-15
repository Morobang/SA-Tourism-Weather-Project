# SA Tourism Weather Project - Complete Step-by-Step Plan

## 🎯 What Are We Building?

A **complete weather data pipeline** for South Africa that:
1. Gets weather data from Open-Meteo API (historical + forecast)
2. Stores it properly (files + database)
3. Cleans and processes it
4. Analyzes it (find patterns, tourism insights)
5. Builds ML models (predict weather, tourism suitability)
6. Visualizes it (Power BI dashboards, interactive charts)
7. Automates everything (Airflow runs daily)

**Why?** To prove you can build a complete data engineering + data science project for FREE, using real APIs, and showcase all the skills you learned for your AWS Data Engineering exam.

---

## 📚 PHASE 0: Understanding What Data We Need & Why

Before we write ANY code, let's discuss what data exists and what we actually need.

### Open-Meteo API - What's Available?

Open-Meteo gives us **3 different types of data**:

#### 1. **Historical Weather API** (1940 - yesterday)
- **What it is:** Actual observed weather that already happened
- **How far back:** Goes back to 1940! (but quality varies by period)
- **Best quality period:** 2000-present (hourly data available)
- **Example:** "What was the temperature in Cape Town on January 15, 2023?"
- **Why we need it:** 
  - Train ML models (need past data to learn patterns)
  - Analyze trends (is Cape Town getting hotter over the years?)
  - Compare seasons (which month has best weather for tourists?)
  - Validate forecasts (were the predictions accurate?)

#### 2. **Forecast API** (today + next 7-16 days)
- **What it is:** Predicted weather for the future
- **How far ahead:** Default 7 days, can get up to 16 days
- **Special feature:** Can also look back 92 days using `past_days` parameter
- **Example:** "What will the temperature be in Johannesburg next Tuesday?"
- **Why we need it:**
  - Help tourists plan trips
  - Track forecast accuracy (were yesterday's predictions correct?)
  - Build "forecast correction" models (improve the predictions)
  - Monitor current conditions

#### 3. **Historical Forecast API** (archived predictions from 2022+)
- **What it is:** OLD forecasts that were made in the past (what the model PREDICTED back then)
- **Example:** "On January 1, 2024, what did the model predict for January 7, 2024?"
- **Why we need it:**
  - Compare prediction vs reality
  - Measure forecast skill (how good is the model?)
  - Build bias-correction models
  - Research purposes

### Decision Time: Which APIs Will We Use?

**For this project, we'll use:**

1. ✅ **Historical Weather API** → Get 2-3 years of actual weather (2022-2025)
2. ✅ **Forecast API** → Get daily forecasts (7-16 days ahead)
3. ❌ **Historical Forecast API** → Skip for now (advanced, we can add later)

**Why skip Historical Forecast API?**
- More complex to manage (stores forecasts made on different dates)
- We can still validate forecasts by comparing today's forecast with tomorrow's actual weather
- Keeps project simpler for Phase 1


---

## 🗺️ PHASE 1: What Weather Variables Do We Need?

### Understanding Weather Variables

Open-Meteo provides **100+ different weather measurements**. We can't collect everything (too much data, too slow). We need to pick what matters for **tourism analysis**.

### Core Variables We'll Collect

#### **Hourly Data** (measurements every hour)

**Temperature Variables** ⭐ (PRIORITY 1)
- `temperature_2m` - Air temperature at 2 meters height (°C)
  - **Why:** Main factor for tourists ("Is it hot or cold?")
  - **Use case:** Track daily temperature patterns, heatwaves, cold snaps
  
- `apparent_temperature` - "Feels like" temperature
  - **Why:** Combines temperature + humidity + wind (what it REALLY feels like)
  - **Use case:** Better than actual temp for comfort assessment

**Precipitation Variables** ⭐ (PRIORITY 1)
- `precipitation` - Total precipitation (rain + snow + showers) in mm
  - **Why:** Tourists avoid rainy days
  - **Use case:** Identify dry seasons, predict rain probability
  
- `rain` - Rain only (mm)
  - **Why:** Separate rain from snow for regional analysis
  
- `precipitation_probability` - Chance of rain (0-100%)
  - **Why:** Helps tourists assess risk
  - **Use case:** "70% chance of rain tomorrow"

**Weather Conditions** ⭐ (PRIORITY 1)
- `weather_code` - WMO weather code (0-99)
  - **Why:** Describes overall conditions (clear, cloudy, rainy, stormy)
  - **Use case:** Classify days as "good" or "bad" for tourism
  - **Codes:** 0=clear, 1-3=partly cloudy, 51-67=rain, 71-77=snow, 95-99=thunderstorm

**Cloud & Visibility** (PRIORITY 2)
- `cloud_cover` - Total cloud cover (0-100%)
  - **Why:** Affects photography, scenic views, outdoor activities
  
- `visibility` - How far you can see (meters)
  - **Why:** Important for safaris, mountain viewing, coastal drives

**Wind Variables** (PRIORITY 2)
- `wind_speed_10m` - Wind speed at 10m height (km/h)
  - **Why:** Affects outdoor comfort, beach activities
  
- `wind_direction_10m` - Wind direction (0-360°)
  - **Why:** Some directions are warmer/cooler
  
- `wind_gusts_10m` - Maximum wind gusts (km/h)
  - **Why:** Safety for outdoor activities

**Humidity & Comfort** (PRIORITY 3)
- `relative_humidity_2m` - Humidity percentage (0-100%)
  - **Why:** High humidity = feels hotter, uncomfortable
  
- `dew_point_2m` - Dew point temperature (°C)
  - **Why:** Indicates muggy conditions

**Sun & UV** (PRIORITY 2)
- `is_day` - Is it daytime? (1=yes, 0=no)
  - **Why:** Filter out nighttime for certain analyses

**Advanced (PRIORITY 4 - Optional)**
- `soil_temperature_0cm` - Ground surface temperature
- `soil_moisture_0_to_1cm` - Ground moisture
- `evapotranspiration` - Water evaporation rate
- Pressure levels (advanced atmospheric data)

---

#### **Daily Data** (one value per day - aggregated from hourly)

**Temperature** ⭐
- `temperature_2m_max` - Highest temp of the day
- `temperature_2m_min` - Lowest temp of the day
- `temperature_2m_mean` - Average temperature
  - **Why:** "Cape Town: 15-25°C" is what tourists want to know

**Precipitation** ⭐
- `precipitation_sum` - Total rain/snow for the day (mm)
- `precipitation_hours` - How many hours it rained
  - **Why:** Difference between "light drizzle for 1 hour" vs "all-day rain"

**Sun & Light** ⭐
- `sunrise` - Time of sunrise (ISO format)
- `sunset` - Time of sunset
- `daylight_duration` - Total daylight in seconds
- `sunshine_duration` - Actual sunshine (not cloudy) in seconds
  - **Why:** More sunshine = better for tourism
  
- `uv_index_max` - Peak UV radiation (0-11+)
  - **Why:** Safety (sunburn risk), health warnings

**Weather Summary** ⭐
- `weather_code` - Dominant weather condition for the day

**Wind** 
- `wind_speed_10m_max` - Maximum wind speed
- `wind_gusts_10m_max` - Strongest gusts
- `dominant_wind_direction_10m` - Prevailing wind direction

---

#### **Current Weather** (right now snapshot)

- `temperature_2m` - Current temperature
- `relative_humidity_2m` - Current humidity
- `apparent_temperature` - Current "feels like"
- `precipitation` - Is it raining NOW?
- `weather_code` - Current conditions
- `cloud_cover` - Current cloud cover
- `wind_speed_10m` - Current wind
- `wind_direction_10m` - Current wind direction
- `is_day` - Is it day or night?

**Why collect current weather?**
- Real-time dashboard updates
- Validation (compare current reading with yesterday's forecast)
- Live tourism recommendations

---

### Decision: Our Final Variable List (Start Simple, Expand Later)

**Phase 1 - Core Collection (Start Here):**

**Hourly:**
- temperature_2m
- apparent_temperature
- precipitation
- precipitation_probability
- weather_code
- cloud_cover
- wind_speed_10m
- wind_direction_10m
- relative_humidity_2m

**Daily:**
- temperature_2m_max
- temperature_2m_min
- precipitation_sum
- precipitation_hours
- weather_code
- sunrise
- sunset
- sunshine_duration
- uv_index_max

**Current:**
- All available current weather fields

**Phase 2 - Expand Later:**
- Add visibility, wind gusts, soil temperature, etc.
- Add pressure levels for advanced ML

---

## 📂 PHASE 2: Where & How Do We Store This Data?

### The Big Question: Where Does Each Type of Data Go?

We'll use a **3-layer storage strategy**:

#### **Layer 1: Raw Data** (`data/raw/`)
- **What:** Exact JSON responses from the API (no changes)
- **Why:** 
  - Backup (if processing fails, we can reprocess)
  - Debugging (see exactly what API returned)
  - Audit trail (prove data came from API)
- **Format:** JSON files
- **Organization:**
  ```
  data/raw/
    historical/
      2024-11-15_cape_town_historical.json
      2024-11-15_johannesburg_historical.json
    forecast/
      2024-11-15_cape_town_forecast.json
      2024-11-16_cape_town_forecast.json  # New forecast each day
    current/
      2024-11-15_12-00_cape_town_current.json
  ```

#### **Layer 2: Processed Data** (`data/processed/`)
- **What:** Cleaned, structured data ready for analysis
- **Why:** 
  - Fast to load (Parquet is 10x faster than JSON)
  - Smaller file size (compressed)
  - Organized by type
- **Format:** Parquet files (columnar, efficient)
- **Organization:**
  ```
  data/processed/
    hourly/
      cape_town_hourly_2022.parquet
      cape_town_hourly_2023.parquet
      johannesburg_hourly_2022.parquet
    daily/
      cape_town_daily_2022.parquet
      all_locations_daily_2022-2024.parquet
    current/
      current_weather_snapshots_2024-11.parquet
  ```

#### **Layer 3: Database** (`data/database/weather.db`)
- **What:** SQLite database for fast queries, joins, filtering
- **Why:**
  - Power BI can connect to it
  - Fast queries (indexed)
  - Relational (join locations + weather + forecasts)
  - Good for Airflow to track what's loaded
- **Format:** SQLite (or upgrade to PostgreSQL later)
- **Tables:** (We'll design schema in Phase 3)

---

### Historical vs Forecast Storage - The Critical Difference

**Historical Data (Actual Weather That Happened):**
- **When we get it:** One-time backfill, maybe monthly updates
- **Date range:** 2022-01-01 to yesterday
- **Storage:**
  - Raw: `data/raw/historical/YYYY-MM-DD_location_historical.json`
  - Processed: `data/processed/hourly/location_hourly_YYYY.parquet`
  - Database: `weather_hourly` table (flag: `is_forecast=0`)
- **How much:** ~3 years × 5 locations × 365 days × 24 hours = ~131,400 rows

**Forecast Data (Predicted Future Weather):**
- **When we get it:** Every day (Airflow runs daily)
- **Date range:** Today + 7 days ahead
- **Storage:**
  - Raw: `data/raw/forecast/YYYY-MM-DD_location_forecast.json`
    - Keep for 30 days, then delete (saves space)
  - Processed: `data/processed/forecast/location_forecast_YYYY-MM.parquet`
  - Database: `weather_forecast` table (separate from historical)
    - Include `forecast_made_on` date (when was this prediction made?)
- **How much:** Daily append (5 locations × 7 days × 24 hours = 840 new rows/day)

**Current Weather Snapshots:**
- **When we get it:** Every hour (or multiple times per day)
- **Storage:**
  - Raw: `data/raw/current/YYYY-MM-DD_HH-mm_location_current.json`
  - Processed: `data/processed/current/current_snapshots_YYYY-MM.parquet`
  - Database: `weather_current` table
- **How much:** 5 locations × 24 snapshots/day = 120 rows/day

---

### Data Volume Planning

Let's calculate how much space we need:

**Historical (3 years):**
- Hourly: 5 locations × 3 years × 365 days × 24 hours × 10 variables ≈ 1.3M data points
- JSON: ~500 MB
- Parquet: ~50 MB (10x compression)
- SQLite: ~100 MB (with indexes)

**Forecast (ongoing):**
- Per day: 5 locations × 7 days × 24 hours × 10 variables = 8,400 data points
- Monthly: ~250,000 data points
- Parquet: ~2 MB/month

**Total after 1 year:** ~500 MB (very manageable!)

---

## 🗄️ PHASE 3: Database Design - What Tables Do We Need?

### Table 1: `locations`
**Purpose:** Store info about each South African city/region

```sql
CREATE TABLE locations (
    id INTEGER PRIMARY KEY,
    location_code TEXT UNIQUE NOT NULL,  -- 'cape_town', 'johannesburg'
    name TEXT NOT NULL,                   -- 'Cape Town'
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    region TEXT,                          -- 'Western Cape'
    elevation INTEGER,                    -- meters above sea level
    timezone TEXT,                        -- 'Africa/Johannesburg'
    description TEXT,                     -- 'Popular tourist destination...'
    is_active BOOLEAN DEFAULT 1,          -- Still collecting data?
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Why each field?**
- `location_code`: Easy to use in code ('cape_town' in file names)
- `latitude/longitude`: Required for API calls
- `elevation`: Open-Meteo can adjust for altitude
- `is_active`: Can disable locations without deleting history

---

### Table 2: `weather_hourly`
**Purpose:** Store hourly historical weather

```sql
CREATE TABLE weather_hourly (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER NOT NULL,
    timestamp_utc TIMESTAMP NOT NULL,     -- '2024-11-15 12:00:00' (UTC)

    timestamp_local TIMESTAMP,            -- Local time in South Africa
    temperature_2m REAL,
    apparent_temperature REAL,
    precipitation REAL,
    precipitation_probability REAL,
    weather_code INTEGER,
    cloud_cover REAL,
    wind_speed_10m REAL,
    wind_direction_10m REAL,
    relative_humidity_2m REAL,
    
    -- Metadata
    data_source TEXT DEFAULT 'historical',  -- 'historical' or 'forecast'
    raw_file_path TEXT,                     -- Path to raw JSON
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (location_id) REFERENCES locations(id),
    UNIQUE(location_id, timestamp_utc)      -- Prevent duplicates
);

CREATE INDEX idx_hourly_location_time ON weather_hourly(location_id, timestamp_utc);
CREATE INDEX idx_hourly_date ON weather_hourly(DATE(timestamp_utc));
```

**Why this design?**
- `timestamp_utc`: Standardized time for comparisons
- `timestamp_local`: Easier for humans to read ("8 AM in Cape Town")
- `UNIQUE constraint`: Can't accidentally insert same hour twice
- `raw_file_path`: Trace back to original data if needed
- Indexes: Fast queries by location and time

---

### Table 3: `weather_daily`
**Purpose:** Store daily aggregated weather

```sql
CREATE TABLE weather_daily (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER NOT NULL,
    date DATE NOT NULL,                   -- '2024-11-15'
    
    -- Temperature
    temperature_2m_max REAL,
    temperature_2m_min REAL,
    temperature_2m_mean REAL,
    
    -- Precipitation
    precipitation_sum REAL,
    precipitation_hours REAL,
    
    -- Conditions
    weather_code INTEGER,
    
    -- Sun
    sunrise TIME,
    sunset TIME,
    daylight_duration INTEGER,            -- seconds
    sunshine_duration INTEGER,            -- seconds
    uv_index_max REAL,
    
    -- Wind
    wind_speed_10m_max REAL,
    
    -- Metadata
    data_source TEXT DEFAULT 'historical',
    raw_file_path TEXT,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (location_id) REFERENCES locations(id),
    UNIQUE(location_id, date)
);

CREATE INDEX idx_daily_location_date ON weather_daily(location_id, date);
CREATE INDEX idx_daily_month ON weather_daily(strftime('%Y-%m', date));
```

---

### Table 4: `weather_forecast`
**Purpose:** Store forecasted weather (predictions)

```sql
CREATE TABLE weather_forecast (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER NOT NULL,
    forecast_made_on DATE NOT NULL,       -- When was this forecast created?
    forecast_for_timestamp TIMESTAMP NOT NULL,  -- What time is being predicted?
    
    -- Same weather fields as hourly
    temperature_2m REAL,
    apparent_temperature REAL,
    precipitation REAL,
    precipitation_probability REAL,
    weather_code INTEGER,
    cloud_cover REAL,
    wind_speed_10m REAL,
    wind_direction_10m REAL,
    relative_humidity_2m REAL,
    
    -- Metadata
    forecast_hours_ahead INTEGER,        -- How far in the future? (24, 48, 168)
    raw_file_path TEXT,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (location_id) REFERENCES locations(id),
    UNIQUE(location_id, forecast_made_on, forecast_for_timestamp)
);

CREATE INDEX idx_forecast_location ON weather_forecast(location_id, forecast_for_timestamp);
```

**Why separate forecast table?**
- Can compare multiple forecasts for same future date
- Track forecast accuracy over time
- Example: "On Nov 10, what did we predict for Nov 15? On Nov 12, what did we predict for Nov 15?"

---

### Table 5: `weather_current`
**Purpose:** Snapshots of current weather conditions

```sql
CREATE TABLE weather_current (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id INTEGER NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    
    temperature_2m REAL,
    relative_humidity_2m REAL,
    apparent_temperature REAL,
    is_day INTEGER,                      -- 1 or 0
    precipitation REAL,
    weather_code INTEGER,
    cloud_cover REAL,
    wind_speed_10m REAL,
    wind_direction_10m REAL,
    
    raw_file_path TEXT,
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (location_id) REFERENCES locations(id)
);

CREATE INDEX idx_current_location_time ON weather_current(location_id, timestamp);
```

---

### Table 6: `ingestion_log`
**Purpose:** Track every data collection job (for monitoring & debugging)

```sql
CREATE TABLE ingestion_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_type TEXT NOT NULL,              -- 'historical_backfill', 'daily_forecast', 'current_snapshot'
    location_code TEXT,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    status TEXT,                         -- 'success', 'failed', 'partial'
    records_fetched INTEGER,
    records_inserted INTEGER,
    error_message TEXT,
    api_url TEXT,                        -- Full URL called
    dag_run_id TEXT,                     -- Airflow DAG run ID (if applicable)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ingestion_time ON ingestion_log(start_time);
CREATE INDEX idx_ingestion_status ON ingestion_log(status);
```

**Why track ingestion?**
- Debug failures ("Why did Cape Town fail yesterday?")
- Monitor API usage (how many calls per day?)
- Airflow can check this before re-running
- Audit trail for compliance

---

## 🔄 PHASE 4: The Data Flow - From API to Storage (Step by Step)

### How Does Data Actually Move Through the System?

Let me walk you through the COMPLETE journey of weather data:

### Journey 1: Historical Backfill (One-Time Setup)

**Step 1: You decide the date range**
- Example: "Get all hourly weather for Cape Town from 2022-01-01 to 2024-11-14"

**Step 2: Python script calls Open-Meteo Historical API**
```python
# src/api_client.py makes this call:
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": -33.9249,
    "longitude": 18.4241,
    "start_date": "2022-01-01",
    "end_date": "2024-11-14",
    "hourly": "temperature_2m,precipitation,weather_code,...",
    "timezone": "auto"
}
response = requests.get(url, params=params)
```

**Step 3: Save raw response**
- File: `data/raw/historical/2024-11-15_cape_town_2022-2024.json`
- Content: Exact JSON from API (no modifications)
- Why: Backup, can reprocess if needed

**Step 4: Parse JSON and clean data**
- `src/data_processing.py` reads the JSON
- Converts to pandas DataFrame
- Cleans missing values (NaN → NULL)
- Adds calculated fields (e.g., date from timestamp)
- Validates (check for impossible values like temp = 999°C)

**Step 5: Save to Parquet**
- File: `data/processed/hourly/cape_town_hourly_2022-2024.parquet`
- Format: Compressed, columnar (fast to load)
- Why: Analysis in notebooks, ML training

**Step 6: Insert to database**
- `src/database.py` inserts rows into `weather_hourly`
- Check for duplicates (UNIQUE constraint prevents re-insertion)
- Log success in `ingestion_log` table

**Step 7: Repeat for all locations**
- Cape Town ✅
- Johannesburg ✅
- Durban ✅
- Kruger Park ✅
- Port Elizabeth ✅

**Result:** You now have 3 years of historical data!

---

### Journey 2: Daily Forecast Collection (Runs Every Day via Airflow)

**Step 1: Airflow triggers at 6:00 AM**
- DAG: `daily_weather_dag`
- Runs automatically every morning

**Step 2: Python script calls Forecast API**
```python
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": -33.9249,
    "longitude": 18.4241,
    "forecast_days": 7,              # Next 7 days
    "hourly": "temperature_2m,...",
    "daily": "temperature_2m_max,...",
    "current_weather": True,
    "timezone": "auto"
}
```

**Step 3: Save raw response**
- File: `data/raw/forecast/2024-11-15_cape_town_forecast.json`
- Keep for 30 days, then auto-delete (saves space)

**Step 4: Parse and extract 3 data types**

**4a) Current weather** → `weather_current` table
- Just the "current_weather" section of response
- One row per location

**4b) Hourly forecast** → `weather_forecast` table
- Next 168 hours (7 days × 24 hours)
- Include `forecast_made_on = '2024-11-15'`
- Include `forecast_hours_ahead` (24, 48, 72, etc.)

**4c) Daily forecast** → Similar table or merge with `weather_daily`
- Next 7 days of aggregates

**Step 5: Validation**
- Check: Did we get data for all 5 locations?
- Check: Are there any NULLs in critical fields?
- Check: Is temperature in reasonable range (-20 to 50°C)?

**Step 6: Update database**
- Insert new forecast rows
- Update `ingestion_log` with status

**Step 7: (Optional) Compare with yesterday's forecast**
- "Yesterday we predicted today would be 25°C. It's actually 23°C."
- Store forecast error for ML training

**Result:** Fresh forecasts every day!

---

### Journey 3: Current Weather Snapshots (Runs Every Hour)

**Step 1: Airflow triggers hourly**
- DAG: `hourly_current_weather_dag`
- Runs at :00 minutes every hour

**Step 2: Call API for current conditions only**
```python
params = {
    "latitude": -33.9249,
    "longitude": 18.4241,
    "current_weather": True
}
```

**Step 3: Save snapshot**
- File: `data/raw/current/2024-11-15_14-00_cape_town.json`
- Insert into `weather_current` table

**Step 4: (Optional) Real-time dashboard update**
- Export to CSV for Power BI refresh
- Or: Update live web dashboard

**Result:** Track conditions throughout the day!

---

## 🛠️ PHASE 5: Building the Code - What Scripts Do We Need?

Now that we know WHAT data and WHERE it goes, let's plan WHAT CODE to write.

### Module 1: `src/config.py`
**Purpose:** Central configuration (no hardcoded values!)

**What goes in it:**
```python
# API settings
API_BASE_URL = "https://api.open-meteo.com/v1/forecast"
API_TIMEOUT = 30  # seconds
API_RETRY_COUNT = 3

# Locations
LOCATIONS = {
    "cape_town": {
        "name": "Cape Town",
        "latitude": -33.9249,
        "longitude": 18.4241,
        "region": "Western Cape",
        "timezone": "Africa/Johannesburg"
    },
    # ... more locations
}

# Weather variables
HOURLY_VARIABLES = [
    "temperature_2m",
    "precipitation",
    # ... full list
]

DAILY_VARIABLES = [
    "temperature_2m_max",
    # ... full list
]

# Paths
RAW_DATA_DIR = "data/raw"
PROCESSED_DATA_DIR = "data/processed"
DATABASE_PATH = "data/database/weather.db"

# Date ranges
HISTORICAL_START_DATE = "2022-01-01"
FORECAST_DAYS = 7
```

---

### Module 2: `src/api_client.py`
**Purpose:** Talk to Open-Meteo API

**Functions to write:**

```python
def fetch_historical_weather(location_code, start_date, end_date):
    """
    Get historical weather for a location.
    
    Args:
        location_code: 'cape_town', 'johannesburg', etc.
        start_date: '2022-01-01'
        end_date: '2024-11-14'
    
    Returns:
        dict: Raw JSON response from API
    
    Steps:
        1. Get lat/lon from LOCATIONS config
        2. Build API URL with params
        3. Make HTTP GET request
        4. Handle errors (retry 3 times)
        5. Return JSON
    """
    pass

def fetch_forecast(location_code, forecast_days=7):
    """Get forecast for next N days"""
    pass

def fetch_current_weather(location_code):
    """Get current conditions right now"""
    pass

def save_raw_response(response_json, file_path):
    """Save JSON to data/raw/"""
    pass
```

**Error handling:**
- Retry on network failures
- Log errors
- Return None if API is down (don't crash!)

---

### Module 3: `src/data_processing.py`
**Purpose:** Clean and transform raw JSON

**Functions to write:**

```python
def parse_hourly_data(raw_json, location_code):
    """
    Convert API JSON to pandas DataFrame.
    
    Steps:
        1. Extract 'hourly' section from JSON
        2. Create DataFrame with columns: time, temperature_2m, precipitation, etc.
        3. Convert time strings to datetime
        4. Add location_id column
        5. Handle missing values
        6. Validate data types
    
    Returns:
        pd.DataFrame
    """
    pass

def parse_daily_data(raw_json, location_code):
    """Parse daily aggregates"""
    pass

def clean_temperature(df):
    """
    Validate temperature values.
    
    Rules:
        - Must be between -50°C and 60°C (SA range)
        - Replace outliers with NULL
    """
    pass

def save_to_parquet(df, file_path):
    """Save DataFrame to Parquet format"""
    pass
```

---

### Module 4: `src/database.py`
**Purpose:** All database operations

**Functions to write:**

```python
def get_connection():
    """Connect to SQLite database"""
    pass

def init_database():
    """
    Create all tables if they don't exist.
    
    Steps:
        1. Read SQL from sql/schema.sql
        2. Execute CREATE TABLE statements
        3. Create indexes
    """
    pass

def insert_hourly_weather(df):
    """
    Insert DataFrame into weather_hourly table.
    
    Steps:
        1. Check for duplicates (location_id + timestamp)
        2. Insert only new rows
        3. Return count of inserted rows
    """
    pass

def insert_daily_weather(df):
    """Insert into weather_daily"""
    pass

def insert_forecast(df, forecast_made_on):
    """Insert into weather_forecast with forecast_made_on date"""
    pass

def log_ingestion(job_type, location_code, status, records_inserted):
    """Insert row into ingestion_log"""
    pass

def get_latest_date(location_code):
    """
    Query: What's the most recent date we have data for?
    
    Used to avoid re-downloading data we already have.
    """
    pass
```

---

### Script 1: `scripts/initial_setup.py`
**Purpose:** One-time setup (run once to get started)

**What it does:**

```python
#!/usr/bin/env python3
"""
Initial setup script.
Run this ONCE to set up the project.
"""

def main():
    print("Step 1: Creating folders...")
    create_folder_structure()
    
    print("Step 2: Creating database...")
    init_database()
    
    print("Step 3: Inserting locations...")
    insert_locations()
    
    print("Step 4: Testing API connection...")
    test_api_call()
    
    print("✅ Setup complete!")

if __name__ == "__main__":
    main()
```

---

### Script 2: `scripts/backfill_historical.py`
**Purpose:** Download all historical data (run once or monthly)

**What it does:**

```python
#!/usr/bin/env python3
"""
Backfill historical weather data for all locations.
"""

def backfill_location(location_code):
    print(f"📥 Downloading {location_code}...")
    
    # 1. Call API
    raw_json = fetch_historical_weather(
        location_code,
        start_date="2022-01-01",
        end_date=yesterday
    )
    
    # 2. Save raw
    save_raw_response(raw_json, f"data/raw/historical/{location_code}.json")
    
    # 3. Process
    df_hourly = parse_hourly_data(raw_json, location_code)
    df_daily = parse_daily_data(raw_json, location_code)
    
    # 4. Save Parquet
    save_to_parquet(df_hourly, f"data/processed/hourly/{location_code}_2022-2024.parquet")
    save_to_parquet(df_daily, f"data/processed/daily/{location_code}_2022-2024.parquet")
    
    # 5. Insert to DB
    rows_inserted = insert_hourly_weather(df_hourly)
    insert_daily_weather(df_daily)
    
    # 6. Log
    log_ingestion("historical_backfill", location_code, "success", rows_inserted)
    
    print(f"✅ {location_code}: {rows_inserted} rows inserted")

def main():
    for location_code in LOCATIONS.keys():
        backfill_location(location_code)

if __name__ == "__main__":
    main()
```

---

### Airflow DAG 1: `airflow/dags/daily_weather_dag.py`
**Purpose:** Run every day to get fresh forecasts

**What it does:**

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def fetch_and_store_forecast():
    """Fetch forecast for all locations"""
    for location_code in LOCATIONS.keys():
        # 1. Fetch forecast
        raw_json = fetch_forecast(location_code, forecast_days=7)
        
        # 2. Save raw
        today = datetime.now().strftime("%Y-%m-%d")
        save_raw_response(raw_json, f"data/raw/forecast/{today}_{location_code}.json")
        
        # 3. Process
        df_forecast = parse_hourly_data(raw_json, location_code)
        
        # 4. Insert to DB
        insert_forecast(df_forecast, forecast_made_on=today)

default_args = {
    'owner': 'data_engineer',
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    'daily_weather_collection',
    default_args=default_args,
    description='Collect daily weather forecasts',
    schedule_interval='0 6 * * *',  # 6 AM every day
    start_date=datetime(2024, 11, 1),
    catchup=False
) as dag:
    
    task = PythonOperator(
        task_id='fetch_forecasts',
        python_callable=fetch_and_store_forecast
    )
```

---

## 📊 PHASE 6: Analysis & ML - What Questions Will We Answer?

### Tourism Analysis Questions

1. **Best time to visit each city?**
   - Query: Average temperature, precipitation, sunshine by month
   - Visualization: Heatmap of weather quality by month & location

2. **Which city has the most consistent weather?**
   - Calculate: Standard deviation of temperature
   - Find: Lowest variability = most predictable

3. **Rainy season patterns?**
   - Query: Precipitation by month
   - Identify: Wet vs dry seasons

4. **UV safety?**
   - Query: Average UV index by month
   - Alert: When to warn tourists about sunburn risk

5. **Temperature comfort zones?**
   - Calculate: Days with temp between 18-28°C (comfortable range)
   - Rank: Cities by "comfortable days per year"

### Machine Learning Projects

**Project 1: Tourism Suitability Score**
- Combine: temperature, precipitation, sunshine, wind
- Formula: `score = (0.4 * temp_comfort) + (0.3 * no_rain) + (0.2 * sunshine) + (0.1 * low_wind)`
- Output: 0-100 score for each day
- Use: "Cape Town: 85/100 tourist-friendly today!"

**Project 2: Weather Forecast Correction**
- Compare: Yesterday's 24-hour forecast vs actual weather today
- Train: Model to predict forecast error
- Improve: "API says 25°C, but model predicts 23°C"

**Project 3: Precipitation Classifier**
- Features: Humidity, pressure, wind, cloud cover
- Target: Will it rain in next 3 hours?
- Model: Random Forest or XGBoost

**Project 4: Temperature Prediction**
- Features: Past 7 days temp, season, location
- Target: Tomorrow's temperature
- Model: LSTM or simple linear regression

---

## 🎨 PHASE 7: Visualization - Power BI & Dashboards

### Power BI Dashboard Design

**Page 1: Overview**
- Map: South Africa with current temp at each location
- Cards: Current conditions (temp, weather, wind)
- 7-day forecast: Temperature line chart

**Page 2: Historical Trends**
- Line chart: Temperature over time (3 years)
- Bar chart: Monthly precipitation
- Heatmap: Weather quality by month/year

**Page 3: Tourism Insights**
- Table: Best months to visit each city
- Gauge: Tourism suitability score
- Comparison: City rankings

**Page 4: Forecast vs Actual**
- Scatter plot: Predicted vs actual temperature
- Accuracy metrics: MAE, RMSE
- Trend: Is forecast getting better over time?

### How to Connect Power BI

**Option 1: CSV Export (Easiest)**
1. Python script exports to `data/exports/weather_summary.csv`
2. Power BI Desktop → Get Data → CSV
3. Refresh data: Re-run script, refresh in Power BI

**Option 2: Direct Database (Best)**
1. Install Power BI Desktop
2. Get Data → SQLite (via ODBC driver)
3. Connect to `data/database/weather.db`
4. Auto-refresh on schedule

---

## ⚙️ PHASE 8: Automation with Airflow

### Why Airflow?

- **Alternative to n8n:** Free, open-source, powerful
- **Local setup:** No cloud costs
- **Scheduling:** Run daily/hourly automatically
- **Monitoring:** See which jobs failed
- **Retries:** Auto-retry on failure
- **Dependencies:** Run tasks in order (fetch → process → store)

### Airflow Setup

**Option 1: Local Install**
```powershell
pip install apache-airflow==2.7.0
airflow db init
airflow users create --username admin --password admin --role Admin
airflow webserver --port 8080
airflow scheduler
```

**Option 2: Docker (Recommended)**
```powershell
# Use docker-compose.yml
docker-compose up -d
```

### DAGs We'll Create

1. **`daily_weather_dag.py`** - Fetch forecasts (runs daily at 6 AM)
2. **`hourly_current_dag.py`** - Current conditions (runs hourly)
3. **`weekly_backfill_dag.py`** - Backfill recent history (runs weekly)
4. **`monthly_analysis_dag.py`** - Generate reports (runs monthly)
5. **`ml_training_dag.py`** - Retrain models (runs monthly)

---

## ✅ YOUR STEP-BY-STEP ACTION PLAN

### Week 1: Setup & Exploration

**Day 1: Environment**
- [ ] Create folder structure
- [ ] Create `.gitignore`
- [ ] Create `requirements.txt`
- [ ] Set up virtual environment
- [ ] Install dependencies

**Day 2-3: Config & First API Call**
- [ ] Write `src/config.py` with locations
- [ ] Write `src/api_client.py` (just `fetch_historical_weather` function)
- [ ] Create `notebooks/01_api_exploration.ipynb`
- [ ] Make first API call for Cape Town (1 day of data)
- [ ] Print the JSON to understand structure

**Day 4-5: Data Processing**
- [ ] Write `src/data_processing.py` (parse_hourly_data)
- [ ] Convert JSON to DataFrame
- [ ] Save to Parquet file
- [ ] Visualize temperature in notebook

### Week 2: Database

**Day 6-7: Database Setup**
- [ ] Create `sql/schema.sql` with all CREATE TABLE statements
- [ ] Write `src/database.py` (init_database, get_connection)
- [ ] Run script to create database
- [ ] Manually insert 1 location into `locations` table
- [ ] Test: Query the location back

**Day 8-9: Loading Data**
- [ ] Write `insert_hourly_weather()` function
- [ ] Load DataFrame into database
- [ ] Check: Query to see if data is there
- [ ] Write `insert_daily_weather()` function

**Day 10: Testing**
- [ ] Create `tests/test_api_client.py`
- [ ] Mock API response
- [ ] Test parsing functions
- [ ] Run: `pytest tests/`

### Week 3: Historical Backfill

**Day 11-12: Backfill Script**
- [ ] Write `scripts/backfill_historical.py`
- [ ] Start with 1 location, 1 month of data
- [ ] Verify: Check database, check Parquet file
- [ ] Expand: All 5 locations, 3 years

**Day 13-14: EDA Notebook**
- [ ] Create `notebooks/02_eda.ipynb`
- [ ] Load data from Parquet
- [ ] Plot: Temperature over time
- [ ] Plot: Precipitation by month
- [ ] Calculate: Average temp by city

### Week 4: Forecasts

**Day 15-16: Forecast Collection**
- [ ] Update `src/api_client.py` (add `fetch_forecast`)
- [ ] Create `weather_forecast` table
- [ ] Write script to fetch today's forecast
- [ ] Insert into database

**Day 17: Airflow Basics**
- [ ] Install Airflow (local or Docker)
- [ ] Access web UI (http://localhost:8080)
- [ ] Create simple test DAG ("Hello World")
- [ ] Trigger it manually

**Day 18-19: Daily Forecast DAG**
- [ ] Write `airflow/dags/daily_weather_dag.py`
- [ ] Test: Run manually
- [ ] Schedule: 6 AM daily
- [ ] Monitor: Check logs

### Week 5: ML Experiments

**Day 20-22: Tourism Score**
- [ ] Create `notebooks/05_ml_experiments.ipynb`
- [ ] Calculate tourism suitability score
- [ ] Visualize scores by month/city
- [ ] Export top insights

**Day 23-24: Forecast Accuracy**
- [ ] Compare yesterday's forecast with today's actual
- [ ] Calculate error (MAE, RMSE)
- [ ] Plot: Forecast vs actual scatter

### Week 6: Power BI

**Day 25-26: Data Export**
- [ ] Write `scripts/export_for_powerbi.py`
- [ ] Export CSVs (daily summary, locations, etc.)
- [ ] Test: Open CSV in Excel

**Day 27-28: Dashboard**
- [ ] Open Power BI Desktop
- [ ] Connect to CSVs (or SQLite)
- [ ] Create visualizations
- [ ] Publish dashboard

### Week 7: Polish

**Day 29: Documentation**
- [ ] Update README.md
- [ ] Write `docs/SETUP_GUIDE.md`
- [ ] Document any issues in `docs/TROUBLESHOOTING.md`

**Day 30: Final Testing**
- [ ] Run full pipeline end-to-end
- [ ] Check all DAGs
- [ ] Review all notebooks
- [ ] Git commit everything

---

## 🎯 What to Do RIGHT NOW

1. **Create folders** (5 min)
2. **Create `.gitignore`** (2 min)
3. **Create `requirements.txt`** (2 min)
4. **Set up virtual environment** (5 min)
5. **Create `src/config.py`** with locations (10 min)
6. **Open Jupyter notebook** and make first API call (30 min)

Start with these 6 steps. Once you see weather data in a notebook, you'll be motivated to continue!

---

**Last Updated:** November 15, 2025
**Status:** Planning Complete - Ready to Build!

## Airflow DAGs (recommended)
- `daily_fetch_dag`: run daily -> fetch forecast and current weather for all locations -> validate -> save
- `backfill_historical_dag`: run on demand/weekly -> fetch past_days or start/end ranges for historical backfill
- `ml_train_dag`: scheduled weekly/monthly -> prepare features, train model, store metrics/artifacts
- `report_generation_dag`: scheduled weekly -> produce exports for Power BI and static reports

Airflow tips: run Airflow locally with SQLite executor or use Docker Compose example. Keep logs and raw responses for traceability.

## ML & Analytics Ideas
- Task: Create a "tourism suitability" score combining temperature, precipitation probability, sunshine and wind.
- Nowcasting: short‑term precipitation classifier using the most recent hours + current conditions.
- Forecast correction: train a model to reduce forecast bias for temperature/precipitation per-location.
- Clustering: group locations by seasonal patterns.

## Power BI Integration (free options)
- Power BI Desktop can connect to CSV, Parquet (via DuckDB/ODBC), or SQL Server/Postgres. For a pure free local flow:
  - Export daily/weekly summary CSVs to `data/exports/` and refresh in Power BI.
  - Or run a local Postgres or SQL Server Express instance and let Power BI connect directly.

## Testing & Reproducibility
- Provide `requirements.txt` and an optional `docker-compose.yml` for Airflow + Postgres for reproducible local dev.
- Add unit tests for the API client (mock responses), DB writers, and data validators in `tests/`.
- Include a small sample dataset in `data/sample/` for quick dev and CI tests.

## Privacy, Limits & Costs
- Open‑Meteo public endpoints are free for non-commercial use; check docs for rate limits. No personal data involved.
- Keep API call volume reasonable (cache raw responses, use backfill only when needed).

## Implementation Milestones (Concrete)
1. Project scaffolding and environment (this repo) — deliverables: `requirements.txt`, folder layout, sample notebook. (1–2 days)
2. API exploration notebook and working `api_client.py` for one location — deliverable: notebook, raw JSON sample. (1–2 days)
3. Local storage + simple ingestion DAG — insert hourly and daily into SQLite + Parquet. (2–3 days)
4. EDA notebooks and sample Power BI export — deliverable: EDA report, sample PBI dataset. (2–3 days)
5. ML experiment (tourism suitability or forecast correction) — deliverable: notebook, trained model, metrics. (3–5 days)
6. Packaging: Docker Compose for Airflow & Postgres, README with run instructions. (2–3 days)

## Quick-run Instructions (local)
1. Create virtualenv and install dependencies:
```
python -m venv .venv
.\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
```
2. Run a sample notebook to fetch one location (open `notebooks/01_api_exploration.ipynb`).
3. Start Airflow (optional Docker Compose) to run DAGs locally.

## Deliverables for this repo
- Updated `PROJECT_PLAN.md` (this file)
- `notebooks/01_api_exploration.ipynb` (sample API calls)
- `src/api_client.py`, `src/database.py`, `src/config.py`
- `airflow/dags/daily_weather_dag.py` (initial skeleton)
- `data/sample/` with sample JSON and Parquet
- `requirements.txt`, optional `docker-compose.yml`

## Next Immediate Steps (what I'll do next)
1. Add a sample `notebooks/01_api_exploration.ipynb` to test the Open‑Meteo call for 5 SA locations (Cape Town, Johannesburg, Durban, Port Elizabeth, Kruger). 
2. Implement a minimal `src/api_client.py` and a one-shot script to write raw JSON to `data/raw/`.
3. Create the first Airflow DAG skeleton `airflow/dags/daily_weather_dag.py` to schedule daily ingestion.

---

**Last Updated**: November 15, 2025
**Status**: Planning Phase
**Current Branch**: `main`
