"""
Module untuk preprocessing data kualitas udara
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import joblib
import os


class AirQualityPreprocessor:
    """Kelas untuk preprocessing data kualitas udara"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.feature_scaler = MinMaxScaler()
        
        # Standar WHO untuk kualitas udara (annual mean)
        self.who_standards = {
            'pm2_5': 15,    # μg/m³
            'pm10': 45,     # μg/m³
            'no2': 25,      # μg/m³
            'so2': 40,      # μg/m³ (24-hour)
            'o3': 100,      # μg/m³ (8-hour)
            'co': 4000,     # μg/m³ (24-hour), converted from 4 mg/m³
        }
    
    def load_data(self, filepath='data/air_quality_data.csv'):
        """Load data dari CSV"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File {filepath} not found!")
        
        df = pd.read_csv(filepath)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    
    def add_temporal_features(self, df):
        """Tambahkan fitur temporal dari timestamp"""
        df = df.copy()
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['day_of_month'] = df['timestamp'].dt.day
        df['month'] = df['timestamp'].dt.month
        df['year'] = df['timestamp'].dt.year
        
        # Cyclical encoding untuk hour dan month
        df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24)
        df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24)
        df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
        df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
        
        return df
    
    def add_lag_features(self, df, columns, lags=[1, 3, 6, 12, 24]):
        """Tambahkan lag features untuk time series"""
        df = df.copy()
        df = df.sort_values(['city', 'timestamp'])
        
        for col in columns:
            for lag in lags:
                df[f'{col}_lag_{lag}'] = df.groupby('city')[col].shift(lag)
        
        return df
    
    def add_rolling_features(self, df, columns, windows=[3, 6, 12, 24]):
        """Tambahkan rolling statistics - HANYA MENGGUNAKAN DATA MASA LALU"""
        df = df.copy()
        df = df.sort_values(['city', 'timestamp'])
        
        for col in columns:
            for window in windows:
                # PENTING: Shift dulu agar tidak menggunakan current value (data leakage)
                df[f'{col}_rolling_mean_{window}'] = df.groupby('city')[col].transform(
                    lambda x: x.shift(1).rolling(window=window, min_periods=1).mean()
                )
                df[f'{col}_rolling_std_{window}'] = df.groupby('city')[col].transform(
                    lambda x: x.shift(1).rolling(window=window, min_periods=1).std()
                )
        
        return df
    
    def calculate_who_compliance(self, df):
        """Hitung compliance terhadap standar WHO"""
        df = df.copy()
        
        # Ratio terhadap standar WHO
        for pollutant, standard in self.who_standards.items():
            if pollutant in df.columns:
                df[f'{pollutant}_who_ratio'] = df[pollutant] / standard
        
        # Overall air quality status
        df['pm2_5_status'] = pd.cut(
            df['pm2_5'], 
            bins=[0, 15, 35, 55, 150, np.inf],
            labels=['Good', 'Moderate', 'Unhealthy-Sensitive', 'Unhealthy', 'Very Unhealthy']
        )
        
        return df
    
    def handle_missing_values(self, df):
        """Handle missing values"""
        df = df.copy()
        
        # Forward fill untuk time series data (pandas 2.0+ compatible)
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df.groupby('city')[numeric_cols].ffill()
        
        # Backward fill untuk sisa missing values
        df[numeric_cols] = df.groupby('city')[numeric_cols].bfill()
        
        # Drop jika masih ada missing values
        df = df.dropna()
        
        return df
    
    def remove_outliers(self, df, columns, n_std=3):
        """Remove outliers menggunakan z-score"""
        df = df.copy()
        
        for col in columns:
            if col in df.columns:
                mean = df[col].mean()
                std = df[col].std()
                df = df[
                    (df[col] >= mean - n_std * std) & 
                    (df[col] <= mean + n_std * std)
                ]
        
        return df
    
    def encode_categorical(self, df):
        """Encode categorical variables"""
        df = df.copy()
        
        # One-hot encoding untuk city
        df = pd.get_dummies(df, columns=['city'], prefix='city')
        
        return df
    
    def prepare_features(self, df):
        """Persiapkan features untuk modeling"""
        pollutant_cols = ['pm2_5', 'pm10', 'no2', 'so2', 'o3', 'co']
        
        # Add temporal features
        df = self.add_temporal_features(df)
        
        # Add lag features
        df = self.add_lag_features(df, pollutant_cols, lags=[1, 3, 6, 12])
        
        # Add rolling features
        df = self.add_rolling_features(df, pollutant_cols, windows=[3, 6, 12])
        
        # Calculate WHO compliance
        df = self.calculate_who_compliance(df)
        
        # Handle missing values
        df = self.handle_missing_values(df)
        
        # Remove outliers
        df = self.remove_outliers(df, pollutant_cols)
        
        return df
    
    def split_data(self, df, target_col='pm2_5', test_size=0.2, val_size=0.1):
        """Split data menjadi train, validation, dan test set - TIME-BASED SPLIT"""
        # Sort by timestamp - CRITICAL untuk time series!
        df = df.sort_values('timestamp')
        
        # Feature columns (exclude target, timestamp, city, dan categorical)
        exclude_cols = [target_col, 'timestamp', 'city', 'aqi', 'pm2_5_status']
        feature_cols = [col for col in df.columns if col not in exclude_cols 
                       and not col.endswith('_status')
                       and df[col].dtype in ['int64', 'float64']]  # Only numeric columns
        
        X = df[feature_cols]
        y = df[target_col]
        
        # TIME-BASED SPLIT (tidak random!) untuk menghindari data leakage
        train_val_size = 1 - test_size
        val_size_adjusted = val_size / train_val_size
        
        split_idx_test = int(len(df) * (1 - test_size))
        split_idx_val = int(len(df) * (1 - test_size - val_size))
        
        # Split berdasarkan waktu
        X_train = X[:split_idx_val]
        X_val = X[split_idx_val:split_idx_test]
        X_test = X[split_idx_test:]
        
        y_train = y[:split_idx_val]
        y_val = y[split_idx_val:split_idx_test]
        y_test = y[split_idx_test:]
        
        print(f"\nTime-based split:")
        print(f"  Train: index 0 to {split_idx_val} ({len(X_train)} samples)")
        print(f"  Val: index {split_idx_val} to {split_idx_test} ({len(X_val)} samples)")
        print(f"  Test: index {split_idx_test} to {len(df)} ({len(X_test)} samples)")
        
        return X_train, X_val, X_test, y_train, y_val, y_test, feature_cols
    
    def scale_features(self, X_train, X_val, X_test):
        """Scale features"""
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_val_scaled = self.scaler.transform(X_val)
        X_test_scaled = self.scaler.transform(X_test)
        
        return X_train_scaled, X_val_scaled, X_test_scaled
    
    def save_preprocessor(self, filepath='models/preprocessor.pkl'):
        """Simpan preprocessor"""
        joblib.dump(self.scaler, filepath)
        print(f"Preprocessor saved to {filepath}")
    
    def load_preprocessor(self, filepath='models/preprocessor.pkl'):
        """Load preprocessor"""
        self.scaler = joblib.load(filepath)
        print(f"Preprocessor loaded from {filepath}")


def main():
    """Main function untuk preprocessing"""
    preprocessor = AirQualityPreprocessor()
    
    print("Loading data...")
    df = preprocessor.load_data()
    
    print("\nOriginal data shape:", df.shape)
    print("\nPreparing features...")
    df_processed = preprocessor.prepare_features(df)
    
    print("Processed data shape:", df_processed.shape)
    print("\nSplitting data...")
    X_train, X_val, X_test, y_train, y_val, y_test, feature_cols = preprocessor.split_data(df_processed)
    
    print(f"Train set: {X_train.shape}")
    print(f"Validation set: {X_val.shape}")
    print(f"Test set: {X_test.shape}")
    
    print("\nScaling features...")
    X_train_scaled, X_val_scaled, X_test_scaled = preprocessor.scale_features(
        X_train, X_val, X_test
    )
    
    # Save processed data
    print("\nSaving processed data...")
    
    # Save train data
    train_df = pd.DataFrame(X_train_scaled, columns=feature_cols)
    train_df['target'] = y_train.values
    train_df.to_csv('data/train_data.csv', index=False)
    
    # Save validation data
    val_df = pd.DataFrame(X_val_scaled, columns=feature_cols)
    val_df['target'] = y_val.values
    val_df.to_csv('data/val_data.csv', index=False)
    
    # Save test data
    test_df = pd.DataFrame(X_test_scaled, columns=feature_cols)
    test_df['target'] = y_test.values
    test_df.to_csv('data/test_data.csv', index=False)
    
    # Save preprocessor
    preprocessor.save_preprocessor()
    
    print("\n" + "="*50)
    print("Preprocessing completed successfully!")
    print("="*50)
    print(f"Feature columns: {len(feature_cols)}")
    print(f"\nFiles saved:")
    print("  - data/train_data.csv")
    print("  - data/val_data.csv")
    print("  - data/test_data.csv")
    print("  - models/preprocessor.pkl")


if __name__ == "__main__":
    main()
