# SA Tourism Weather Project - Folder Structure & Step-by-Step Guide

## 📁 Complete Folder Structure

```
SA-Tourism-Weather-Project/
│
├── README.md                          # Project overview, setup instructions
├── PROJECT_PLAN.md                    # Detailed project plan (already created)
├── FOLDER_STRUCTURE.md                # This file - explains what goes where
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Files to exclude from Git
├── docker-compose.yml                 # (Optional) Docker setup for Airflow + Postgres
│
├── data/                              # All data files (add to .gitignore except sample/)
│   ├── raw/                          # Raw JSON responses from API
│   │   └── YYYY-MM-DD/               # Organized by date
│   │       └── location_name_timestamp.json
│   ├── processed/                    # Cleaned Parquet files
│   │   ├── hourly/                   # Hourly weather data
│   │   ├── daily/                    # Daily aggregates
│   │   └── current/                  # Current conditions snapshots
│   ├── exports/                      # CSV/Excel exports for Power BI
│   ├── sample/                       # Sample data for testing (commit this)
│   └── database/                     # SQLite database file(s)
│       └── weather.db
│
├── notebooks/                         # Jupyter notebooks for exploration
│   ├── 01_api_exploration.ipynb      # Test API calls, understand response format
│   ├── 02_eda_initial.ipynb          # Initial data exploration
│   ├── 03_data_quality.ipynb         # Check for missing values, outliers
│   ├── 04_visualization.ipynb        # Create charts and graphs
│   ├── 05_ml_experiments.ipynb       # ML model experiments
│   └── 06_tourism_insights.ipynb     # Tourism-specific analysis
│
├── src/                               # Source code (reusable modules)
│   ├── __init__.py                   # Makes src a Python package
│   ├── config.py                     # Configuration (API URLs, locations, settings)
│   ├── api_client.py                 # Functions to fetch data from Open-Meteo
│   ├── database.py                   # Database connection and operations
│   ├── data_processing.py            # Clean and transform data
│   ├── validators.py                 # Data validation functions
│   └── ml/                           # ML-related code
│       ├── __init__.py
│       ├── features.py               # Feature engineering
│       ├── models.py                 # Model definitions
│       └── train.py                  # Training scripts
│
├── sql/                               # SQL scripts
│   ├── schema.sql                    # Database schema (CREATE TABLE statements)
│   ├── queries/                      # Useful SQL queries
│   │   ├── tourism_insights.sql
│   │   └── data_quality_checks.sql
│   └── migrations/                   # Schema changes over time
│
├── airflow/                           # Airflow orchestration
│   ├── dags/                         # DAG definitions
│   │   ├── daily_weather_dag.py     # Daily data collection
│   │   ├── backfill_historical_dag.py  # Backfill historical data
│   │   ├── ml_training_dag.py       # ML model training/retraining
│   │   └── report_generation_dag.py # Generate reports
│   ├── plugins/                      # Custom Airflow plugins (if needed)
│   └── config/                       # Airflow configuration
│       └── airflow.cfg
│
├── models/                            # Saved ML models
│   └── YYYY-MM-DD/                   # Organized by training date
│       ├── model.pkl
│       └── metrics.json
│
├── reports/                           # Generated reports
│   ├── weekly/
│   └── monthly/
│
├── powerbi/                           # Power BI files
│   ├── SA_Weather_Dashboard.pbix     # Power BI Desktop file
│   └── README.md                     # Instructions for Power BI setup
│
├── scripts/                           # Standalone scripts
│   ├── initial_setup.py              # One-time setup script
│   ├── backfill_data.py              # Manual backfill script
│   └── export_for_powerbi.py         # Export data for Power BI
│
├── tests/                             # Unit tests
│   ├── __init__.py
│   ├── test_api_client.py
│   ├── test_database.py
│   ├── test_validators.py
│   └── fixtures/                     # Test data
│       └── sample_api_response.json
│
└── docs/                              # Additional documentation
    ├── API_GUIDE.md                  # Open-Meteo API usage guide
    ├── SETUP_GUIDE.md                # Detailed setup instructions
    └── TROUBLESHOOTING.md            # Common issues and solutions
```

---

## 🎯 Step-by-Step Implementation Plan

### **PHASE 1: Project Setup (Week 1)**

