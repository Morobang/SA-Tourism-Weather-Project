
USE SA_TOURISM_WEATHER;
GO

-- Create gold schema if not exists
IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'gold')
    EXEC('CREATE SCHEMA gold');
GO

-- Create gold table
CREATE TABLE gold.gold_location_season_summary (
    id INT IDENTITY(1,1) PRIMARY KEY,
    location_name NVARCHAR(100),
    season NVARCHAR(20),
    avg_perfect_day_score FLOAT,
    avg_temperature FLOAT,
    avg_precipitation FLOAT,
    percent_perfect_days FLOAT,
    total_days INT
);
GO
