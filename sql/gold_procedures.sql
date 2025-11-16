-- Gold Layer Stored Procedures
USE SA_TOURISM_WEATHER;
GO

-- Refresh gold summary from silver
CREATE OR ALTER PROCEDURE gold.usp_refresh_gold_location_season_summary
AS
BEGIN
    DELETE FROM gold.gold_location_season_summary;
    INSERT INTO gold.gold_location_season_summary (location_name, season, avg_perfect_day_score, avg_temperature, avg_precipitation, percent_perfect_days, total_days)
    SELECT
        ISNULL(location_name, 'Unknown') AS location_name,
        ISNULL(season, 'Unknown') AS season,
        AVG(perfect_day_score) AS avg_perfect_day_score,
        AVG(temperature_2m_mean) AS avg_temperature,
        AVG(precipitation_sum) AS avg_precipitation,
        AVG(CAST(is_perfect_day AS FLOAT)) * 100.0 AS percent_perfect_days,
        COUNT(*) AS total_days
    FROM silver.silver_daily_features
    GROUP BY location_name, season;
END
GO
