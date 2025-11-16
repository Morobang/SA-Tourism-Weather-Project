-- Bronze Layer Stored Procedures
USE SA_TOURISM_WEATHER;
GO

-- Insert raw daily weather data
CREATE OR ALTER PROCEDURE bronze.usp_insert_bronze_daily_weather
    @date DATE,
    @location_code NVARCHAR(50),
    @location_name NVARCHAR(100),
    @temperature_2m_mean FLOAT,
    @temperature_2m_min FLOAT,
    @temperature_2m_max FLOAT,
    @precipitation_sum FLOAT,
    @wind_speed_10m_max FLOAT,
    @sunshine_duration INT,
    @cloud_cover_mean FLOAT
AS
BEGIN
    INSERT INTO bronze.bronze_daily_weather (
        date, location_code, location_name, temperature_2m_mean, temperature_2m_min, temperature_2m_max,
        precipitation_sum, wind_speed_10m_max, sunshine_duration, cloud_cover_mean
    ) VALUES (
        @date, @location_code, @location_name, @temperature_2m_mean, @temperature_2m_min, @temperature_2m_max,
        @precipitation_sum, @wind_speed_10m_max, @sunshine_duration, @cloud_cover_mean
    );
END
GO