#### Step 1.1: Create Folder Structure
**What to do:**
```powershell
# Run these commands in PowerShell to create all folders
mkdir data\raw, data\processed\hourly, data\processed\daily, data\processed\current, data\exports, data\sample, data\database
mkdir notebooks, src\ml, sql\queries, sql\migrations
mkdir airflow\dags, airflow\plugins, airflow\config
mkdir models, reports\weekly, reports\monthly
mkdir powerbi, scripts, tests\fixtures, docs
```

**Deliverable:** All folders created ✅

---

#### Step 1.2: Create `.gitignore`
**What to do:** Create a `.gitignore` file to exclude data files and sensitive info.

**File content:**
```
# Virtual environment
.venv/
venv/
env/

# Data files (except sample)
data/raw/
data/processed/
data/database/
data/exports/
!data/sample/

# Airflow
airflow/logs/
airflow/*.db
airflow/*.pid

# Python
__pycache__/
*.py[cod]
*.so
*.egg-info/
dist/
build/

# Jupyter
.ipynb_checkpoints/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Models (large files)
models/*
!models/.gitkeep

# Reports
reports/*
!reports/.gitkeep

# Power BI temp files
*.pbix.tmp
```

**Deliverable:** `.gitignore` created ✅

---

#### Step 1.3: Create `requirements.txt`
**What to do:** List all Python packages you'll need.

**File content:**
```
# Core dependencies
requests>=2.31.0
pandas>=2.0.0
numpy>=1.24.0

# Data storage
pyarrow>=12.0.0          # For Parquet files
sqlalchemy>=2.0.0        # Database ORM

# Jupyter and visualization
jupyter>=1.0.0
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.14.0

# Machine Learning
scikit-learn>=1.3.0
xgboost>=1.7.0           # Optional: powerful ML library

# Airflow (install separately or via Docker)
# apache-airflow==2.7.0  # Uncomment if installing locally

# Testing
pytest>=7.4.0
pytest-cov>=4.1.0

# Utilities
python-dotenv>=1.0.0     # For environment variables
tqdm>=4.65.0             # Progress bars
```

**Deliverable:** `requirements.txt` created ✅

---

#### Step 1.4: Set Up Virtual Environment
**What to do:**
```powershell
# Create virtual environment
python -m venv .venv

# Activate it
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

**Deliverable:** Virtual environment ready ✅

---

### **PHASE 2: API Exploration (Week 1-2)**

#### Step 2.1: Define South African Locations
**What to do:** Create `src/config.py` with location data.

**File content example:**
```python
# src/config.py

# South African tourist destinations
LOCATIONS = {
    "cape_town": {
        "name": "Cape Town",
        "latitude": -33.9249,
        "longitude": 18.4241,
        "region": "Western Cape",
        "description": "Popular tourist destination, Table Mountain"
    },
    "johannesburg": {
        "name": "Johannesburg",
        "latitude": -26.2041,
        "longitude": 28.0473,
        "region": "Gauteng",
        "description": "Largest city, business hub"
    },
    "durban": {
        "name": "Durban",
        "latitude": -29.8587,
        "longitude": 31.0218,
        "region": "KwaZulu-Natal",
        "description": "Beach destination, warm weather"
    },
    "kruger_park": {
        "name": "Kruger National Park",
        "latitude": -23.9884,
        "longitude": 31.5547,
        "region": "Mpumalanga/Limpopo",
        "description": "Safari destination"
    },
    "port_elizabeth": {
        "name": "Port Elizabeth (Gqeberha)",
        "latitude": -33.9608,
        "longitude": 25.6022,
        "region": "Eastern Cape",
        "description": "Garden Route gateway"
    }
}

# API settings
API_BASE_URL = "https://api.open-meteo.com/v1/forecast"

# Weather variables to collect
HOURLY_VARS = [
    "temperature_2m",
    "relative_humidity_2m",
    "precipitation",
    "weather_code",
    "wind_speed_10m",
    "wind_direction_10m",
    "cloud_cover"
]

