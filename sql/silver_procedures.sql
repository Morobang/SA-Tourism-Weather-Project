-- Silver Layer Stored Procedures
USE SA_TOURISM_WEATHER;
GO

-- Insert feature-engineered daily data
CREATE OR ALTER PROCEDURE silver.usp_insert_silver_daily_features
    @date DATE,
    @location_code NVARCHAR(50),
    @location_name NVARCHAR(100),
    @temperature_2m_mean FLOAT,
    @temperature_2m_min FLOAT,
    @temperature_2m_max FLOAT,
    @precipitation_sum FLOAT,
    @wind_speed_10m_max FLOAT,
    @sunshine_duration INT,
    @cloud_cover_mean FLOAT,
    @season NVARCHAR(20),
    @is_weekend BIT,
    @is_perfect_day BIT,
    @perfect_day_score FLOAT,
    @tourism_season NVARCHAR(20),
    @temp_category NVARCHAR(20),
    @rain_category NVARCHAR(20),
    @is_school_holiday BIT,
    @is_public_holiday BIT,
    @is_dry BIT,
    @is_rainy BIT,
    @is_windy BIT,
    @is_coastal BIT,
    @is_wine_region BIT,
    @is_safari_gateway BIT,
    @is_city_business BIT,
    @is_adventure BIT,
    @perfect_beach_day BIT,
    @perfect_wine_day BIT,
    @perfect_safari_day BIT,
    @is_peak_season BIT,
    @is_low_season BIT,
    @temp_7day_avg FLOAT,
    @precip_7day_sum FLOAT,
    @temp_3day_avg FLOAT,
    @consecutive_dry_days INT,
    @consecutive_rainy_days INT,
    @temp_change_1day FLOAT,
    @sudden_temp_change BIT
AS
BEGIN
    INSERT INTO silver.silver_daily_features (
        date, location_code, location_name, temperature_2m_mean, temperature_2m_min, temperature_2m_max,
        precipitation_sum, wind_speed_10m_max, sunshine_duration, cloud_cover_mean, season, is_weekend,
        is_perfect_day, perfect_day_score, tourism_season, temp_category, rain_category, is_school_holiday,
        is_public_holiday, is_dry, is_rainy, is_windy, is_coastal, is_wine_region, is_safari_gateway,
        is_city_business, is_adventure, perfect_beach_day, perfect_wine_day, perfect_safari_day, is_peak_season,
        is_low_season, temp_7day_avg, precip_7day_sum, temp_3day_avg, consecutive_dry_days, consecutive_rainy_days,
        temp_change_1day, sudden_temp_change
    ) VALUES (
        @date, @location_code, @location_name, @temperature_2m_mean, @temperature_2m_min, @temperature_2m_max,
        @precipitation_sum, @wind_speed_10m_max, @sunshine_duration, @cloud_cover_mean, @season, @is_weekend,
        @is_perfect_day, @perfect_day_score, @tourism_season, @temp_category, @rain_category, @is_school_holiday,
        @is_public_holiday, @is_dry, @is_rainy, @is_windy, @is_coastal, @is_wine_region, @is_safari_gateway,
        @is_city_business, @is_adventure, @perfect_beach_day, @perfect_wine_day, @perfect_safari_day, @is_peak_season,
        @is_low_season, @temp_7day_avg, @precip_7day_sum, @temp_3day_avg, @consecutive_dry_days, @consecutive_rainy_days,
        @temp_change_1day, @sudden_temp_change
    );
END
GO
