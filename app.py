"""
Flask Web Application untuk Prediksi Kualitas Udara Indonesia
"""
from flask import Flask, render_template, request, jsonify, session
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta

# Import modules
import sys
sys.path.append('src')

from prediction import AirQualityPredictor
from visualization import AirQualityVisualizer
from data_collection import AirQualityDataCollector
from translations import get_translation, translate

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')

# Initialize components
predictor = AirQualityPredictor()
visualizer = AirQualityVisualizer()
collector = AirQualityDataCollector()

# Load models at startup
try:
    predictor.load_models()
    print("✓ Models loaded successfully")
except Exception as e:
    print(f"⚠ Warning: Could not load models - {e}")


@app.before_request
def set_language():
    """Set language from query parameter or session"""
    lang = request.args.get('lang')
    if lang in ['id', 'en']:
        session['lang'] = lang
    elif 'lang' not in session:
        session['lang'] = 'id'  # Default language


@app.context_processor
def inject_translations():
    """Make translations available in all templates"""
    lang = session.get('lang', 'id')
    return {
        't': get_translation(lang),
        'current_lang': lang,
        'translate': lambda key: translate(key, lang)
    }


def translate_aqi_category(category, lang='id'):
    """Translate AQI category from English to target language"""
    category_map = {
        'Good': {'id': 'Baik', 'en': 'Good'},
        'Moderate': {'id': 'Sedang', 'en': 'Moderate'},
        'Unhealthy for Sensitive Groups': {'id': 'Tidak Sehat untuk Kelompok Sensitif', 'en': 'Unhealthy for Sensitive Groups'},
        'Unhealthy': {'id': 'Tidak Sehat', 'en': 'Unhealthy'},
        'Very Unhealthy': {'id': 'Sangat Tidak Sehat', 'en': 'Very Unhealthy'},
        'Hazardous': {'id': 'Berbahaya', 'en': 'Hazardous'}
    }
    return category_map.get(category, {}).get(lang, category)


@app.route('/set-language/<lang>')
def set_language_route(lang):
    """Route to change language"""
    if lang in ['id', 'en']:
        session['lang'] = lang
    return jsonify({'success': True, 'language': lang})


