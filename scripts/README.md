Scripts to load medallion layers into SQL Server

Prerequisites
- Windows with ODBC Driver for SQL Server (ODBC Driver 17 or 18) installed
- Python environment with packages in `requirements.txt` installed

Install dependencies (PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run scripts (PowerShell):

```powershell
# Load bronze (raw)
python .\scripts\load_bronze_to_sqlserver.py

# Load silver (features)
python .\scripts\load_silver_to_sqlserver.py

# Aggregate gold (summary)
python .\scripts\aggregate_gold.py
```

Notes
- Scripts use Windows Authentication (Trusted Connection). Ensure your Windows user has permission to create database/tables on `DESKTOP-939GPCA`.
- Parquet input paths used:
  - `data/processed/daily/all_locations_daily.parquet` (bronze)
  - `data/processed/daily/daily_with_features.parquet` (silver)
