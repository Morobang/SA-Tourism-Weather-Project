
USE SA_TOURISM_WEATHER;
GO

-- Create silver schema if not exists
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'silver')
    EXEC('CREATE SCHEMA silver');
GO

-- Create silver table
CREATE TABLE silver.silver_daily_features (
    id INT IDENTITY(1,1) PRIMARY KEY,
    date DATE NOT NULL,
    location_code NVARCHAR(50) NOT NULL,
    location_name NVARCHAR(100),
    temperature_2m_mean FLOAT,
    temperature_2m_min FLOAT,
    temperature_2m_max FLOAT,
    precipitation_sum FLOAT,
    wind_speed_10m_max FLOAT,
    sunshine_duration INT,
    cloud_cover_mean FLOAT,
    season NVARCHAR(20),
    is_weekend BIT,
    is_perfect_day BIT,
    perfect_day_score FLOAT,
    tourism_season NVARCHAR(20),
    temp_category NVARCHAR(20),
    rain_category NVARCHAR(20),
    is_school_holiday BIT,
    is_public_holiday BIT,
    is_dry BIT,
    is_rainy BIT,
    is_windy BIT,
    is_coastal BIT,
    is_wine_region BIT,
    is_safari_gateway BIT,
    is_city_business BIT,
    is_adventure BIT,
    perfect_beach_day BIT,
    perfect_wine_day BIT,
    perfect_safari_day BIT,
    is_peak_season BIT,
    is_low_season BIT,
    temp_7day_avg FLOAT,
    precip_7day_sum FLOAT,
    temp_3day_avg FLOAT,
    consecutive_dry_days INT,
    consecutive_rainy_days INT,
    temp_change_1day FLOAT,
    sudden_temp_change BIT
    -- Add other engineered columns as needed
);
GO
