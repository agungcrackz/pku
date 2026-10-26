"""
Multilingual support for Air Quality Prediction System
"""

TRANSLATIONS = {
    'id': {
        # Navigation
        'home': 'Home',
        'dashboard': 'Dashboard',
        'map': 'Peta',
        'predict': 'Prediksi',
        'visualizations': 'Visualisasi',
        'about': 'Tentang',
        
        # Common
        'language': 'Bahasa',
        'loading': 'Memuat...',
        'error': 'Error',
        'success': 'Berhasil',
        'back_to_home': 'Kembali ke Home',
        
        # Air Quality Status
        'good': 'Baik',
        'moderate': 'Sedang',
        'unhealthy_sensitive': 'Tidak Sehat untuk Kelompok Sensitif',
        'unhealthy': 'Tidak Sehat',
        'very_unhealthy': 'Sangat Tidak Sehat',
        'hazardous': 'Berbahaya',
        
        # WHO Standards
        'who_standards': 'Standar WHO',
        'who_compliant': 'Sesuai WHO',
        'who_non_compliant': 'Tidak Sesuai WHO',
        
        # Dashboard
        'total_cities': 'Total Kota',
        'avg_pm25': 'Rata-rata PM2.5',
        'cities_above_who': 'Kota Di Atas Standar WHO',
        'total_records': 'Total Data',
        'last_update': 'Terakhir Diperbarui',
        'city': 'Kota',
        'status': 'Status',
        'air_quality_per_city': 'Data Kualitas Udara per Kota',
        
        # Prediction
        'select_city': 'Pilih Kota',
        'run_prediction': 'Jalankan Prediksi',
        'prediction_parameters': 'Parameter Prediksi',
        'prediction_results': 'Hasil Prediksi',
        'predicted_pm25': 'PM2.5 Prediksi',
        'air_quality': 'Kualitas Udara',
        'recommendations': 'Rekomendasi',
        'model_comparison': 'Perbandingan Model',
        'predict_again': 'Prediksi Lagi',
        'view_dashboard': 'Lihat Dashboard',
        'view_map': 'Lihat Peta',
        
        # Health Recommendations
        'rec_good_1': 'Nikmati aktivitas outdoor',
        'rec_good_2': 'Ventilasi rumah dengan baik',
        'rec_good_3': 'Tidak perlu masker khusus',
        'rec_moderate_1': 'Aktivitas outdoor masih aman',
        'rec_moderate_2': 'Kelompok sensitif sebaiknya membatasi aktivitas outdoor berkepanjangan',
        'rec_moderate_3': 'Perhatikan kondisi jika ada gejala respirasi',
        'rec_unhealthy_sensitive_1': 'Kelompok sensitif sebaiknya mengurangi aktivitas outdoor',
        'rec_unhealthy_sensitive_2': 'Gunakan masker N95 jika harus ke luar',
        'rec_unhealthy_sensitive_3': 'Gunakan air purifier di dalam ruangan',
        'rec_unhealthy_1': 'Hindari aktivitas outdoor',
        'rec_unhealthy_2': 'Gunakan masker N95 jika harus ke luar',
        'rec_unhealthy_3': 'Tutup jendela dan pintu',
        'rec_unhealthy_4': 'Gunakan air purifier',
        'rec_very_unhealthy_1': 'Tetap di dalam ruangan',
        'rec_very_unhealthy_2': 'Gunakan air purifier',
        'rec_very_unhealthy_3': 'Hindari semua aktivitas outdoor',
        'rec_very_unhealthy_4': 'Kelompok berisiko sebaiknya konsultasi dokter',
        
        # About
        'about_title': 'Tentang Sistem',
        'about_description': 'Sistem prediksi dan pemetaan kualitas udara Indonesia berbasis Machine Learning dengan standar WHO',
        'main_features': 'Fitur Utama',
        'technology': 'Teknologi',
        'cities_monitored': 'Kota yang Dipantau',
        'disclaimer': 'Disclaimer',
        'disclaimer_text': 'Sistem ini dikembangkan untuk tujuan edukasi dan penelitian. Prediksi yang dihasilkan berdasarkan model machine learning dan data historis, yang mungkin tidak 100% akurat.',
        
        # Footer
        'system_description': 'Sistem prediksi dan pemetaan kualitas udara Indonesia berbasis Machine Learning dengan standar WHO.',
        'links': 'Links',
        'powered_by': 'Powered by Machine Learning',
        
        # Map
        'interactive_map': 'Peta Interaktif Indonesia',
        'air_quality_legend': 'Legenda Kualitas Udara',
        
        # Error messages
        'oops': 'Oops! Something went wrong',
        'model_not_available': 'Model random_forest not available',
        'no_data': 'No such file or directory',
    },
    
    'en': {
        # Navigation
        'home': 'Home',
        'dashboard': 'Dashboard',
        'map': 'Map',
        'predict': 'Predict',
        'visualizations': 'Visualizations',
        'about': 'About',
        
        # Common
        'language': 'Language',
        'loading': 'Loading...',
        'error': 'Error',
        'success': 'Success',
        'back_to_home': 'Back to Home',
        
        # Air Quality Status
        'good': 'Good',
        'moderate': 'Moderate',
        'unhealthy_sensitive': 'Unhealthy for Sensitive Groups',
        'unhealthy': 'Unhealthy',
        'very_unhealthy': 'Very Unhealthy',
        'hazardous': 'Hazardous',
        
        # WHO Standards
        'who_standards': 'WHO Standards',
        'who_compliant': 'WHO Compliant',
        'who_non_compliant': 'Not WHO Compliant',
        
        # Dashboard
        'total_cities': 'Total Cities',
        'avg_pm25': 'Average PM2.5',
        'cities_above_who': 'Cities Above WHO Standard',
        'total_records': 'Total Records',
        'last_update': 'Last Updated',
        'city': 'City',
        'status': 'Status',
        'air_quality_per_city': 'Air Quality Data per City',
        
        # Prediction
        'select_city': 'Select City',
        'run_prediction': 'Run Prediction',
        'prediction_parameters': 'Prediction Parameters',
        'prediction_results': 'Prediction Results',
        'predicted_pm25': 'Predicted PM2.5',
        'air_quality': 'Air Quality',
        'recommendations': 'Recommendations',
        'model_comparison': 'Model Comparison',
        'predict_again': 'Predict Again',
        'view_dashboard': 'View Dashboard',
        'view_map': 'View Map',
        
        # Health Recommendations
        'rec_good_1': 'Enjoy outdoor activities',
        'rec_good_2': 'Ventilate your home well',
        'rec_good_3': 'No special mask needed',
        'rec_moderate_1': 'Outdoor activities are still safe',
        'rec_moderate_2': 'Sensitive groups should limit prolonged outdoor activities',
        'rec_moderate_3': 'Monitor your condition if you have respiratory symptoms',
        'rec_unhealthy_sensitive_1': 'Sensitive groups should reduce outdoor activities',
        'rec_unhealthy_sensitive_2': 'Wear N95 mask if going outside',
        'rec_unhealthy_sensitive_3': 'Use air purifier indoors',
        'rec_unhealthy_1': 'Avoid outdoor activities',
        'rec_unhealthy_2': 'Wear N95 mask if going outside',
        'rec_unhealthy_3': 'Close windows and doors',
        'rec_unhealthy_4': 'Use air purifier',
        'rec_very_unhealthy_1': 'Stay indoors',
        'rec_very_unhealthy_2': 'Use air purifier',
        'rec_very_unhealthy_3': 'Avoid all outdoor activities',
        'rec_very_unhealthy_4': 'At-risk groups should consult doctor',
        
        # About
        'about_title': 'About System',
        'about_description': 'Air quality prediction and mapping system for Indonesia based on Machine Learning with WHO standards',
        'main_features': 'Main Features',
        'technology': 'Technology',
        'cities_monitored': 'Cities Monitored',
        'disclaimer': 'Disclaimer',
        'disclaimer_text': 'This system was developed for educational and research purposes. Predictions are based on machine learning models and historical data, which may not be 100% accurate.',
        
        # Footer
        'system_description': 'Air quality prediction and mapping system for Indonesia based on Machine Learning with WHO standards.',
        'links': 'Links',
        'powered_by': 'Powered by Machine Learning',
        
        # Map
        'interactive_map': 'Interactive Map of Indonesia',
        'air_quality_legend': 'Air Quality Legend',
        
        # Error messages
        'oops': 'Oops! Something went wrong',
        'model_not_available': 'Model random_forest not available',
        'no_data': 'No such file or directory',
    }
}


def get_translation(lang='id'):
    """Get translations for specified language"""
    return TRANSLATIONS.get(lang, TRANSLATIONS['id'])


def translate(key, lang='id'):
    """Translate a single key"""
    translations = get_translation(lang)
    return translations.get(key, key)
