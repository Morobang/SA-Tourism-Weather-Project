# Variable Selection Review - Based on Official API Metadata

**Date:** November 16, 2025  
**Reviewed Against:** Open-Meteo Archive API Official Documentation

---

## 📋 Comparison: What We're Fetching vs What's Available

### ✅ Hourly Variables - GOOD COVERAGE

**We're currently fetching (29 variables):**
```
temperature_2m ✓
relative_humidity_2m ✓
dew_point_2m ✓
apparent_temperature ✓
precipitation ✓
rain ✓
snowfall ✓
snow_depth ✓
weather_code ✓
pressure_msl ✓
surface_pressure ✓
cloud_cover ✓
cloud_cover_low ✓
cloud_cover_mid ✓
cloud_cover_high ✓
et0_fao_evapotranspiration ✓
vapour_pressure_deficit ✓
wind_gusts_10m ✓
wind_direction_10m ✓
wind_direction_100m ✓
wind_speed_10m ✓
wind_speed_100m ✓
soil_temperature_0_to_7cm ✓
soil_temperature_7_to_28cm ✓
soil_temperature_28_to_100cm ✓
soil_temperature_100_to_255cm ✓
soil_moisture_0_to_7cm ✓
soil_moisture_7_to_28cm ✓
soil_moisture_28_to_100cm ✓
soil_moisture_100_to_255cm ✓ (but API shows 255cm, we have it!)
```

**🚨 MISSING from our fetch (but available in API):**
1. `shortwave_radiation` - **SHOULD ADD!** (solar radiation, tourism-relevant)
2. `direct_radiation` - Optional (advanced solar metric)
3. `direct_normal_irradiance` - Optional (advanced solar metric)
4. `diffuse_radiation` - Optional (advanced solar metric)
5. `global_tilted_irradiance` - Not needed (for solar panels)
6. `sunshine_duration` - **SHOULD ADD!** (very important for tourism!)

**API Note:** We're using soil depth ranges 0-7, 7-28, 28-100, 100-255cm but these don't match API exactly (API has 0_to_7cm etc). Need to verify exact variable names.

---

### ⚠️ Daily Variables - SOME ISSUES

**We're currently fetching (54 variables):**

**Good variables we're fetching:**
```
weather_code ✓
temperature_2m_max ✓
temperature_2m_min ✓
apparent_temperature_max ✓
apparent_temperature_min ✓
sunrise ✓
sunset ✓
sunshine_duration ✓
daylight_duration ✓
precipitation_sum ✓
rain_sum ✓
snowfall_sum ✓
precipitation_hours ✓
wind_speed_10m_max ✓
wind_gusts_10m_max ✓
wind_direction_10m_dominant ✓
shortwave_radiation_sum ✓
et0_fao_evapotranspiration ✓
```

**❌ PROBLEMS - Variables we're fetching but DON'T exist in API:**

These are NOT in the official API documentation:
1. `temperature_2m_mean` - **NOT AVAILABLE** (API only has max/min)
2. `apparent_temperature_mean` - **NOT AVAILABLE** (API only has max/min)
3. `cloud_cover_mean` - **NOT AVAILABLE**
4. `cloud_cover_max` - **NOT AVAILABLE**
5. `cloud_cover_min` - **NOT AVAILABLE**
6. `dew_point_2m_mean` - **NOT AVAILABLE**
7. `dew_point_2m_max` - **NOT AVAILABLE**
8. `dew_point_2m_min` - **NOT AVAILABLE**
9. `pressure_msl_mean` - **NOT AVAILABLE**
10. `pressure_msl_max` - **NOT AVAILABLE**
11. `pressure_msl_min` - **NOT AVAILABLE**
12. `surface_pressure_mean` - **NOT AVAILABLE**
13. `surface_pressure_max` - **NOT AVAILABLE**
14. `surface_pressure_min` - **NOT AVAILABLE**
15. `relative_humidity_2m_mean` - **NOT AVAILABLE**
16. `relative_humidity_2m_max` - **NOT AVAILABLE**
17. `relative_humidity_2m_min` - **NOT AVAILABLE**
18. `wind_speed_10m_mean` - **NOT AVAILABLE**
19. `wind_speed_10m_min` - **NOT AVAILABLE**
20. `wind_gusts_10m_mean` - **NOT AVAILABLE**
21. `wind_gusts_10m_min` - **NOT AVAILABLE**
22. `winddirection_10m_dominant` - DUPLICATE (we have `wind_direction_10m_dominant`)
23. `wet_bulb_temperature_2m_*` - **NOT AVAILABLE**
24. `vapour_pressure_deficit_max` - **NOT AVAILABLE**
25. `snowfall_water_equivalent_sum` - **NOT AVAILABLE**
26. `et0_fao_evapotranspiration_sum` - DUPLICATE (same as `et0_fao_evapotranspiration`)
27. All `soil_*` variables - **NOT AVAILABLE in DAILY** (only hourly!)

---

## 🔧 Recommended Fixes

