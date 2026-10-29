"""
Module untuk prediksi kualitas udara
"""
import pandas as pd
import numpy as np
import joblib
from tensorflow import keras
import json


class AirQualityPredictor:
    """Kelas untuk prediksi kualitas udara"""
    
    def __init__(self):
        self.rf_model = None
        self.gb_model = None
        self.lstm_model = None
        self.preprocessor = None
        self.feature_cols = None
        
        # Standar WHO
        self.who_standards = {
            'pm2_5': 15,
            'pm10': 45,
            'no2': 25,
            'so2': 40,
            'o3': 100,
            'co': 4000,
        }
    
    def load_models(self):
        """Load trained models"""
        try:
            self.rf_model = joblib.load('models/random_forest_model.pkl')
            print("✓ Random Forest model loaded")
        except Exception as e:
            print(f"✗ Could not load Random Forest: {e}")
        
        try:
            self.gb_model = joblib.load('models/gradient_boosting_model.pkl')
            print("✓ Gradient Boosting model loaded")
        except Exception as e:
            print(f"✗ Could not load Gradient Boosting: {e}")
        
        try:
            # Try loading LSTM with custom objects for backward compatibility
            from tensorflow.keras import metrics
            custom_objects = {
                'mse': metrics.MeanSquaredError(),
                'mae': metrics.MeanAbsoluteError()
            }
            try:
                self.lstm_model = keras.models.load_model('models/lstm_model.h5', 
                                                         custom_objects=custom_objects,
                                                         compile=False)
            except:
                # Fallback: load without compilation
                self.lstm_model = keras.models.load_model('models/lstm_model.h5', compile=False)
            
            # Recompile model
            self.lstm_model.compile(
                optimizer='adam',
                loss='mse',
                metrics=['mae']
            )
            print("✓ LSTM model loaded")
        except Exception as e:
            print(f"✗ Could not load LSTM: {e}")
        
        try:
            self.preprocessor = joblib.load('models/preprocessor.pkl')
            print("✓ Preprocessor loaded")
        except Exception as e:
            print(f"✗ Could not load preprocessor: {e}")
    
    def predict_single(self, features, model_type='random_forest'):
        """Prediksi untuk single input"""
        if model_type == 'random_forest' and self.rf_model:
            return self.rf_model.predict(features)[0]
        elif model_type == 'gradient_boosting' and self.gb_model:
            return self.gb_model.predict(features)[0]
        else:
            raise ValueError(f"Model {model_type} not available")
    
    def predict_ensemble(self, features):
        """Prediksi menggunakan ensemble (average dari semua model)"""
        predictions = []
        
        if self.rf_model:
            predictions.append(self.rf_model.predict(features)[0])
        
        if self.gb_model:
            predictions.append(self.gb_model.predict(features)[0])
        
        if len(predictions) > 0:
            return np.mean(predictions)
        else:
            raise ValueError("No models available for prediction")
    
    def predict_future(self, city_data, hours=24, model_type='random_forest'):
        """Prediksi untuk beberapa jam ke depan"""
        predictions = []
        current_data = city_data.copy()
        
        for hour in range(hours):
            # Predict next hour
            pred = self.predict_single(current_data, model_type)
            predictions.append(pred)
            
            # Update features for next prediction (simple approach)
            # In production, you'd update all lag features properly
            current_data = current_data.copy()
        
        return predictions
    
    def classify_air_quality(self, pm25_value):
        """Klasifikasi kualitas udara berdasarkan PM2.5"""
        if pm25_value <= 15:
            return {
                'status': 'Good',
                'color': '#00e400',
                'description': 'Kualitas udara baik, aman untuk semua aktivitas',
                'who_compliant': True
            }
        elif pm25_value <= 35:
            return {
                'status': 'Moderate',
                'color': '#ffff00',
                'description': 'Kualitas udara sedang, dapat diterima untuk sebagian besar orang',
                'who_compliant': False
            }
        elif pm25_value <= 55:
            return {
                'status': 'Unhealthy for Sensitive Groups',
                'color': '#ff7e00',
                'description': 'Kelompok sensitif mungkin mengalami efek kesehatan',
                'who_compliant': False
            }
        elif pm25_value <= 150:
            return {
                'status': 'Unhealthy',
                'color': '#ff0000',
                'description': 'Semua orang mungkin mulai mengalami efek kesehatan',
                'who_compliant': False
            }
        else:
            return {
                'status': 'Very Unhealthy',
                'color': '#8f3f97',
                'description': 'Peringatan kesehatan: semua orang dapat mengalami efek kesehatan serius',
                'who_compliant': False
            }
    
    def get_recommendations(self, air_quality_status):
        """Dapatkan rekomendasi berdasarkan status kualitas udara"""
        recommendations = {
            'Good': [
                'Nikmati aktivitas outdoor',
                'Ventilasi rumah dengan baik',
                'Tidak perlu masker khusus'
            ],
            'Moderate': [
                'Aktivitas outdoor masih aman',
                'Kelompok sensitif sebaiknya membatasi aktivitas outdoor berkepanjangan',
                'Perhatikan kondisi jika ada gejala respirasi'
            ],
            'Unhealthy for Sensitive Groups': [
                'Kelompok sensitif sebaiknya mengurangi aktivitas outdoor',
                'Gunakan masker N95 jika harus ke luar',
                'Gunakan air purifier di dalam ruangan'
            ],
            'Unhealthy': [
                'Hindari aktivitas outdoor',
                'Gunakan masker N95 jika harus ke luar',
                'Tutup jendela dan pintu',
                'Gunakan air purifier'
            ],
            'Very Unhealthy': [
                'Tetap di dalam ruangan',
                'Gunakan air purifier',
                'Hindari semua aktivitas outdoor',
                'Kelompok berisiko sebaiknya konsultasi dokter'
            ]
        }
        
        return recommendations.get(air_quality_status, [])
    
    def predict_and_classify(self, features, model_type='random_forest'):
        """Prediksi dan klasifikasi sekaligus"""
        prediction = self.predict_single(features, model_type)
        classification = self.classify_air_quality(prediction)
        recommendations = self.get_recommendations(classification['status'])
        
        result = {
            'pm25_predicted': float(prediction),
            'air_quality': classification,
            'recommendations': recommendations,
            'who_standard': self.who_standards['pm2_5'],
            'who_ratio': float(prediction / self.who_standards['pm2_5'])
        }
        
        return result
    
    def batch_predict(self, X, model_type='random_forest'):
        """Prediksi untuk batch data"""
        if model_type == 'random_forest' and self.rf_model:
            predictions = self.rf_model.predict(X)
        elif model_type == 'gradient_boosting' and self.gb_model:
            predictions = self.gb_model.predict(X)
        else:
            raise ValueError(f"Model {model_type} not available")
        
        results = []
        for pred in predictions:
            classification = self.classify_air_quality(pred)
            results.append({
                'pm25_predicted': float(pred),
                'status': classification['status'],
                'color': classification['color'],
                'who_compliant': classification['who_compliant']
            })
        
        return results
    
    def compare_models(self, features):
        """Bandingkan prediksi dari semua model"""
        results = {}
        
        if self.rf_model:
            rf_pred = self.rf_model.predict(features)[0]
            results['random_forest'] = {
                'prediction': float(rf_pred),
                'classification': self.classify_air_quality(rf_pred)
            }
        
        if self.gb_model:
            gb_pred = self.gb_model.predict(features)[0]
            results['gradient_boosting'] = {
                'prediction': float(gb_pred),
                'classification': self.classify_air_quality(gb_pred)
            }
        
        # Ensemble
        if results:
            ensemble_pred = np.mean([v['prediction'] for v in results.values()])
            results['ensemble'] = {
                'prediction': float(ensemble_pred),
                'classification': self.classify_air_quality(ensemble_pred)
            }
        
        return results