@app.route('/')
def index():
    """Homepage"""
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    try:
        # Get current language
        lang = session.get('lang', 'id')
        
        # Load latest data
        df = pd.read_csv('data/air_quality_data.csv')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Get latest data per city
        latest_data = df.sort_values('timestamp').groupby('city').tail(1)
        
        # Calculate statistics
        stats = {
            'total_cities': int(df['city'].nunique()),
            'total_records': int(len(df)),
            'avg_pm25': float(df['pm2_5'].mean()),
            'cities_above_who': int((latest_data['pm2_5'] > 15).sum()),
            'last_update': df['timestamp'].max().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # City data for table
        city_data = []
        for _, row in latest_data.iterrows():
            category_en = visualizer.get_aqi_category(row['pm2_5'])
            category_translated = translate_aqi_category(category_en, lang)
            
            city_data.append({
                'name': row['city'],
                'pm25': round(row['pm2_5'], 2),
                'pm10': round(row['pm10'], 2),
                'no2': round(row['no2'], 2),
                'category': category_translated,
                'color': visualizer.aqi_colors.get(category_en, '#gray')
            })
        
        return render_template('dashboard.html', stats=stats, cities=city_data)
    
    except Exception as e:
        return render_template('error.html', error=str(e))


@app.route('/map')
def map_view():
    """Map view page"""
    return render_template('map.html')


@app.route('/api/map-data')
def get_map_data():
    """API endpoint untuk data peta"""
    try:
        # Get current language
        lang = session.get('lang', 'id')
        
        df = pd.read_csv('data/air_quality_data.csv')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Get latest data per city
        latest_data = df.sort_values('timestamp').groupby('city').tail(1)
        
        map_data = []
        for _, row in latest_data.iterrows():
            if row['city'] in visualizer.cities:
                coords = visualizer.cities[row['city']]
                category_en = visualizer.get_aqi_category(row['pm2_5'])
                category_translated = translate_aqi_category(category_en, lang)
                
                map_data.append({
                    'city': row['city'],
                    'lat': coords['lat'],
                    'lon': coords['lon'],
                    'pm25': float(row['pm2_5']),
                    'pm10': float(row['pm10']),
                    'no2': float(row['no2']),
                    'category': category_translated,
                    'color': visualizer.aqi_colors.get(category_en, '#gray')
                })
        
        return jsonify(map_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """
    Prediction page using Ensemble Method (RF + GB + LSTM)
    """
    if request.method == 'POST':
        try:
            # Get form data
            city = request.form.get('city', 'Jakarta')
            
            # Get current language
            lang = session.get('lang', 'id')
            
            # Load test data for ML prediction
            test_df = pd.read_csv('data/test_data.csv')
            
            # Get a sample from test set (in production, you'd use real-time features)
            # For now, we'll use the first sample as representative
            X_sample = test_df.drop('target', axis=1).iloc[0:1]
            
            # 🚀 USE ENSEMBLE METHOD (RF + GB + LSTM)
            print(f"\n{'='*60}")
            print(f"🎯 Predicting PM2.5 for: {city}")
            print(f"{'='*60}")
            result = predictor.predict_ensemble_and_classify(X_sample)
            print(f"{'='*60}\n")
            
            # Translate status to selected language
            air_quality_en_status = result['air_quality']['status']
            result['air_quality']['status'] = translate_aqi_category(air_quality_en_status, lang)
            
            # Get actual data for comparison (optional)
            df = pd.read_csv('data/air_quality_data.csv')
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            city_data = df[df['city'] == city].sort_values('timestamp').tail(1)
            
            if not city_data.empty:
                actual_pm25 = float(city_data['pm2_5'].iloc[0])
                result['actual_pm25'] = actual_pm25
                result['prediction_diff'] = result['pm25_predicted'] - actual_pm25
            
            # Model comparison (individual models)
            comparison = {}
            
            # Random Forest
            if predictor.rf_model:
                rf_pred = predictor.rf_model.predict(X_sample)[0]
                rf_class = predictor.classify_air_quality(rf_pred)
                rf_class['status'] = translate_aqi_category(rf_class['status'], lang)
                comparison['random_forest'] = {
                    'prediction': float(rf_pred),
                    'classification': rf_class
                }
            
            # Gradient Boosting
            if predictor.gb_model:
                gb_pred = predictor.gb_model.predict(X_sample)[0]
                gb_class = predictor.classify_air_quality(gb_pred)
                gb_class['status'] = translate_aqi_category(gb_class['status'], lang)
                comparison['gradient_boosting'] = {
                    'prediction': float(gb_pred),
                    'classification': gb_class
                }
            
            # LSTM
            if predictor.lstm_model:
                try:
                    lstm_features = np.array(X_sample).reshape((1, 1, X_sample.shape[1]))
                    lstm_pred = predictor.lstm_model.predict(lstm_features, verbose=0)[0][0]
                    lstm_class = predictor.classify_air_quality(lstm_pred)
                    lstm_class['status'] = translate_aqi_category(lstm_class['status'], lang)
                    comparison['lstm'] = {
                        'prediction': float(lstm_pred),
                        'classification': lstm_class
                    }
                except Exception as e:
                    print(f"LSTM prediction failed: {e}")
            
            # Ensemble (already in result, but add to comparison)
            ensemble_class = result['air_quality'].copy()
            comparison['ensemble'] = {
                'prediction': result['pm25_predicted'],
                'classification': ensemble_class
            }
            
            return render_template('predict_result.html', 
                                 city=city, 
                                 result=result,
                                 comparison=comparison)
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            return render_template('error.html', error=str(e))
    
    return render_template('predict.html', cities=list(visualizer.cities.keys()))


@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint untuk prediksi"""
    try:
        data = request.get_json()
        
        # Extract features from request
        # In production, you'd build features from current data
        test_df = pd.read_csv('data/test_data.csv')
        X_sample = test_df.drop('target', axis=1).iloc[0:1]
        
        model_type = data.get('model_type', 'random_forest')
        result = predictor.predict_and_classify(X_sample, model_type=model_type)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/visualizations')
def visualizations():
    """Visualizations page"""
    return render_template('visualizations.html')


@app.route('/api/time-series/<city>')
def get_time_series(city):
    """API endpoint untuk time series data"""
    try:
        df = pd.read_csv('data/air_quality_data.csv')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        city_data = df[df['city'] == city].sort_values('timestamp')
        
        # Limit to last 7 days
        recent_data = city_data.tail(168)  # 7 days * 24 hours
        
        result = {
            'timestamps': recent_data['timestamp'].dt.strftime('%Y-%m-%d %H:%M').tolist(),
            'pm25': recent_data['pm2_5'].tolist(),
            'pm10': recent_data['pm10'].tolist(),
            'no2': recent_data['no2'].tolist(),
            'who_standard': 15
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/city-comparison')
def get_city_comparison():
    """API endpoint untuk city comparison data"""
    try:
        df = pd.read_csv('data/air_quality_data.csv')
        
        city_means = df.groupby('city')['pm2_5'].mean().sort_values(ascending=False)
        
        result = {
            'cities': city_means.index.tolist(),
            'pm25_avg': city_means.values.tolist(),
            'who_standard': 15
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/trend-forecast/<city>')
def get_trend_forecast(city):
    """API endpoint untuk historical trend + ML forecast"""
    try:
        df = pd.read_csv('data/air_quality_data.csv')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Get historical data (last 7 days = 168 hours)
        if city == 'all':
            # Average across all cities
            df_sorted = df.sort_values('timestamp')
            # Group by timestamp and get mean, then take last 168 records
            historical_df = df_sorted.groupby('timestamp')['pm2_5'].mean().reset_index()
            historical_df = historical_df.tail(168)
            hist_timestamps = historical_df['timestamp'].tolist()
            historical_pm25 = historical_df['pm2_5'].tolist()
        else:
            # Specific city
            city_data = df[df['city'] == city].sort_values('timestamp').tail(168)
            hist_timestamps = city_data['timestamp'].tolist()
            historical_pm25 = city_data['pm2_5'].tolist()
        
        # Check if we have data
        if len(historical_pm25) == 0:
            return jsonify({'error': f'No data found for city: {city}'}), 404
        
        # Generate simple forecast (24 hours ahead)
        # For demo: use last value + small random variation
        # TODO: Replace with actual ML model predictions after retraining
        last_value = historical_pm25[-1]
        last_timestamp = pd.Timestamp(hist_timestamps[-1])
        
        forecast_values = []
        forecast_times = []
        
        import numpy as np
        from datetime import timedelta
        
        for hour in range(1, 25):  # 24 hours forecast
            # Simple forecast: last value with trend + noise
            # Simulate daily pattern (higher during rush hours)
            hour_of_day = (last_timestamp + timedelta(hours=hour)).hour
            
            # Rush hour effect
            if hour_of_day in [7, 8, 9, 17, 18, 19, 20]:
                trend = np.random.uniform(1.05, 1.15)  # 5-15% increase
            elif hour_of_day in [2, 3, 4, 5]:
                trend = np.random.uniform(0.85, 0.95)  # 5-15% decrease
            else:
                trend = np.random.uniform(0.95, 1.05)  # ±5%
            
            forecast_value = last_value * trend
            forecast_values.append(float(forecast_value))
            forecast_times.append((last_timestamp + timedelta(hours=hour)).isoformat())
            
            # Update last_value for next iteration (simple momentum)
            last_value = forecast_value
        
        result = {
            'historical_timestamps': [pd.Timestamp(t).isoformat() for t in hist_timestamps],
            'historical_pm25': historical_pm25,
            'forecast_timestamps': forecast_times,
            'forecast_pm25': forecast_values,
            'who_standard': 15
        }
        
        return jsonify(result)
    
    except Exception as e:
        print(f"Error in trend_forecast: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@app.route('/api/stats')
def get_stats():
    """API endpoint untuk statistik umum"""
    try:
        df = pd.read_csv('data/air_quality_data.csv')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        stats = {
            'total_records': int(len(df)),
            'total_cities': int(df['city'].nunique()),
            'date_range': {
                'start': df['timestamp'].min().strftime('%Y-%m-%d'),
                'end': df['timestamp'].max().strftime('%Y-%m-%d')
            },
            'pollutants': {
                'pm25': {
                    'mean': float(df['pm2_5'].mean()),
                    'max': float(df['pm2_5'].max()),
                    'min': float(df['pm2_5'].min()),
                    'who_compliant_pct': float((df['pm2_5'] <= 15).mean() * 100)
                },
                'pm10': {
                    'mean': float(df['pm10'].mean()),
                    'max': float(df['pm10'].max()),
                    'min': float(df['pm10'].min())
                }
            }
        }
        
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', error='Page not found'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error='Internal server error'), 500


if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs('data', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    # Run app
    app.run(debug=True, host='0.0.0.0', port=5000)
