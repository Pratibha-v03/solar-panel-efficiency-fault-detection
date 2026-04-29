"""
data_collection.py
Solar Secure Solutions - Data Analytics Internship (May-July 2025)
Module for collecting solar panel data from sensors and APIs.
"""

import requests
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta

# Configuration
API_BASE_URL = "https://api.solarsecure.io/v1"
RAW_DATA_DIR = "data/raw"

class SolarDataCollector:
      """Handles collection of solar panel data from sensors and APIs."""

    def __init__(self, api_key: str = None):
              self.api_key = api_key or os.getenv('SOLAR_API_KEY')
              self.headers = {'Authorization': f'Bearer {self.api_key}', 'Content-Type': 'application/json'}
              os.makedirs(RAW_DATA_DIR, exist_ok=True)

    def fetch_sensor_data(self, panel_id: str, start_date: str, end_date: str) -> pd.DataFrame:
              """Fetch solar sensor data for a given panel and date range."""
              endpoint = f"{API_BASE_URL}/panels/{panel_id}/readings"
              params = {'start': start_date, 'end': end_date, 'interval': '15min'}
              try:
                            response = requests.get(endpoint, headers=self.headers, params=params, timeout=30)
                            response.raise_for_status()
                            data = response.json()
                            df = pd.DataFrame(data['readings'])
                            df['panel_id'] = panel_id
                            df['timestamp'] = pd.to_datetime(df['timestamp'])
                            print(f"Fetched {len(df)} records for panel {panel_id}")
                            return df
except requests.RequestException as e:
            print(f"Error fetching data for panel {panel_id}: {e}")
            return pd.DataFrame()

    def load_csv_data(self, filepath: str) -> pd.DataFrame:
              """Load solar data from a local CSV file."""
              df = pd.read_csv(filepath, parse_dates=['timestamp'])
              print(f"Loaded {len(df)} records from {filepath}")
              return df

    def save_raw_data(self, df: pd.DataFrame, filename: str):
              """Save raw data to the data/raw directory."""
              filepath = os.path.join(RAW_DATA_DIR, filename)
              df.to_csv(filepath, index=False)
              print(f"Saved raw data to {filepath}")


if __name__ == '__main__':
      collector = SolarDataCollector()
      df = collector.fetch_sensor_data('PANEL_001', '2025-05-01', '2025-07-31')
      if not df.empty:
                collector.save_raw_data(df, 'panel_001_readings.csv')
