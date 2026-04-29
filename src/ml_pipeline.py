"""
ml_pipeline.py
Solar Secure Solutions - Data Analytics Internship (May-July 2025)
ML-based pipeline for solar fault detection and performance monitoring.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import warnings
warnings.filterwarnings('ignore')

# Feature columns used for ML models
FEATURE_COLS = ['irradiance', 'temperature', 'voltage', 'current', 'power_output',
                                'efficiency_ratio', 'temp_coefficient', 'dust_factor']

class SolarFaultDetector:
      """ML pipeline for solar panel fault detection and efficiency monitoring."""

    def __init__(self, contamination: float = 0.05):
              self.scaler = StandardScaler()
              self.anomaly_detector = IsolationForest(contamination=contamination, random_state=42)
              self.fault_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
              self.is_fitted = False

          def preprocess(self, df: pd.DataFrame) -> np.ndarray:
                    """Scale features for ML model input."""
                    features = df[FEATURE_COLS].fillna(df[FEATURE_COLS].median())
                    return self.scaler.fit_transform(features)

    def detect_anomalies(self, df: pd.DataFrame) -> pd.DataFrame:
              """Use Isolation Forest to detect anomalous panel readings."""
              X = self.preprocess(df)
              df = df.copy()
              df['anomaly_score'] = self.anomaly_detector.fit_predict(X)
              df['is_fault'] = df['anomaly_score'] == -1
              fault_rate = df['is_fault'].mean() * 100
              print(f"Fault detection complete. Fault rate: {fault_rate:.2f}%")
              self.is_fitted = True
              return df

    def compute_efficiency(self, df: pd.DataFrame) -> pd.DataFrame:
              """Compute efficiency metrics for solar panels."""
              df = df.copy()
              df['actual_efficiency'] = (df['power_output'] / (df['irradiance'] * 1.6)) * 100
              df['efficiency_degradation'] = df['actual_efficiency'].pct_change(periods=24).fillna(0)
              df['performance_flag'] = df['actual_efficiency'] < df['actual_efficiency'].quantile(0.10)
              return df

          def generate_report(self, df: pd.DataFrame) -> dict:
                    """Generate a summary performance report."""
                    report = {
                                  'total_readings': len(df),
                                  'fault_count': int(df['is_fault'].sum()) if 'is_fault' in df.columns else 0,
                                  'avg_efficiency': float(df['actual_efficiency'].mean()) if 'actual_efficiency' in df.columns else None,
                                  'avg_power_output': float(df['power_output'].mean()),
                                  'peak_power': float(df['power_output'].max()),
                    }
                    return report


if __name__ == '__main__':
      df = pd.read_csv('data/processed/clean_solar_data.csv', parse_dates=['timestamp'])
      detector = SolarFaultDetector(contamination=0.05)
      df = detector.detect_anomalies(df)
      df = detector.compute_efficiency(df)
      report = detector.generate_report(df)
      print('Performance Report:', report)
              """Compute efficiency metrics for solar panels."""
              df = d
