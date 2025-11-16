
-- Create database if not exists
IF DB_ID(N'SA_TOURISM_WEATHER') IS NULL
    CREATE DATABASE SA_TOURISM_WEATHER;
GO

USE SA_TOURISM_WEATHER;
GO

-- Create bronze schema if not exists
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'bronze')
    EXEC('CREATE SCHEMA bronze');
GO

-- Create bronze table
CREATE TABLE bronze.bronze_daily_weather (
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
    cloud_cover_mean FLOAT
    -- Add other raw columns as needed
);
GO