def main():
    """Main function untuk testing prediction"""
    predictor = AirQualityPredictor()
    
    print("Loading models...")
    predictor.load_models()
    
    # Load test data
    print("\nLoading test data...")
    test_df = pd.read_csv('data/test_data.csv')
    X_test = test_df.drop('target', axis=1)
    y_test = test_df['target']
    
    # Sample prediction
    print("\n" + "="*50)
    print("Sample Predictions")
    print("="*50)
    
    for i in range(min(5, len(X_test))):
        sample = X_test.iloc[i:i+1]
        actual = y_test.iloc[i]
        
        result = predictor.predict_and_classify(sample, model_type='random_forest')
        
        print(f"\nSample {i+1}:")
        print(f"  Actual PM2.5: {actual:.2f} μg/m³")
        print(f"  Predicted PM2.5: {result['pm25_predicted']:.2f} μg/m³")
        print(f"  Air Quality Status: {result['air_quality']['status']}")
        print(f"  WHO Compliant: {result['air_quality']['who_compliant']}")
        print(f"  WHO Ratio: {result['who_ratio']:.2f}x")
        print(f"  Recommendations:")
        for rec in result['recommendations']:
            print(f"    - {rec}")
    
    # Compare models
    print("\n" + "="*50)
    print("Model Comparison (Sample 1)")
    print("="*50)
    
    sample = X_test.iloc[0:1]
    comparison = predictor.compare_models(sample)
    
    for model_name, result in comparison.items():
        print(f"\n{model_name.upper()}:")
        print(f"  Prediction: {result['prediction']:.2f} μg/m³")
        print(f"  Status: {result['classification']['status']}")


if __name__ == "__main__":
    main()
