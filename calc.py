import pandas as pd
import numpy as np
from scipy import stats
def calculate_stats(data, column_name):
    scores = data[column_name].dropna()
    
    stats_dict = {
        "Statistik": ["Rata-rata (Mean)", "Median", "Modus", "Kuartil 1 (Q1)", "Kuartil 2 (Q2)", "Kuartil 3 (Q3)"],
        "Nilai": [
            round(scores.mean(), 2),
            round(scores.median(), 2),
            round(stats.mode(scores, keepdims=True).mode[0], 2),
            round(scores.quantile(0.25), 2),
            round(scores.quantile(0.50), 2),
            round(scores.quantile(0.75), 2)
        ]
    }
    return pd.DataFrame(stats_dict)

def generate_frequency_table(data, column_name):
    # Fetch Data
    scores = data[column_name].dropna().sort_values().reset_index(drop=True)
    n = len(scores)
    
    # Classes
    k = int(1 + 3.322 * np.log10(n))
    
    # Range
    r = scores.max() - scores.min()
    p = int(np.ceil(r / k)) if r > 0 else 1
    
    # Batas Bawah
    start_point = scores.min()
    
    bins = [start_point + i * p for i in range(k + 1)]
    
    # Table Distribution
    labels = [f"{int(bins[i])} - {int(bins[i+1]-1)}" for i in range(k)]
    
    # Calc Frequency with pd.cut
    freq_series = pd.cut(scores, bins=bins, labels=labels, include_lowest=True, right=False).value_counts().sort_index()
    
    df_freq = pd.DataFrame({
        'Interval Kelas': freq_series.index,
        'Frekuensi (f)': freq_series.values
    })
    
    # Add Frekuensi Kumulatif
    df_freq['Frek Kumulatif Kurang Dari (Ogiva Positif)'] = df_freq['Frekuensi (f)'].cumsum()
    total_f = df_freq['Frekuensi (f)'].sum()
    df_freq['Frek Kumulatif Lebih Dari (Ogiva Negatif)'] = total_f - df_freq['Frekuensi (f)'].cumsum().shift(1).fillna(0)
    
    return df_freq, bins