### For Hourly Variables - ADD THESE:

```python
HOURLY_VARIABLES = [
    # ... existing variables ...
    
    # ADD THESE TOURISM-RELEVANT VARIABLES:
    "shortwave_radiation",      # Solar radiation (affects heat, UV, comfort)
    "sunshine_duration",         # Hours of sunshine per hour (very important!)
]
```

### For Daily Variables - REMOVE INVALID ONES:

The API documentation shows **ONLY** these daily variables are available:

```python
DAILY_VARIABLES = [
    # Weather
    "weather_code",
    
    # Temperature (ONLY max/min, NO mean!)
    "temperature_2m_max",
    "temperature_2m_min",
    
    # Apparent temperature (ONLY max/min, NO mean!)
    "apparent_temperature_max",
    "apparent_temperature_min",
    
    # Precipitation
    "precipitation_sum",
    "rain_sum",
    "snowfall_sum",
    "precipitation_hours",
    
    # Sun/Daylight
    "sunrise",
    "sunset",
    "sunshine_duration",
    "daylight_duration",
    
    # Wind
    "wind_speed_10m_max",
    "wind_gusts_10m_max",
    "wind_direction_10m_dominant",
    
    # Solar
    "shortwave_radiation_sum",
    
    # Evapotranspiration
    "et0_fao_evapotranspiration",
]
```

**This is only 18 variables, not 54!**

---

## 🎯 Updated Variable Selection for Tourism

### Hourly Variables (Tourism Focus) - 21 variables

```python
HOURLY_VARIABLES_TOURISM = [
    # Temperature & Comfort (5)
    "temperature_2m",
    "relative_humidity_2m",
    "dew_point_2m",
    "apparent_temperature",
    "vapour_pressure_deficit",
    
    # Precipitation (3)
    "precipitation",
    "rain",
    "weather_code",
    
    # Wind (3)
    "wind_speed_10m",
    "wind_direction_10m",
    "wind_gusts_10m",
    
    # Pressure (2)
    "pressure_msl",
    "surface_pressure",
    
    # Cloud & Sun (4)
    "cloud_cover",
    "shortwave_radiation",    # ADD THIS!
    "sunshine_duration",      # ADD THIS!
    
    # Evapotranspiration (1)
    "et0_fao_evapotranspiration",
]
```

### Daily Variables (Tourism Focus) - 18 variables

```python
DAILY_VARIABLES_TOURISM = [
    # Weather
    "weather_code",
    
    # Temperature
    "temperature_2m_max",
    "temperature_2m_min",
    
    # Apparent Temperature
    "apparent_temperature_max",
    "apparent_temperature_min",
    
    # Precipitation
    "precipitation_sum",
    "rain_sum",
    "precipitation_hours",
    
    # Sun & Daylight
    "sunrise",
    "sunset",
    "sunshine_duration",
    "daylight_duration",
    
    # Wind
    "wind_speed_10m_max",
    "wind_gusts_10m_max",
    "wind_direction_10m_dominant",
    
    # Solar
    "shortwave_radiation_sum",
    
    # Evapotranspiration
    "et0_fao_evapotranspiration",
]
```

---

## 📊 Impact Analysis

### What This Means for Your Data:

**Current Situation:**
- ✅ Hourly: 263,160 records with 29 variables (mostly valid)
- ⚠️ Daily: 10,965 records with 54 variables (36 are INVALID!)

**After Fix:**
- ✅ Hourly: Will have 21 variables (8 removed, but mostly soil/snow)
- ✅ Daily: Will have 18 variables (36 invalid ones won't be fetched)
- ⚠️ **You'll need to re-fetch data with corrected variable lists!**

### What's in Your Current Data:

Your current Parquet files likely have:
1. **Hourly:** Missing `sunshine_duration` and `shortwave_radiation`
2. **Daily:** Have invalid columns with all NULL/NaN values (the 36 variables that don't exist)

---

## ✅ Action Items

1. **Update `fetch_historical_batches.py`:**
   - Add `sunshine_duration` and `shortwave_radiation` to HOURLY_VARIABLES
   - Remove all invalid variables from DAILY_VARIABLES

2. **Re-fetch data:**
   - Batch 1 (2020-2021): Re-fetch with corrected variables
   - Batch 2 (2022-2023): Fetch with corrected variables
   - Batch 3 (2024): Fetch with corrected variables

3. **Update variable selection notebooks:**
   - Remove references to non-existent daily variables
   - Add `sunshine_duration` and `shortwave_radiation` to hourly selection

4. **Update documentation:**
   - Correct VARIABLE_SELECTION_RATIONALE.md
   - Remove references to mean/min/max daily aggregations that don't exist

---

## 🤔 Why Were Invalid Variables in the List?

Likely reasons:
1. Variables were from a different API endpoint (ERA5, ECMWF)
2. Variables were from Forecast API (different from Archive API)
3. Confusion between what's calculated vs what's available
4. Old API documentation that's since changed

**The official API docs are the source of truth!**