DAILY_VARS = [
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "weather_code",
    "sunrise",
    "sunset",
    "sunshine_duration",
    "uv_index_max"
]
```

**Deliverable:** `src/config.py` with locations ✅

---

#### Step 2.2: Create API Client
**What to do:** Build `src/api_client.py` to fetch data.

**What it should do:**
- Make HTTP requests to Open-Meteo API
- Handle errors and retries
- Save raw JSON responses
- Return parsed data

**Deliverable:** Working `src/api_client.py` ✅

---

#### Step 2.3: Create Exploration Notebook
**What to do:** Create `notebooks/01_api_exploration.ipynb`.

**What to explore:**
1. Test API call for one location
2. Understand JSON response structure
3. Check available variables
4. Test different time ranges (past_days, forecast_days)
5. Visualize sample data (temperature over 7 days)

**Deliverable:** Notebook with successful API calls ✅

---

### **PHASE 3: Database Setup (Week 2)**

#### Step 3.1: Design Database Schema
**What to do:** Create `sql/schema.sql`.

**Tables to create:**
- `locations` - Store city information
- `weather_hourly` - Hourly weather data
- `weather_daily` - Daily aggregates
- `ingestion_log` - Track when data was collected

**Deliverable:** `sql/schema.sql` ✅

---

#### Step 3.2: Create Database Module
**What to do:** Build `src/database.py`.

**Functions needed:**
- `create_connection()` - Connect to SQLite
- `init_database()` - Create tables
- `insert_hourly_data()` - Insert hourly weather
- `insert_daily_data()` - Insert daily weather
- `get_latest_data()` - Query recent data

**Deliverable:** `src/database.py` ✅

---

#### Step 3.3: Initial Data Collection
**What to do:** Create `scripts/initial_setup.py`.

**Script should:**
1. Create database
2. Insert locations
3. Fetch last 30 days of data for all locations
4. Store in database and Parquet files

**Deliverable:** Database with initial data ✅

---

### **PHASE 4: Data Processing (Week 3)**

#### Step 4.1: Create Data Processing Module
**What to do:** Build `src/data_processing.py`.

**Functions:**
- Clean missing values
- Convert units if needed
- Add derived columns (e.g., feels_like temperature)
- Save to Parquet format

**Deliverable:** `src/data_processing.py` ✅

---

#### Step 4.2: Data Quality Checks
**What to do:** Create `notebooks/03_data_quality.ipynb`.

**Check for:**
- Missing values
- Duplicate timestamps
- Outliers (impossible temperatures)
- Data gaps

**Deliverable:** Data quality report ✅

---

### **PHASE 5: Exploratory Data Analysis (Week 3-4)**

#### Step 5.1: EDA Notebook
**What to do:** Create `notebooks/02_eda_initial.ipynb`.

**Analyze:**
- Temperature trends by city
- Precipitation patterns
- Seasonal variations
- Compare forecast vs actual (if you have historical data)

**Deliverable:** EDA notebook with insights ✅

---

#### Step 5.2: Visualization Notebook
**What to do:** Create `notebooks/04_visualization.ipynb`.

**Create:**
- Time series plots (temperature, rainfall)
- Comparison charts (5 cities side-by-side)
- Heatmaps (weather patterns by month)
- Interactive Plotly charts

**Deliverable:** Visualization notebook ✅

---

### **PHASE 6: Airflow Setup (Week 4-5)**

#### Step 6.1: Install Airflow
**What to do:**
```powershell
# Option 1: Local installation
pip install apache-airflow==2.7.0

