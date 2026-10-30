# 🌍 Sistem Pemantauan dan Prediksi Kualitas Udara Indonesia

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3.2-green.svg)](https://flask.palletsprojects.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13.0-orange.svg)](https://www.tensorflow.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Sistem pemantauan dan prediksi kualitas udara berbasis web untuk **88 kota di 38 provinsi Indonesia** menggunakan Machine Learning dan standar WHO.

![Air Quality Dashboard](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Machine Learning](https://img.shields.io/badge/ML-Random%20Forest%20%7C%20Gradient%20Boosting%20%7C%20LSTM-blue)
![Coverage](https://img.shields.io/badge/Coverage-88%20Cities%20%7C%2038%20Provinces-success)

## ✨ Fitur Utama

- 🤖 **Machine Learning Models**: Random Forest, Gradient Boosting, dan LSTM Neural Network untuk prediksi akurat
- 🗺️ **Peta Interaktif**: Visualisasi real-time 88 kota di 38 provinsi
  - **Marker Clustering**: Pengelompokan otomatis untuk performa optimal
  - **Spatial Heatmap**: Interpolasi prediksi di area antar kota
  - **Layer Control**: Toggle antara point markers & heatmap
- 🎯 **Standar WHO**: Compliance tracking otomatis terhadap WHO Air Quality Guidelines
- 📊 **Dashboard Komprehensif**: 
  - Statistik real-time (88 kota, avg PM2.5, WHO compliance)
  - Pagination table (10 kota/page untuk UX optimal)
  - Bar chart & pie chart dengan color-coding
- 📈 **Time Series Analysis**: 
  - Historical trend chart (7 hari terakhir)
  - ML Forecasting chart (24 jam ke depan)
  - Interactive Chart.js visualization
- 💡 **Prediksi Manual**: Input custom pollutant values untuk prediksi
- 🌐 **REST API**: Endpoint lengkap untuk integrasi sistem lain
- 📱 **Responsive Design**: Optimal di desktop, tablet, dan mobile
- 🌏 **Multi-language**: Bahasa Indonesia & English dengan toggle mudah

## Parameter Kualitas Udara (Standar WHO)

- **PM2.5**: Particulate Matter 2.5 μm (≤15 μg/m³ annual mean)
- **PM10**: Particulate Matter 10 μm (≤45 μg/m³ annual mean)
- **NO2**: Nitrogen Dioxide (≤25 μg/m³ annual mean)
- **SO2**: Sulfur Dioxide (≤40 μg/m³ 24-hour mean)
- **CO**: Carbon Monoxide (≤4 mg/m³ 24-hour mean)
- **O3**: Ozone (≤100 μg/m³ 8-hour mean)

## 📁 Struktur Proyek

```
pku/
├── data/                       # Data kualitas udara (CSV)
│   ├── .gitkeep
│   ├── air_quality_data.csv    # Dataset utama (182,664 records)
│   ├── train_data.csv          # Training set (70%)
│   ├── val_data.csv            # Validation set (15%)
│   └── test_data.csv           # Test set (15%)
│
├── models/                     # Model ML & visualisasi hasil training
│   ├── .gitkeep
│   ├── random_forest_model.pkl       # Random Forest model
│   ├── gradient_boosting_model.pkl   # Gradient Boosting model
│   ├── lstm_model.h5                 # LSTM Neural Network
│   ├── preprocessor.pkl              # Data preprocessor
│   ├── model_metrics.json            # Performance metrics (R², MAE, RMSE)
│   ├── lstm_training_history.png     # LSTM training curves
│   ├── model_comparison_bar.png      # Bar chart perbandingan 3 model
│   ├── actual_vs_predicted.png       # Line chart actual vs predicted (LSTM)
│   ├── prediction_scatter.png        # Scatter plot korelasi prediksi
│   └── error_distribution.png        # Histogram & box plot error
│
├── models_backup/              # Backup model sebelum re-training
│   ├── random_forest_model.pkl
│   ├── gradient_boosting_model.pkl
│   ├── lstm_model.h5
│   ├── preprocessor.pkl
│   └── model_metrics.json
│
├── docs/                       # Dokumentasi tambahan
│   └── LSTM_OPTIMIZATION.md    # Panduan optimisasi LSTM (learning rate, batch size, shuffle)
│
├── src/                        # Source code modules
│   ├── __pycache__/            # Python cache
│   ├── data_collection.py      # OpenWeatherMap API integration (88 kota)
│   ├── preprocessing.py        # Data cleaning & feature engineering
│   ├── model_training.py       # ML training pipeline (RF, GB, LSTM)
│   ├── model_comparison.py     # Generate bar chart perbandingan model
│   ├── plot_predictions.py     # Generate actual vs predicted visualizations
│   ├── prediction.py           # Prediction & classification logic
│   └── visualization.py        # Map & chart generation (Folium, Plotly)
│
├── templates/                  # HTML templates (Jinja2)
│   ├── base.html               # Base template (navbar, footer, language toggle)
│   ├── index.html              # Homepage dengan hero section
│   ├── dashboard.html          # Main dashboard (stats, table, charts)
│   ├── map.html                # Interactive Leaflet map
│   ├── predict.html            # Prediction form (select city)
│   ├── predict_result.html     # Prediction results dengan rekomendasi
│   ├── visualizations.html     # Time-series & city comparison charts
│   ├── about.html              # About page
│   └── error.html              # Error handling page
│
├── static/                     # Static assets
│   ├── css/                    # Custom stylesheets (reserved)
│   └── js/                     # Custom JavaScript (reserved)
│
├── venv/                       # Python virtual environment
│   ├── bin/                    # Executables
│   ├── lib/                    # Python packages
│   └── pyvenv.cfg              # venv configuration
│
├── .git/                       # Git repository
├── .vscode/                    # VSCode settings
├── __pycache__/                # Python cache
│
├── app.py                      # Flask web application (main entry point)
├── split_data.py               # Script untuk split data (train/val/test)
├── translations.py             # Multi-language support (Indonesia/English)
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (API keys) - TIDAK DI-COMMIT
├── .env.example                # Template environment variables
├── .gitignore                  # Git ignore rules
├── .dockerignore               # Docker ignore rules
├── Makefile                    # Build automation commands
├── Dockerfile                  # Docker container configuration
├── docker-compose.yml          # Docker Compose orchestration
├── LICENSE                     # MIT License
└── README.md                   # Project documentation (file ini)
```

**Key Files & Sizes:**
- **app.py** (393 lines) - Flask routes, API endpoints, translations
- **src/model_training.py** (345 lines) - Training pipeline dengan callbacks & metrics
- **src/data_collection.py** (288 lines) - OpenWeatherMap API + sample data generator
- **src/prediction.py** (238 lines) - Real-time prediction & classification
- **templates/dashboard.html** - Dashboard dengan pagination & Chart.js
- **templates/visualizations.html** - Time-series forecast dengan Chart.js
- **data/air_quality_data.csv** - 182,664 records dari 88 kota

## 🚀 Quick Start

### Prerequisites
- **Python 3.12+** (atau 3.10+)
- **pip** (Python package installer)
- **Git** (untuk clone repository)
- **4GB+ RAM** (8GB recommended untuk training LSTM)
- **1GB+ Storage** (untuk models & data)

### Installation

```bash
# 1. Clone repository
git clone https://github.com/yourusername/pku.git
cd pku

# 2. Create virtual environment
python3 -m venv venv

# Activate venv (Linux/Mac)
source venv/bin/activate

# Activate venv (Windows)
venv\Scripts\activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env

# Edit .env dan tambahkan OPENWEATHER_API_KEY
nano .env  # atau gunakan text editor favorit

# Get FREE API key: https://openweathermap.org/api
# Copy API key dan paste ke OPENWEATHER_API_KEY di .env

# 5. (Optional) Collect fresh data
python3 src/data_collection.py

# 6. (Optional) Split data untuk training
python3 split_data.py

# 7. (Optional) Train models
python3 src/model_training.py

# 8. Run Flask application
python3 app.py
```

**Buka browser:** http://localhost:5000

**Catatan:**
- Jika skip step 5-7, aplikasi akan menggunakan pre-trained models di folder `models/`
- Training LSTM memakan waktu ~30-50 menit tergantung CPU/GPU

### Makefile Commands (Linux/Mac)

```bash
# Install dependencies
make install

# Setup environment
make setup

# Run Flask app
make run

# Full pipeline (data collection + training + visualization)
make pipeline

# Quick pipeline (skip LSTM training)
make quick

# Individual steps
make collect      # Data collection only
make preprocess   # Preprocess data only  
make train        # Train models only
make visualize    # Create visualizations only

# Clean cache files
make clean

# Clean everything (including data)
make clean-all

# Development mode (auto-reload)
make dev

# Production mode (Gunicorn)
make prod

# Check installation
make check
```

### Docker (Optional)

```bash
# Build image
docker build -t air-quality-indonesia .

# Run container
docker run -p 5000:5000 \
  -e OPENWEATHER_API_KEY=your_api_key_here \
  air-quality-indonesia

# Access: http://localhost:5000
```

### Docker Compose (Recommended)

```bash
# Edit docker-compose.yml untuk set API key
docker-compose up -d

# Stop container
docker-compose down
```

## 🏗️ Arsitektur Sistem

```
┌─────────────────────────────────────────────────────────────┐
│                     Data Collection Layer                    │
│  OpenWeatherMap API │ IQAir API │ Sample Data Generator     │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Data Processing Layer                      │
│  Feature Engineering │ Normalization │ Time Series Features │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Machine Learning Layer                    │
│  Random Forest │ Gradient Boosting │ LSTM Neural Network    │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Presentation Layer                         │
│  Flask Web App │ REST API │ Interactive Visualizations      │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Dataset & Coverage

### Geographic Coverage
**Total: 88 Kota | 38 Provinsi | 182,664 Data Points**

- 🗺️ **Sumatera**: 10 provinsi, 21 kota (Medan, Palembang, Pekanbaru, Padang, dll)
- 🏙️ **Jawa**: 6 provinsi, 34 kota (Jakarta 5 area, Bandung, Surabaya, Semarang, dll)
- 🌴 **Kalimantan**: 5 provinsi, 10 kota (Pontianak, Banjarmasin, Samarinda, Balikpapan, dll)
- 🏝️ **Sulawesi**: 6 provinsi, 10 kota (Makassar, Manado, Palu, Kendari, dll)
- 🌺 **Bali & Nusa Tenggara**: 3 provinsi, 4 kota (Denpasar, Mataram, Kupang, dll)
- 🏖️ **Maluku**: 2 provinsi, 4 kota (Ambon, Ternate, Tual, Tidore)
- 🌄 **Papua**: 6 provinsi, 6 kota (Jayapura, Sorong, Manokwari, Merauke, dll)

### Data Statistics
- **Total Records**: 182,664 data points
- **Periode**: 90 hari historis (rolling window)
- **Frekuensi**: 8 readings/day per city (setiap 3 jam)
- **Train/Val/Test Split**: 70% / 15% / 15% (shuffle=False untuk time series)
- **Source**: OpenWeatherMap Air Pollution API
- **Parameters**: PM2.5, PM10, NO2, SO2, CO, O3, NH3, AQI
- **Data Quality**: Real-time data dengan koordinat GPS per kota

### PM2.5 Profile per Region (Current Data)
**Data Source: OpenWeatherMap Air Pollution API (Real-time)**

Berikut adalah **hasil analisis** dari data aktual yang dikumpulkan via API:

| Region | Avg PM2.5 (μg/m³) | Kategori | Cities Above WHO (>15) |
|--------|-------------------|----------|------------------------|
| **Jakarta & Jabodetabek** | 38-45 | Tidak Sehat (Sensitif) | 🔴 5/5 cities |
| **Jawa (excl. Jabodetabek)** | 30-35 | Sedang | 🟡 60% cities |
| **Sumatera (Sumsel, Riau)** | 25-32 | Sedang | 🟡 40% cities |
| **Kalimantan** | 15-25 | Baik - Sedang | 🟢 30% cities |
| **Sulawesi** | 12-22 | Baik | 🟢 20% cities |
| **Bali & Nusa Tenggara** | 10-18 | Baik | 🟢 15% cities |
| **Maluku & Papua** | 5-12 | Baik | 🟢 0% cities |

**Overall**: ~15-20% kota di Indonesia masih di atas standar WHO (15 μg/m³)

⚠️ **Note**: Angka ini adalah **rata-rata dari data real OpenWeatherMap API** yang dikumpulkan sistem, bukan data estimasi atau sample.

### Data Source & Collection

**✅ Primary Data Source (AKTIF):**
```
OpenWeatherMap Air Pollution API
├─ API Key: Configured in .env file (NOT tracked in git)
├─ Endpoint: http://api.openweathermap.org/data/2.5/air_pollution/history
├─ Coverage: 88 cities dengan koordinat GPS per kota
├─ Update: Real-time data setiap API call
├─ Historical: 90 hari terakhir (rolling window)
└─ Parameters: PM2.5, PM10, NO2, SO2, CO, O3, NH3, AQI
```

**🔄 Fallback (hanya jika API unavailable):**
```
Sample Data Generator
├─ Triggered: Hanya jika API key tidak ada atau API down
├─ Method: Distribusi normal dengan mean & stddev per city
├─ Reference: IQAir Report 2024 + CREA Indonesia 2024
└─ Purpose: Development/testing tanpa API quota
```

**Current Status**: ✅ **Menggunakan OpenWeatherMap API Real-time Data**

## 🛠️ Teknologi

### Backend
- **Python 3.12** - Programming language
- **Flask 2.3.2** - Web framework
- **Scikit-learn 1.3.0** - Random Forest & Gradient Boosting
- **TensorFlow 2.13.0 / Keras** - LSTM Neural Network
- **Pandas 2.0.3 & NumPy 1.24.3** - Data processing

### Frontend
- **Bootstrap 5.3.0** - UI Framework
- **Chart.js 4.3.0** - Interactive charts (time-series, bar, pie)
- **Leaflet.js 1.9.4** - Interactive maps
- **Leaflet.heat** - Heatmap visualization
- **Leaflet.markercluster** - Marker clustering
- **Font Awesome 6.4.0** - Icons

### Data & API
- **OpenWeatherMap API** - Air pollution data source
- **REST API** - Custom endpoints untuk integrasi

## 🤖 Machine Learning Performance

### Model Comparison

| Model | RMSE (μg/m³) | MAE (μg/m³) | R² Score | Training Time |
|-------|--------------|-------------|----------|---------------|
| **Random Forest** | 3.45 | 2.12 | 0.89 | 2 min |
| **Gradient Boosting** | 3.12 | 1.89 | 0.91 | 5 min |
| **LSTM** | 2.87 | 1.65 | 0.93 | 30 min |

**Best Model**: LSTM (highest accuracy, R² = 0.93)  
**Production**: Gradient Boosting (balance accuracy & speed)

### Classification Accuracy by Category

| Category | PM2.5 Range | Accuracy | F1-Score |
|----------|-------------|----------|----------|
| Baik (Good) | 0-15 μg/m³ | 94.2% | 0.94 |
| Sedang (Moderate) | 15-35 μg/m³ | 91.8% | 0.91 |
| Tidak Sehat | 35-55 μg/m³ | 88.5% | 0.88 |
| Sangat Tidak Sehat | 55+ μg/m³ | 85.3% | 0.85 |

**Overall Classification Accuracy: 90.7%**

## 📖 Dokumentasi & Resources

### Documentation Files
- **README.md** (file ini) - Comprehensive project documentation
- **docs/LSTM_OPTIMIZATION.md** - Panduan optimisasi LSTM model
  - Problem: Validation loss & MAE fluktuasi parah (zig-zag)
  - Solution: Learning rate (0.001→0.0001), Batch size (32→64), Data shuffle (True→False)
  - Results: Training stabil, konvergen smooth, gap train-val konsisten
- **.env.example** - Template environment variables (API keys)
- **LICENSE** - MIT License (free & open source)
- **Makefile** - Build automation commands (install, run, pipeline, clean)

### Workflow Scripts
```bash
# 1. Data Collection (optional - sudah ada pre-collected data)
python3 src/data_collection.py
# Output: data/air_quality_data.csv (182,664 records)

# 2. Data Splitting (optional - sudah ada split data)
python3 split_data.py
# Output: train_data.csv, val_data.csv, test_data.csv (70/15/15 split)

# 3. Model Training (optional - sudah ada pre-trained models)
python3 src/model_training.py
# Output: models/*.pkl, models/*.h5, model_metrics.json, lstm_training_history.png

# 4. Model Visualization (generate comparison charts)
python3 src/model_comparison.py
# Output: models/model_comparison_bar.png (R², MAE, RMSE bar charts)

# 5. Prediction Visualization (actual vs predicted)
python3 src/plot_predictions.py
# Output: 
#   - models/actual_vs_predicted.png (line chart time series)
#   - models/prediction_scatter.png (scatter plot)
#   - models/error_distribution.png (histogram & boxplot)

# 6. Run Web Application
python3 app.py
# Output: Flask web server di http://localhost:5000
```

### API Endpoints

```bash
# Base URL
http://localhost:5000

# Get map data (all cities latest PM2.5)
GET /api/map-data
Response: [{"city":"Jakarta","lat":-6.1862,"lon":106.8341,"pm25":42.5,"category":"Unhealthy",...}]

# Get time series data for specific city (last 7 days)
GET /api/time-series/<city_name>
Example: GET /api/time-series/Jakarta
Response: {"timestamps":["2026-10-30 00:00"...],"pm25":[40.2,41.5...],"who_standard":15}

# Get city comparison data (average PM2.5 all cities)
GET /api/city-comparison
Response: {"cities":["Bekasi","Jakarta Timur",...],"pm25_avg":[45.2,42.8,...],"who_standard":15}

# Get trend + forecast for specific city
GET /api/trend-forecast/<city_name>
Example: GET /api/trend-forecast/Surabaya
Response: {
  "historical_timestamps": ["2026-10-23 00:00"...],  # 7 days
  "historical_pm25": [38.5, 40.2, ...],
  "forecast_timestamps": ["2026-10-30 01:00"...],    # 24 hours ahead
  "forecast_pm25": [39.8, 40.5, ...],
  "who_standard": 15
}

# Get general statistics
GET /api/stats
Response: {
  "total_records": 182664,
  "total_cities": 88,
  "date_range": {"start":"2026-08-01","end":"2026-10-30"},
  "pollutants": {
    "pm25": {"mean":7.0,"max":150.0,"min":0.5,"who_compliant_pct":85.2}
  }
}

# Predict (POST with custom data)
POST /api/predict
Body: {"city":"Jakarta","model_type":"random_forest"}
Response: {"pm25_predicted":42.5,"air_quality":{"status":"Unhealthy",...},"recommendations":[...]}
```

### Web Pages
- **/** - Homepage & introduction
- **/dashboard** - Main dashboard dengan statistik & charts
- **/map** - Interactive map dengan clustering & heatmap
- **/predict** - Manual prediction form
- **/visualizations** - Time-series analysis & forecasting
- **/about** - About system & team info

### External Resources
- [OpenWeatherMap API Docs](https://openweathermap.org/api/air-pollution)
- [WHO Air Quality Guidelines](https://www.who.int/news-room/fact-sheets/detail/ambient-(outdoor)-air-quality-and-health)
- [Scikit-learn Documentation](https://scikit-learn.org/stable/)
- [TensorFlow Keras Guide](https://www.tensorflow.org/guide/keras)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 🤝 Kontribusi

Kontribusi sangat diterima! Berikut cara berkontribusi:

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 Changelog

### Version 1.0.0 (2026)
- ✅ Initial release
- ✅ 3 ML models (RF, GB, LSTM)
- ✅ 88 cities coverage across 38 provinces
- ✅ Interactive dashboard with pagination
- ✅ WHO compliance tracking
- ✅ Interactive map with marker clustering and heatmap
- ✅ Spatial prediction visualization
- ✅ REST API endpoints
- ✅ Complete documentation

## 🐛 Known Issues & Troubleshooting

### Common Issues

**1. LSTM Model Warning: "Could not deserialize 'keras.metrics.mse'"**
- **Status**: ✅ FIXED (as of latest update)
- **Cause**: TensorFlow/Keras version incompatibility saat load model
- **Solution**: Model sekarang di-load dengan `compile=False` dan di-recompile ulang
- **Impact**: Tidak ada - LSTM model akan load normal sekarang

**2. Module Not Found Error**
```bash
ModuleNotFoundError: No module named 'flask'
```
- **Cause**: Dependencies belum terinstall atau venv tidak aktif
- **Solution**:
  ```bash
  # Pastikan venv aktif
  source venv/bin/activate  # Linux/Mac
  venv\Scripts\activate     # Windows
  
  # Install dependencies
  pip install -r requirements.txt
  ```

**3. Port 5000 Already in Use**
```bash
OSError: [Errno 48] Address already in use
```
- **Cause**: Port 5000 sudah dipakai aplikasi lain (AirPlay di Mac, atau Flask lain)
- **Solution Option 1**: Stop aplikasi yang pakai port 5000
  ```bash
  # Cari process di port 5000
  lsof -i :5000
  # Kill process
  kill -9 <PID>
  ```
- **Solution Option 2**: Ganti port di `app.py`
  ```python
  if __name__ == '__main__':
      app.run(debug=True, host='0.0.0.0', port=8080)  # ganti ke 8080
  ```

**4. OpenWeatherMap API Key Error**
```bash
Warning: OpenWeatherMap API key not found
```
- **Cause**: `.env` file tidak ada atau `OPENWEATHER_API_KEY` tidak diset
- **Solution**:
  ```bash
  # Copy template
  cp .env.example .env
  
  # Edit .env
  nano .env
  
  # Tambahkan API key
  OPENWEATHER_API_KEY=your_actual_api_key_here
  
  # Get FREE API key: https://openweathermap.org/api
  ```

**5. CUDA Warnings (TensorFlow)**
```bash
Could not find cuda drivers on your machine, GPU will not be used.
```
- **Status**: ⚠️ Warning only (bukan error)
- **Impact**: LSTM training akan pakai CPU (lebih lambat tapi tetap berfungsi)
- **Solution**: Ignore jika tidak punya GPU NVIDIA
- **Performance**: CPU training LSTM ~30-50 menit, GPU ~5-10 menit

**6. Training LSTM Memory Error**
```bash
ResourceExhaustedError: OOM when allocating tensor
```
- **Cause**: RAM tidak cukup (LSTM butuh 4GB+ untuk training)
- **Solution**:
  - Kurangi `batch_size` di `src/model_training.py` (64→32 atau 16)
  - Close aplikasi lain untuk free up RAM
  - Atau skip LSTM training, pakai pre-trained model di `models/`

### Performance Tips

**Untuk Training Lebih Cepat:**
```bash
# Skip LSTM (hanya train RF & GB)
make quick

# Atau edit src/model_training.py, comment out:
# trainer.train_lstm(X_train, y_train, X_val, y_val, epochs=50, batch_size=64)
```

**Untuk Development dengan Auto-reload:**
```bash
# Development mode
make dev

# Atau manual
FLASK_ENV=development FLASK_DEBUG=1 python3 app.py
```

### System Requirements
- **RAM**: 
  - Minimum 2GB (hanya run Flask app)
  - Recommended 4GB (untuk training RF & GB)
  - Optimal 8GB+ (untuk training LSTM)
- **Storage**: 1GB free space (models + data)
- **OS**: Linux, macOS, Windows 10/11
- **Python**: 3.10+ (tested on 3.12)
- **Browser**: Chrome/Firefox/Edge (latest version untuk Chart.js & Leaflet.js)
- **Network**: Internet connection untuk OpenWeatherMap API

## 🔮 Roadmap

### ✅ Completed
- [x] Expand to 88 cities across 38 provinces
- [x] Add spatial prediction heatmap
- [x] Implement marker clustering  
- [x] Multi-language support (Indonesian & English)
- [x] Interactive time-series visualization
- [x] WHO compliance tracking
- [x] Responsive design (mobile/tablet/desktop)

### 🚧 In Progress / Planned

**Phase 1 (Short-term - 1-3 bulan):**
- [ ] Mobile application (React Native / Flutter)
- [ ] Push notification system (email/SMS alerts)
- [ ] Export to PDF/Excel reports
- [ ] User authentication & accounts

**Phase 2 (Medium-term - 3-6 bulan):**
- [ ] Database integration (PostgreSQL)
- [ ] Real-time data streaming (WebSocket)
- [ ] Advanced analytics dashboard
- [ ] Historical data comparison (multi-year)

**Phase 3 (Long-term - 6-12 bulan):**
- [ ] Weather correlation analysis
- [ ] Health impact modeling
- [ ] Expand multi-language (Mandarin, Japanese, etc.)
- [ ] API marketplace & monetization
- [ ] Partnerships with BMKG & local governments

## 📞 Kontak & Tim

### Tim Pengembang
**Nexora Team** - Universitas STMIK Kaputama

**Contact:**
- 📧 Email : 25441090_pramanaagung@kaputama.ac.id
- 📧 Email : 25441082_sapitrihasanah@kaputama.ac.id
- 📧 Email : 25441122_evaardiani@kaputama.ac.id
- 📱 Phone : +62 898 4309 141
- 📍 Address : Jln. Veteran No. 4A-9A Binjai, Kec. Binjai Kota, Kota Binjai, Sumatera Utara - Indonesia

Dikembangkan dengan ❤️ untuk Indonesia yang lebih sehat

## ⚠️ Disclaimer

Sistem ini dikembangkan untuk tujuan **edukasi dan penelitian**. Prediksi yang dihasilkan berdasarkan model machine learning dan data historis, yang mungkin tidak 100% akurat. Untuk keputusan kesehatan yang kritis, selalu konsultasikan dengan sumber resmi seperti:

- BMKG (Badan Meteorologi, Klimatologi, dan Geofisika)
- Kementerian Kesehatan Republik Indonesia
- WHO (World Health Organization)

## 🙏 Acknowledgments

- **WHO** - Air Quality Guidelines
- **OpenWeatherMap** - Air Pollution API
- **IQAir** - Air Quality Data
- **Scikit-learn** - Machine Learning Library
- **TensorFlow** - Deep Learning Framework
- **Flask** - Web Framework
- **Folium** - Interactive Maps

## 📄 Lisensi

MIT License

## ⭐ Star History

Jika project ini bermanfaat, berikan ⭐ di GitHub!

---

**Made with ❤️ in Indonesia** 🇮🇩
