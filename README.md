# SA Tourism Weather Project

A comprehensive data pipeline project for collecting, storing, analyzing, and visualizing weather data from South Africa using the Open-Meteo API to provide insights for tourism planning.

## 🎯 Project Overview

This project builds a complete data engineering pipeline that:
- Collects historical and forecast weather data from Open-Meteo API
- Stores data in a structured SQL database
- Performs exploratory data analysis and visualization
- Develops machine learning models for weather prediction
- Orchestrates automated data pipelines using Apache Airflow

## 🛠️ Tech Stack

- **Language**: Python 3.9+
- **Data Processing**: Pandas, NumPy
- **Database**: SQLite / PostgreSQL
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Notebooks**: Jupyter
- **Orchestration**: Apache Airflow (planned)
- **ML**: Scikit-learn (planned)

## 📁 Project Structure

```
SA-Tourism-Weather-Project/
├── data/
│   ├── raw/              # Raw API responses
│   ├── processed/        # Cleaned data
│   └── database/         # SQLite database file
├── notebooks/
│   └── *.ipynb          # Jupyter notebooks for analysis
├── src/
│   ├── __init__.py
│   ├── api_client.py    # API interaction functions
│   ├── database.py      # Database operations
│   ├── config.py        # Configuration settings
│   └── utils.py         # Helper functions
├── sql/
│   └── schema.sql       # Database schema
├── airflow/
│   └── dags/            # Airflow DAG definitions
├── tests/               # Unit tests
├── .env.example         # Environment variables template
├── requirements.txt     # Python dependencies
└── PROJECT_PLAN.md      # Detailed project plan
```

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Morobang/SA-Tourism-Weather-Project.git
   cd SA-Tourism-Weather-Project
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

### Quick Start

1. **Explore the API** - Open `notebooks/01_api_exploration.ipynb` (coming soon)
2. **Review the plan** - Check `PROJECT_PLAN.md` for detailed roadmap
3. **Run tests** - `pytest tests/` (when available)

## 📊 Data Source

This project uses the [Open-Meteo API](https://open-meteo.com/):
- **Historical Forecast API**: High-resolution archived weather data (2022-present)
- **Weather Forecast API**: Current conditions and 7-16 day forecasts
- **Coverage**: Global, with focus on South African locations
- **Variables**: Temperature, precipitation, wind, humidity, UV index, and more

## 🗺️ Roadmap

- [x] Project setup and planning
- [ ] API exploration and data collection scripts
- [ ] Database schema design and implementation
- [ ] Exploratory data analysis
- [ ] Visualization dashboard
- [ ] Machine learning models
- [ ] Airflow pipeline automation

See [PROJECT_PLAN.md](PROJECT_PLAN.md) for detailed phases and tasks.

## 📝 Contributing

This is a learning project. Feel free to fork and experiment!

## 📄 License

TBD

## 👤 Author

**Morobang**
- GitHub: [@Morobang](https://github.com/Morobang)

## 🙏 Acknowledgments

- [Open-Meteo](https://open-meteo.com/) for providing free weather API access
- South African tourism industry for inspiration
