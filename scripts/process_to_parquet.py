"""
Data Processing Script - CSV to Parquet Conversion

Converts raw CSV weather data to Parquet format for faster analysis.
Intelligently detects new data and appends to existing Parquet files.

Usage:
    python scripts/process_to_parquet.py           # Process new data only
    python scripts/process_to_parquet.py --rebuild # Rebuild everything from scratch
"""

import sys
from pathlib import Path
import pandas as pd
from datetime import datetime
import argparse

# ============================================================================
# SETUP
# ============================================================================

project_root = Path(__file__).parent.parent

# Data directories
raw_dir = project_root / "data" / "raw" / "historical"
processed_dir = project_root / "data" / "processed"

# Input CSV directories
hourly_csv_dir = raw_dir / "hourly"
daily_csv_dir = raw_dir / "daily"

# Output Parquet directories
hourly_parquet_dir = processed_dir / "hourly"
daily_parquet_dir = processed_dir / "daily"

# Create output directories
hourly_parquet_dir.mkdir(parents=True, exist_ok=True)
daily_parquet_dir.mkdir(parents=True, exist_ok=True)

# Output files
hourly_parquet_file = hourly_parquet_dir / "all_locations_hourly.parquet"
daily_parquet_file = daily_parquet_dir / "all_locations_daily.parquet"


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_csv_files(directory):
    """Get all CSV files in a directory."""
    if not directory.exists():
        return []
    return sorted(directory.glob("*.csv"))


def get_existing_locations(parquet_file):
    """Get list of locations already in the Parquet file."""
    if not parquet_file.exists():
        return set()
    
    try:
        df = pd.read_parquet(parquet_file, columns=['location_code'])
        return set(df['location_code'].unique())
    except Exception as e:
        print(f"   ⚠️  Warning: Could not read existing Parquet: {e}")
        return set()


def process_csv_files(csv_files, frequency="hourly"):
    """
    Read and combine multiple CSV files into a single DataFrame.
    
    Args:
        csv_files: List of Path objects pointing to CSV files
        frequency: "hourly" or "daily"
    
    Returns:
        Combined DataFrame
    """
    if not csv_files:
        return None
    
    print(f"\n   Processing {len(csv_files)} {frequency} CSV files...")
    
    dfs = []
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            
            # Parse date column
            df['date'] = pd.to_datetime(df['date'])
            
            # Add metadata
            location_code = csv_file.stem.replace(f"_{frequency}", "")
            
            # Ensure location_code and location_name columns exist
            if 'location_code' not in df.columns:
                df['location_code'] = location_code
            if 'location_name' not in df.columns:
                # Try to infer from filename or use location_code
                df['location_name'] = location_code.replace('_', ' ').title()
            
            dfs.append(df)
            print(f"      ✅ {csv_file.name}: {len(df):,} records")
            
        except Exception as e:
            print(f"      ❌ Error reading {csv_file.name}: {e}")
            continue
    
    if not dfs:
        return None
    
    # Combine all DataFrames
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Sort by date and location
    combined_df = combined_df.sort_values(['date', 'location_code']).reset_index(drop=True)
    
    # Remove duplicates (if any)
    original_rows = len(combined_df)
    combined_df = combined_df.drop_duplicates(subset=['date', 'location_code'], keep='last')
    duplicates_removed = original_rows - len(combined_df)
    
    if duplicates_removed > 0:
        print(f"   🧹 Removed {duplicates_removed:,} duplicate records")
    
    return combined_df


def save_to_parquet(df, output_file, frequency="hourly"):
    """Save DataFrame to Parquet format."""
    if df is None or len(df) == 0:
        print(f"   ⚠️  No data to save for {frequency}")
        return False
    
    try:
        df.to_parquet(output_file, index=False, compression='snappy')
        
        # Get file size
        size_mb = output_file.stat().st_size / (1024 * 1024)
        
        print(f"   ✅ Saved {len(df):,} records to {output_file.name}")
        print(f"      File size: {size_mb:.2f} MB")
        
        return True
    
    except Exception as e:
        print(f"   ❌ Error saving Parquet: {e}")
        return False


# ============================================================================
# MAIN PROCESSING FUNCTIONS
# ============================================================================