# Option 2: Docker (recommended)
# Use docker-compose.yml
```

**Deliverable:** Airflow running locally ✅

---

#### Step 6.2: Create Daily Collection DAG
**What to do:** Build `airflow/dags/daily_weather_dag.py`.

**DAG tasks:**
1. Fetch current + 7-day forecast for all locations
2. Validate data
3. Save to database
4. Save to Parquet
5. Send success/failure notification

**Schedule:** Daily at 6:00 AM

**Deliverable:** Working DAG ✅

---

#### Step 6.3: Create Backfill DAG
**What to do:** Build `airflow/dags/backfill_historical_dag.py`.

**Purpose:** Manually trigger to fetch historical data

**Deliverable:** Backfill DAG ✅

---

### **PHASE 7: Machine Learning (Week 5-6)**

#### Step 7.1: Feature Engineering
**What to do:** Create `src/ml/features.py`.

**Features to create:**
- Rolling averages (7-day, 30-day temp)
- Precipitation indicators
- Season encoding
- Tourism suitability score

**Deliverable:** Feature engineering module ✅

---

#### Step 7.2: ML Experiments
**What to do:** Create `notebooks/05_ml_experiments.ipynb`.

**Experiments:**
1. Predict tomorrow's temperature (regression)
2. Classify weather conditions (classification)
3. Tourism suitability score (custom metric)

**Deliverable:** Trained models with metrics ✅

---

### **PHASE 8: Power BI Dashboard (Week 6-7)**

#### Step 8.1: Export Data for Power BI
**What to do:** Create `scripts/export_for_powerbi.py`.

**Export:**
- Daily weather summary CSV
- Location lookup table
- Recent 90 days of data

**Deliverable:** CSV files in `data/exports/` ✅

---

#### Step 8.2: Create Power BI Dashboard
**What to do:** Build `powerbi/SA_Weather_Dashboard.pbix`.

**Visuals:**
- Temperature trends by city
- Precipitation calendar
- Best months for tourism
- 7-day forecast cards

**Deliverable:** Power BI dashboard ✅

---

### **PHASE 9: Testing & Documentation (Week 7)**

#### Step 9.1: Write Tests
**What to do:** Create tests in `tests/` folder.

**Test files:**
- `test_api_client.py` - Mock API responses
- `test_database.py` - Database operations
- `test_validators.py` - Data validation

**Run tests:**
```powershell
pytest tests/
```

**Deliverable:** Test suite passing ✅

---

#### Step 9.2: Update Documentation
**What to do:**
- Update `README.md` with setup instructions
- Create `docs/SETUP_GUIDE.md` with detailed steps
- Document any issues in `docs/TROUBLESHOOTING.md`

**Deliverable:** Complete documentation ✅

---

## 🎯 Your Next Immediate Actions

### **RIGHT NOW - Do These First:**

1. **Create folder structure** (5 minutes)
   ```powershell
   # Copy the mkdir commands from Step 1.1 above
   ```

2. **Create `.gitignore`** (2 minutes)
   - Copy content from Step 1.2

3. **Create `requirements.txt`** (2 minutes)
   - Copy content from Step 1.3

4. **Set up virtual environment** (5 minutes)
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

5. **Create `src/config.py`** (10 minutes)
   - Copy locations from Step 2.1
   - Customize if you want different cities

6. **Start exploration notebook** (30 minutes)
   - Create `notebooks/01_api_exploration.ipynb`
   - Make your first API call
   - See real data!

---

## 📊 Progress Tracking

As you complete each step, mark it done:

- [ ] Phase 1: Project Setup
  - [ ] Folders created
  - [ ] `.gitignore` created
  - [ ] `requirements.txt` created
  - [ ] Virtual environment set up

- [ ] Phase 2: API Exploration
  - [ ] `src/config.py` created
  - [ ] `src/api_client.py` created
  - [ ] Exploration notebook working

- [ ] Phase 3: Database Setup
  - [ ] Schema designed
  - [ ] Database module created
  - [ ] Initial data collected

- [ ] Phase 4: Data Processing
  - [ ] Processing module created
  - [ ] Data quality checks done

- [ ] Phase 5: EDA
  - [ ] EDA notebook completed
  - [ ] Visualizations created

- [ ] Phase 6: Airflow
  - [ ] Airflow installed
  - [ ] Daily DAG created
  - [ ] Backfill DAG created

- [ ] Phase 7: ML
  - [ ] Features engineered
  - [ ] Models trained

- [ ] Phase 8: Power BI
  - [ ] Data exported
  - [ ] Dashboard created

- [ ] Phase 9: Testing & Docs
  - [ ] Tests written
  - [ ] Documentation complete

---

## 💡 Tips for Success

1. **Start small**: Don't try to do everything at once. Complete Phase 1 fully before moving to Phase 2.

2. **Test as you go**: After creating each module, test it immediately in a notebook.

3. **Commit often**: Use Git to save progress after each completed step.

4. **Ask questions**: If something doesn't work, troubleshoot step-by-step.

5. **Keep notes**: Document issues and solutions in `docs/TROUBLESHOOTING.md`.

6. **Celebrate wins**: Each working component is an achievement!

---

**Last Updated:** November 15, 2025
