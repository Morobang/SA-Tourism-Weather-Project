"""
Configuration settings for the SA Tourism Weather Project.
Contains locations, API settings, and variable definitions.
"""

import os
from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# ==============================================================================
# SOUTH AFRICAN LOCATIONS (15 Major Cities & Tourism Destinations)
# ==============================================================================
# 
# WHY THESE FIELDS?
# -----------------
# - name: Human-readable city name (for reports, dashboards)
# - latitude/longitude: Required by Open-Meteo API to get weather data
# - region: Group cities by province for regional analysis
# - timezone: Ensures timestamps are in local time (not UTC)
# - elevation: API uses this for temperature adjustments (higher = cooler)
# - description: Context for tourism analysis and reporting
#
# DATA ENGINEERING NOTE:
# We store this in config so ANY script/notebook can use the same coordinates.
# If coordinates change, we update once here, not in 10 different places!
#
LOCATIONS = {
    "cape_town": {
        "name": "Cape Town",
        "latitude": -33.9249,
        "longitude": 18.4241,
        "region": "Western Cape",
        "timezone": "Africa/Johannesburg",
        "elevation": 25,
        "description": "Mother City, Table Mountain, beaches, wine lands gateway"
    },
    "johannesburg": {
        "name": "Johannesburg",
        "latitude": -26.2041,
        "longitude": 28.0473,
        "region": "Gauteng",
        "timezone": "Africa/Johannesburg",
        "elevation": 1753,
        "description": "Economic hub, gateway city, Soweto, apartheid museums"
    },
    "durban": {
        "name": "Durban",
        "latitude": -29.8587,
        "longitude": 31.0218,
        "region": "KwaZulu-Natal",
        "timezone": "Africa/Johannesburg",
        "elevation": 5,
        "description": "Subtropical beach city, Indian Ocean, uShaka Marine World"
    },
    "pretoria": {
        "name": "Pretoria",
        "latitude": -25.7479,
        "longitude": 28.2293,
        "region": "Gauteng",
        "timezone": "Africa/Johannesburg",
        "elevation": 1339,
        "description": "Administrative capital, Jacaranda City, Union Buildings"
    },
    "port_elizabeth": {
        "name": "Port Elizabeth (Gqeberha)",
        "latitude": -33.9608,
        "longitude": 25.6022,
        "region": "Eastern Cape",
        "timezone": "Africa/Johannesburg",
        "elevation": 60,
        "description": "Garden Route, beaches, Addo Elephant Park gateway"
    },
    "bloemfontein": {
        "name": "Bloemfontein",
        "latitude": -29.1211,
        "longitude": 26.2142,
        "region": "Free State",
        "timezone": "Africa/Johannesburg",
        "elevation": 1395,
        "description": "Judicial capital, City of Roses, central location"
    },
    "east_london": {
        "name": "East London",
        "latitude": -33.0153,
        "longitude": 27.9116,
        "region": "Eastern Cape",
        "timezone": "Africa/Johannesburg",
        "elevation": 20,
        "description": "Coastal city, surfing, Wild Coast gateway"
    },
    "pietermaritzburg": {
        "name": "Pietermaritzburg",
        "latitude": -29.6006,
        "longitude": 30.3794,
        "region": "KwaZulu-Natal",
        "timezone": "Africa/Johannesburg",
        "elevation": 687,
        "description": "Capital of KZN, Victorian architecture, Midlands Meander"
    },
    "polokwane": {
        "name": "Polokwane",
        "latitude": -23.9045,
        "longitude": 29.4689,
        "region": "Limpopo",
        "timezone": "Africa/Johannesburg",
        "elevation": 1310,
        "description": "Capital of Limpopo, gateway to Kruger North"
    },
    "nelspruit": {
        "name": "Nelspruit (Mbombela)",
        "latitude": -25.4753,
        "longitude": 30.9694,
        "region": "Mpumalanga",
        "timezone": "Africa/Johannesburg",
        "elevation": 660,
        "description": "Lowveld capital, Kruger Park gateway, subtropical climate"
    },
    "stellenbosch": {
        "name": "Stellenbosch",
        "latitude": -33.9321,
        "longitude": 18.8602,
        "region": "Western Cape",
        "timezone": "Africa/Johannesburg",
        "elevation": 136,
        "description": "Wine capital, Cape Dutch architecture, student town"
    },
    "franschhoek": {
        "name": "Franschhoek",
        "latitude": -33.9175,
        "longitude": 19.1252,
        "region": "Western Cape",
        "timezone": "Africa/Johannesburg",
        "elevation": 280,
        "description": "Gourmet capital, wine valley, French heritage"
    },
    "paarl": {
        "name": "Paarl",
        "latitude": -33.7341,
        "longitude": 18.9661,
        "region": "Western Cape",
        "timezone": "Africa/Johannesburg",
        "elevation": 120,
        "description": "Wine route, Afrikaans language monument, granite rock"
    },
    "knysna": {
        "name": "Knysna",
        "latitude": -34.0363,
        "longitude": 23.0471,
        "region": "Western Cape",
        "timezone": "Africa/Johannesburg",
        "elevation": 20,
        "description": "Garden Route, lagoon, Knysna Heads, oysters"
    },
    "hermanus": {
        "name": "Hermanus",
        "latitude": -34.4187,
        "longitude": 19.2345,
        "region": "Western Cape",
        "timezone": "Africa/Johannesburg",
        "elevation": 10,
        "description": "Whale watching capital, coastal walks, wine region"
    }
}

# ==============================================================================
# OPEN-METEO API SETTINGS
# ==============================================================================

API_BASE_URL = "https://api.open-meteo.com/v1/forecast"
API_TIMEOUT = 30  # seconds
API_RETRY_COUNT = 3
API_RETRY_DELAY = 5  # seconds


# ==============================================================================
# DATA PATHS
# ==============================================================================

# Raw data (JSON responses from API)
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
RAW_HISTORICAL_DIR = RAW_DATA_DIR / "historical"
RAW_FORECAST_DIR = RAW_DATA_DIR / "forecast"
RAW_CURRENT_DIR = RAW_DATA_DIR / "current"

# Processed data (Parquet files)
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
PROCESSED_HOURLY_DIR = PROCESSED_DATA_DIR / "hourly"
PROCESSED_DAILY_DIR = PROCESSED_DATA_DIR / "daily"
PROCESSED_CURRENT_DIR = PROCESSED_DATA_DIR / "current"

# Database
DATABASE_DIR = PROJECT_ROOT / "data" / "database"
DATABASE_PATH = DATABASE_DIR / "weather.db"

# Exports (for Power BI, etc.)
EXPORTS_DIR = PROJECT_ROOT / "data" / "exports"

# Sample data
SAMPLE_DATA_DIR = PROJECT_ROOT / "data" / "sample"

# ==============================================================================
# DATE RANGES
# ==============================================================================
#
# API RATE LIMIT CONSIDERATIONS:
# - Free tier: 10,000 calls/day, 5,000/hour, 600/minute
# - 1 year of data (all variables, 1 location) ≈ 260 equivalent calls
# - 5 years for 15 locations ≈ 19,500 calls (requires batching over multiple days)
#
# RECOMMENDED STRATEGY: Fetch by year, one year per day
# Day 1: 2020 for all 15 locations (~3,900 calls)
# Day 2: 2021 for all 15 locations (~3,900 calls)
# Day 3: 2022 for all 15 locations (~3,900 calls)
# Day 4: 2023 for all 15 locations (~3,900 calls)
# Day 5: 2024 for all 15 locations (~3,600 calls)
#
# ==============================================================================

