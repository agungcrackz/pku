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
│   ├── air_quality_data.csv    # Dataset utama (180K+ records)
│   ├── train_data.csv          # Training set
│   ├── val_data.csv            # Validation set
│   └── test_data.csv           # Test set
│
├── models/                     # Model ML yang sudah di-training
│   ├── random_forest_model.pkl       # Random Forest (16MB)
│   ├── gradient_boosting_model.pkl   # Gradient Boosting (448KB)
│   ├── lstm_model.h5                 # LSTM Neural Network (624KB)
│   ├── preprocessor.pkl              # Data preprocessor (4KB)
│   ├── model_metrics.json            # Performance metrics
│   └── lstm_training_history.png     # Training visualization
│
├── models_backup/              # Backup model files
│
├── src/                        # Source code modules
│   ├── data_collection.py      # OpenWeatherMap API integration
│   ├── preprocessing.py        # Data cleaning & feature engineering
│   ├── model_training.py       # ML model training pipeline
│   ├── prediction.py           # Prediction & inference logic
│   └── visualization.py        # Map & chart generation
│
├── templates/                  # HTML templates (Jinja2)
│   ├── base.html               # Base template dengan navbar/footer
│   ├── index.html              # Homepage
│   ├── dashboard.html          # Main dashboard
│   ├── map.html                # Interactive map
│   ├── predict.html            # Prediction form
│   ├── predict_result.html     # Prediction results
│   ├── visualizations.html     # Time-series charts
│   ├── about.html              # About page
│   └── error.html              # Error page
│
├── static/                     # Static assets
│   ├── css/                    # Custom stylesheets (currently empty)
│   └── js/                     # Custom JavaScript (currently empty)
│
├── app.py                      # Flask web application (main entry point)
├── translations.py             # Multi-language support (ID/EN)
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── Makefile                    # Build automation commands
├── Dockerfile                  # Docker container configuration
├── docker-compose.yml          # Docker Compose orchestration
├── LICENSE                     # MIT License
└── README.md                   # Project documentation (this file)
```

**Key Files:**
- **app.py** (393 lines) - Flask routes, API endpoints, error handling
- **src/model_training.py** - Model training & evaluation pipeline
- **src/prediction.py** - Real-time prediction engine
- **templates/dashboard.html** - Main dashboard with charts & tables
- **templates/map.html** - Interactive Leaflet map with clustering & heatmap

## 🚀 Quick Start

### Prerequisites
- Python 3.12 atau lebih tinggi
- pip (Python package installer)
- Git (untuk clone repository)
- 4GB+ RAM (untuk training LSTM)

### Installation

```bash
# 1. Clone repository
git clone https://github.com/agungcrackz/pku.git
cd pku

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env dan tambahkan OPENWEATHER_API_KEY Anda
# Dapatkan FREE API key di: https://openweathermap.org/api

# 5. Run application
python app.py
```

**Buka browser:** http://localhost:5000

### Makefile Commands (Linux/Mac)

```bash
make install    # Install dependencies
make run        # Run Flask app
make clean      # Clean cache files
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
**Total: 88 Kota | 38 Provinsi | 180,576+ Data Points**

- 🗺️ **Sumatera**: 10 provinsi, 20 kota
- 🏙️ **Jawa**: 6 provinsi, 34 kota (Jakarta, Bandung, Surabaya, dll)
- 🌴 **Kalimantan**: 5 provinsi, 10 kota
- 🏝️ **Sulawesi**: 6 provinsi, 10 kota
- 🌺 **Bali & Nusa Tenggara**: 3 provinsi, 4 kota
- 🏖️ **Maluku**: 2 provinsi, 4 kota
- 🌄 **Papua**: 6 provinsi, 6 kota

### Data Statistics
- **Periode**: Juli - Oktober 2026 (3 bulan)
- **Frekuensi**: 8 readings/day per city
- **Total Records**: 180,576 data points
- **Source**: OpenWeatherMap Air Pollution API
- **Parameters**: PM2.5, PM10, NO2, SO2, CO, O3, NH3, AQI
- **Data Quality**: 98% completeness, validated & cleaned

### Data Source
Sistem menggunakan data dari:
- **Primary**: OpenWeatherMap Air Pollution API (real-time)
- **Alternative**: IQAir API, BMKG data
- **Storage**: CSV format untuk portability

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
- **README.md** (file ini) - Overview, installation & quick start guide
- **.env.example** - Template environment variables
- **LICENSE** - MIT License details
- **Makefile** - Build automation commands

### API Endpoints

```bash
# Get all cities data
GET http://localhost:5000/api/cities

# Get specific city data
GET http://localhost:5000/api/city/<city_name>

# Get prediction for specific city
GET http://localhost:5000/api/predict/<city_name>

# Health check
GET http://localhost:5000/api/health
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

**1. LSTM Model Error: "Could not deserialize 'keras.metrics.mse'"**
- **Cause**: TensorFlow version mismatch
- **Solution**: Model akan auto-skip, Random Forest & Gradient Boosting tetap berfungsi normal

**2. Module Not Found Error**
- **Cause**: Dependencies belum terinstall
- **Solution**: Pastikan virtual environment aktif, jalankan `pip install -r requirements.txt`

**3. Port 5000 Already in Use**
- **Cause**: Port sudah dipakai aplikasi lain
- **Solution**: Edit `app.py` ganti port, atau stop aplikasi yang pakai port 5000

**4. API Key Error**
- **Cause**: OPENWEATHER_API_KEY tidak diset atau invalid
- **Solution**: Cek file `.env`, pastikan API key valid dari OpenWeatherMap

### System Requirements
- **RAM**: Minimum 4GB (8GB recommended untuk LSTM)
- **Storage**: 500MB free space
- **OS**: Linux, macOS, Windows 10/11
- **Browser**: Chrome/Firefox/Edge (latest version)

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
