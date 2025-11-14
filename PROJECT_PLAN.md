# SA Tourism Weather Project - Planning Document

## 🎯 Project Goal
Build a complete data pipeline to collect, store, analyze, and visualize weather data from South Africa for tourism insights using Open-Meteo API.

## 🛠️ Tech Stack
- **Data Collection**: Python (requests/httpx)
- **Storage**: SQL Database (SQLite initially, can migrate to PostgreSQL)
- **Notebooks**: Jupyter for exploration and analysis
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Machine Learning**: Scikit-learn, possibly TensorFlow/PyTorch
- **Orchestration**: Apache Airflow (for automated data pipelines)

## 📊 Data Source: Open-Meteo API

### Two Main API Options:

#### 1. **Historical Forecast API** (2022 onwards)
- **Best for**: Recent high-resolution data, machine learning training
- **Resolution**: High (1-11 km depending on model)
- **Availability**: Past 2-5 years
- **Use case**: Training ML models, accurate recent weather analysis

#### 2. **Weather Forecast API** (Current + 7-16 days ahead)
- **Best for**: Real-time predictions, current conditions
- **Availability**: Current + up to 16 days forecast
- **Past days**: Can access up to 92 days in the past
- **Use case**: Live monitoring, prediction validation

## 🗂️ Step-by-Step Development Plan

### Phase 1: Project Setup & Initial Data Exploration ✅
- [x] Initialize Git repository
- [x] Create dev branch
- [ ] Set up project structure (folders)
- [ ] Create requirements.txt
- [ ] Initial notebook for API exploration

### Phase 2: Define Data Strategy
**Decision Points:**
1. **Which locations in South Africa?**
   - Major cities? (Cape Town, Johannesburg, Durban, etc.)
   - Tourist destinations? (Kruger Park, Garden Route, etc.)
   - Multiple regions for comparison?

2. **Which weather variables to collect?**
   - **Essential for Tourism:**
     - Temperature (min/max/mean)
     - Precipitation (rain sum)
     - Weather code (general conditions)
     - Sunshine duration
     - UV Index
   - **Advanced:**
     - Wind speed/direction
     - Humidity
     - Cloud cover
     - Visibility

3. **Time range:**
   - Historical: How far back? (2022-present available)
   - Forecast: Daily updates for next 7-16 days?

4. **Data granularity:**
   - Hourly data?
   - Daily aggregates?
   - Both?

### Phase 3: Database Design
**Database Schema Planning:**
- Locations table (SA cities/regions)
- Historical weather data table
- Forecast data table
- Weather codes lookup table
- Metadata/audit table (when data was collected)

**Questions to decide:**
- SQLite (simple, local) vs PostgreSQL (production-ready)?
- How to handle updates and duplicates?
- Indexing strategy for performance?

### Phase 4: Data Collection Pipeline
**Components to build:**
1. **API Client Module**
   - Function to fetch historical data
   - Function to fetch forecast data
   - Error handling and retry logic
   - Rate limiting (max 10,000 calls/day for free tier)

2. **Data Validation**
   - Check for missing values
   - Validate data types
   - Check coordinate accuracy

3. **Storage Module**
   - Insert data into database
   - Handle duplicates
   - Update existing records

### Phase 5: Data Analysis & Exploration
**Jupyter Notebooks:**
1. **EDA (Exploratory Data Analysis)**
   - Temperature trends over time
   - Seasonal patterns
   - Precipitation patterns
   - Correlation analysis

2. **Tourism Insights**
   - Best months for tourism (weather-wise)
   - Regional comparisons
   - Weather reliability by season
   - Extreme weather events

### Phase 6: Visualization Dashboard
**Potential visualizations:**
- Time series plots (temperature, rainfall)
- Heatmaps (weather patterns by month/region)
- Comparison charts (different cities)
- Weather distribution plots
- Interactive maps (Plotly/Folium)

### Phase 7: Machine Learning
**Potential ML Tasks:**
1. **Forecast Enhancement**
   - Improve API forecasts using historical patterns
   - Ensemble models combining multiple forecasts

2. **Prediction Models**
   - Predict tourism suitability scores
   - Classify weather conditions
   - Anomaly detection (unusual weather)

3. **Time Series Forecasting**
   - ARIMA, LSTM for weather prediction
   - Compare with API forecasts

### Phase 8: Airflow Orchestration
**DAGs to create:**
1. **Daily Data Collection DAG**
   - Fetch latest forecast data
   - Store in database
   - Run data quality checks
   - Send alerts on failures

2. **Weekly Historical Update DAG**
   - Backfill recent historical data
   - Validate forecast accuracy
   - Update ML models

3. **Monthly Analysis DAG**
   - Generate reports
   - Update visualizations
   - Archive old data

## 📁 Proposed Project Structure
```
SA-Tourism-Weather-Project/
├── data/
│   ├── raw/              # Raw API responses (optional backup)
│   ├── processed/        # Cleaned data
│   └── database/         # SQLite database file
├── notebooks/
│   ├── 01_api_exploration.ipynb
│   ├── 02_data_collection.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_visualization.ipynb
│   └── 05_ml_experiments.ipynb
├── src/
│   ├── __init__.py
│   ├── api_client.py     # API interaction functions
│   ├── database.py       # Database operations
│   ├── config.py         # Configuration settings
│   └── utils.py          # Helper functions
├── sql/
│   └── schema.sql        # Database schema
├── airflow/
│   └── dags/
│       ├── daily_weather_dag.py
│       └── analysis_dag.py
├── tests/
│   └── test_api_client.py
├── .gitignore
├── README.md
├── PROJECT_PLAN.md       # This file
└── requirements.txt
```

## ❓ Questions to Answer Before Starting

### Immediate Decisions Needed:
1. **Locations**: Which SA cities/regions to track?
   - Suggestion: Start with 5-10 major tourist destinations

2. **Historical vs Current**: Which API to start with?
   - Suggestion: Start with Historical Forecast API (2022-present) to build initial dataset

3. **Data frequency**: How often to collect?
   - Suggestion: Daily collection for forecasts, one-time backfill for historical

4. **Variables priority**: Which weather variables first?
   - Suggestion: Start with basics (temp, precipitation, weather_code, sunshine)

5. **Database choice**: SQLite or PostgreSQL?
   - Suggestion: Start with SQLite, migrate to PostgreSQL if needed

## 🎯 Next Steps
1. **Create GitHub Issue**: "Setup project structure and development environment"
2. **Build project folder structure**
3. **Create initial exploration notebook** to test API calls
4. **Define SA tourism locations** (cities/coordinates)
5. **Design database schema**

---

## 📝 Notes & Ideas
- Consider adding tourism data later (visitor numbers, hotel bookings) to correlate with weather
- Could expand to predict "tourism suitability index" based on weather
- Potential to compare forecast accuracy across different models
- Real-time dashboard could be valuable for tourism operators

---

**Last Updated**: November 14, 2025
**Status**: Planning Phase
**Current Branch**: `dev/initial-planning`