def process_frequency(frequency, force_rebuild=False):
    """
    Process data for a specific frequency (hourly or daily).
    
    Args:
        frequency: "hourly" or "daily"
        force_rebuild: If True, rebuild from scratch. If False, append new data.
    """
    print("\n" + "="*80)
    print(f"📊 Processing {frequency.upper()} Data")
    print("="*80)
    
    # Set up paths
    if frequency == "hourly":
        csv_dir = hourly_csv_dir
        parquet_file = hourly_parquet_file
    else:
        csv_dir = daily_csv_dir
        parquet_file = daily_parquet_file
    
    # Get all CSV files
    csv_files = get_csv_files(csv_dir)
    
    if not csv_files:
        print(f"   ⚠️  No CSV files found in {csv_dir}")
        return False
    
    print(f"   Found {len(csv_files)} CSV files in {csv_dir}")
    
    # Check if we should do incremental or full rebuild
    if force_rebuild or not parquet_file.exists():
        print(f"   🔄 Building from scratch...")
        
        # Process all CSV files
        combined_df = process_csv_files(csv_files, frequency)
        
        if combined_df is not None:
            print(f"\n   📈 Combined Statistics:")
            print(f"      Total records: {len(combined_df):,}")
            print(f"      Date range: {combined_df['date'].min()} to {combined_df['date'].max()}")
            print(f"      Locations: {combined_df['location_code'].nunique()}")
            print(f"      Columns: {len(combined_df.columns)}")
            
            # Save to Parquet
            return save_to_parquet(combined_df, parquet_file, frequency)
    
    else:
        print(f"   📂 Existing Parquet found, checking for new data...")
        
        # Load existing Parquet
        existing_df = pd.read_parquet(parquet_file)
        print(f"   📊 Existing data: {len(existing_df):,} records")
        print(f"      Date range: {existing_df['date'].min()} to {existing_df['date'].max()}")
        
        # Get locations already in Parquet
        existing_locations = set(existing_df['location_code'].unique())
        print(f"      Locations: {len(existing_locations)}")
        
        # Find new CSV files (locations not in Parquet OR updated dates)
        new_csv_files = []
        for csv_file in csv_files:
            location_code = csv_file.stem.replace(f"_{frequency}", "")
            
            # Check if this location is new
            if location_code not in existing_locations:
                new_csv_files.append(csv_file)
                print(f"   🆕 New location: {location_code}")
            else:
                # Check if CSV has newer data than Parquet
                try:
                    csv_df = pd.read_csv(csv_file)
                    csv_df['date'] = pd.to_datetime(csv_df['date'])
                    csv_max_date = csv_df['date'].max()
                    
                    existing_max_date = existing_df[existing_df['location_code'] == location_code]['date'].max()
                    
                    if csv_max_date > existing_max_date:
                        new_csv_files.append(csv_file)
                        print(f"   🔄 Updated data: {location_code} (new data until {csv_max_date.date()})")
                except:
                    # If error, include it to be safe
                    new_csv_files.append(csv_file)
        
        if not new_csv_files:
            print(f"\n   ✅ No new data to process! Parquet is up to date.")
            return True
        
        print(f"\n   🔄 Processing {len(new_csv_files)} new/updated files...")
        
        # Process new CSV files
        new_df = process_csv_files(new_csv_files, frequency)
        
        if new_df is not None:
            # Combine with existing data
            print(f"\n   🔗 Combining with existing data...")
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            
            # Remove duplicates (keep latest)
            original_rows = len(combined_df)
            combined_df = combined_df.drop_duplicates(subset=['date', 'location_code'], keep='last')
            duplicates_removed = original_rows - len(combined_df)
            
            if duplicates_removed > 0:
                print(f"   🧹 Removed {duplicates_removed:,} duplicate records")
            
            # Sort
            combined_df = combined_df.sort_values(['date', 'location_code']).reset_index(drop=True)
            
            print(f"\n   📈 Updated Statistics:")
            print(f"      Total records: {len(combined_df):,} (added {len(combined_df) - len(existing_df):,})")
            print(f"      Date range: {combined_df['date'].min()} to {combined_df['date'].max()}")
            print(f"      Locations: {combined_df['location_code'].nunique()}")
            
            # Save updated Parquet
            return save_to_parquet(combined_df, parquet_file, frequency)
    
    return False


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main entry point."""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Process weather data to Parquet format")
    parser.add_argument('--rebuild', action='store_true', 
                       help='Force rebuild from scratch (ignore existing Parquet)')
    args = parser.parse_args()
    
    print("\n" + "🌍 SA TOURISM WEATHER PROJECT - DATA PROCESSING")
    print("="*80)
    
    if args.rebuild:
        print("🔄 REBUILD MODE: Processing all data from scratch")
    else:
        print("⚡ INCREMENTAL MODE: Processing only new/updated data")
    
    print("="*80)
    
    start_time = datetime.now()
    
    # Process hourly data
    hourly_success = process_frequency("hourly", force_rebuild=args.rebuild)
    
    # Process daily data
    daily_success = process_frequency("daily", force_rebuild=args.rebuild)
    
    # Summary
    elapsed = datetime.now() - start_time
    minutes = int(elapsed.total_seconds() // 60)
    seconds = int(elapsed.total_seconds() % 60)
    
    print("\n" + "="*80)
    print("✅ PROCESSING COMPLETE!")
    print(f"   Total time: {minutes}m {seconds}s")
    
    if hourly_success:
        print(f"   ✅ Hourly data: {hourly_parquet_file}")
    else:
        print(f"   ⚠️  Hourly data: Issues encountered")
    
    if daily_success:
        print(f"   ✅ Daily data: {daily_parquet_file}")
    else:
        print(f"   ⚠️  Daily data: Issues encountered")
    
    print("\n💡 Next Steps:")
    print("   Load data in Jupyter notebook:")
    print("   >>> import pandas as pd")
    print(f"   >>> hourly = pd.read_parquet('data/processed/hourly/all_locations_hourly.parquet')")
    print(f"   >>> daily = pd.read_parquet('data/processed/daily/all_locations_daily.parquet')")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
