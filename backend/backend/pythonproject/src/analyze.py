import pandas as pd
from sklearn.ensemble import IsolationForest

def dataanalysis(df):
    """Analyze data using Isolation Forest for anomaly detection."""
    
    df_values = df[["CO2 (ppm)", "O2 (%)", "Humidity (%)"]].values
    
    # Train Isolation Forest
    iso_forest = IsolationForest(contamination=0.1, random_state=42)
    df['Anomaly'] = iso_forest.fit_predict(df_values)
    
    print(df)
    