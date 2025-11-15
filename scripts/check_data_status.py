"""
Data Collection Status Checker

Checks which historical weather data has been collected and what's still missing.
Shows file sizes and record counts for each location.
"""

import sys
from pathlib import Path
import pandas as pd

# Project paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from config import LOCATIONS

# Data directories
historical_dir = project_root / "data" / "raw" / "historical"
hourly_dir = historical_dir / "hourly"
daily_dir = historical_dir / "daily"

def get_file_info(filepath):
    """Get record count and file size for a CSV file."""
    if not filepath.exists():
        return None, None
    
    try:
        df = pd.read_csv(filepath)
        records = len(df)
        size_mb = filepath.stat().st_size / (1024 * 1024)
        return records, size_mb
    except Exception as e:
        return "ERROR", 0


def check_data_coverage():
    """Check what data has been collected for each location."""
    
    print("\n" + "="*80)
    print("📊 SA TOURISM WEATHER PROJECT - DATA COLLECTION STATUS")
    print("="*80)
    print(f"\nChecking: {historical_dir}\n")
    
    # Table header
    print(f"{'Location':<25} {'Hourly Records':<20} {'Daily Records':<20} {'Status':<10}")
    print("-" * 80)
    
    total_hourly = 0
    total_daily = 0
    complete_locations = []
    partial_locations = []
    missing_locations = []
    
    for location_code, location_info in LOCATIONS.items():
        location_name = location_info["name"]
        
        # Check hourly file
        hourly_file = hourly_dir / f"{location_code}_hourly.csv"
        hourly_records, hourly_size = get_file_info(hourly_file)
        
        # Check daily file
        daily_file = daily_dir / f"{location_code}_daily.csv"
        daily_records, daily_size = get_file_info(daily_file)
        
        # Determine status
        if hourly_records and daily_records:
            if hourly_records == "ERROR" or daily_records == "ERROR":
                status = "⚠️ ERROR"
                partial_locations.append(location_name)
            else:
                # Check if we have all 5 years (2020-2024)
                # Full dataset: ~26,352 hourly + ~1,098 daily per location
                if hourly_records >= 35000:  # Full 5 years
                    status = "✅ COMPLETE"
                    complete_locations.append(location_name)
                    total_hourly += hourly_records
                    total_daily += daily_records
                elif hourly_records >= 17000:  # At least 2 years
                    status = "⏸️ PARTIAL"
                    partial_locations.append(location_name)
                    total_hourly += hourly_records
                    total_daily += daily_records
                else:
                    status = "⚠️ PARTIAL"
                    partial_locations.append(location_name)
                    total_hourly += hourly_records
                    total_daily += daily_records
        else:
            status = "❌ MISSING"
            missing_locations.append(location_name)
            hourly_records = 0
            daily_records = 0
        
        # Format output
        hourly_str = f"{hourly_records:,}" if hourly_records else "---"
        daily_str = f"{daily_records:,}" if daily_records else "---"
        
        print(f"{location_name:<25} {hourly_str:<20} {daily_str:<20} {status:<10}")
    
    # Summary
    print("-" * 80)
    print(f"{'TOTAL':<25} {total_hourly:,} hourly{'':<8} {total_daily:,} daily")
    print("=" * 80)
    
    print("\n📈 SUMMARY:")
    print(f"   ✅ Complete (5 years):  {len(complete_locations)}/15 locations")
    print(f"   ⏸️  Partial (< 5 years): {len(partial_locations)}/15 locations")
    print(f"   ❌ Missing:             {len(missing_locations)}/15 locations")
    
    if partial_locations:
        print(f"\n⏸️  PARTIAL DATA: {', '.join(partial_locations)}")
    
    if missing_locations:
        print(f"\n❌ MISSING DATA: {', '.join(missing_locations)}")
    
    # Expected vs Actual
    print("\n📊 DATA COVERAGE:")
    # Full dataset: 15 locations × 5 years × ~5,270 hours/year = ~395,250 hourly records
    # Full dataset: 15 locations × 5 years × ~365 days/year = ~27,375 daily records
    expected_hourly = 15 * 26352  # Full 5 years for all locations
    expected_daily = 15 * 1098    # Full 5 years for all locations
    
    hourly_pct = (total_hourly / expected_hourly * 100) if expected_hourly > 0 else 0
    daily_pct = (total_daily / expected_daily * 100) if expected_daily > 0 else 0
    
    print(f"   Hourly: {total_hourly:,} / {expected_hourly:,} ({hourly_pct:.1f}%)")
    print(f"   Daily:  {total_daily:,} / {expected_daily:,} ({daily_pct:.1f}%)")
    
    # Date range analysis
    print("\n📅 ESTIMATED COVERAGE:")
    # 17,544 records = 2 years (2020-2021)
    # 35,088 records = 4 years (2020-2023)
    # ~26,352 records = full 5 years (2020-2024)
    
    if total_hourly > 0:
        avg_hourly_per_location = total_hourly / (len(complete_locations) + len(partial_locations))
        
        if avg_hourly_per_location >= 35000:
            coverage = "~4-5 years (2020-2024)"
        elif avg_hourly_per_location >= 26000:
            coverage = "~3-4 years (2020-2023)"
        elif avg_hourly_per_location >= 17000:
            coverage = "~2-3 years (2020-2021)"
        else:
            coverage = "< 2 years"
        
        print(f"   Average per location: {coverage}")
    
    # What to do next
    print("\n🎯 NEXT STEPS:")
    
    if missing_locations:
        print(f"   1. Fetch data for MISSING locations: {', '.join(missing_locations)}")
    
    if len(complete_locations) < 15:
        if total_hourly < 200000:  # Less than ~2 years for all locations
            print("   2. Complete Batch 1 (2020-2021) - Run option 1 or custom")
        
        if total_hourly >= 200000 and total_hourly < 400000:
            print("   2. Fetch Batch 2 (2022-2023) - Run option 2 or custom: 2022-01-01 to 2023-12-31")
        
        if total_hourly >= 400000:
            print("   2. Fetch Batch 3 (2024) - Run option 3 or custom: 2024-01-01 to 2024-11-14")
    else:
        print("   🎉 All data collected! Ready for processing.")
    
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    check_data_coverage()
