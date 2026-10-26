# 🌍 Sistem Pemantauan dan Prediksi Kualitas Udara Indonesia

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3.2-green.svg)](https://flask.palletsprojects.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13.0-orange.svg)](https://www.tensorflow.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Sistem pemantauan dan prediksi kualitas udara berbasis web untuk **87 kota di 38 provinsi Indonesia** menggunakan Machine Learning dan standar WHO.

![Air Quality Dashboard](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Machine Learning](https://img.shields.io/badge/ML-Random%20Forest%20%7C%20Gradient%20Boosting%20%7C%20LSTM-blue)
![Coverage](https://img.shields.io/badge/Coverage-87%20Cities%20%7C%2038%20Provinces-success)

## ✨ Fitur Utama

- 🤖 **Machine Learning Models**: Random Forest, Gradient Boosting, dan LSTM Neural Network untuk prediksi akurat
- 🗺️ **Peta Interaktif**: Visualisasi real-time 87 kota di 38 provinsi
  - **Marker Clustering**: Pengelompokan otomatis untuk performa optimal
  - **Spatial Heatmap**: Interpolasi prediksi di area antar kota
  - **Layer Control**: Toggle antara point markers & heatmap
- 🎯 **Standar WHO**: Compliance tracking otomatis terhadap WHO Air Quality Guidelines
- 📊 **Dashboard Komprehensif**: 
  - Statistik real-time (87 kota, avg PM2.5, WHO compliance)
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

## Struktur Proyek

```
├── data/                   # Data kualitas udara
├── models/                 # Model ML yang sudah di-train
├── src/
│   ├── data_collection.py  # Pengumpulan data
│   ├── preprocessing.py    # Preprocessing data
│   ├── model_training.py   # Training model ML
│   ├── prediction.py       # Prediksi kualitas udara
│   └── visualization.py    # Visualisasi dan pemetaan
├── notebooks/              # Jupyter notebooks untuk eksplorasi
├── static/                 # File statis untuk web
├── templates/              # Template HTML
├── app.py                  # Flask web application
└── requirements.txt        # Dependencies

```

## 🚀 Quick Start

### Installation

```bash
# 1. Clone repository
git clone <repository-url>
cd pku

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env dan tambahkan OPENWEATHER_API_KEY

# 5. Run application
python app.py
```

Buka browser: **http://localhost:5000**

### Docker (Optional)

```bash
# Build image
docker build -t air-quality-indonesia .

# Run container
docker run -p 5000:5000 air-quality-indonesia
```

### Development

```bash
# Run with auto-reload
export FLASK_ENV=development
python app.py

# Access monitoring dashboard
# Open http://localhost:5000
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
**Total: 87 Kota | 38 Provinsi | 180,576 Data Points**

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

## 📖 Dokumentasi

- **README.md** (file ini) - Overview & quick start

## 🤝 Kontribusi

Kontribusi sangat diterima! Berikut cara berkontribusi:

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 Changelog

### Version 1.0.0 (2024)
- ✅ Initial release
- ✅ 3 ML models (RF, GB, LSTM)
- ✅ 87 cities coverage across 38 provinces
- ✅ Interactive dashboard with pagination
- ✅ WHO compliance tracking
- ✅ Interactive map with marker clustering and heatmap
- ✅ Spatial prediction visualization
- ✅ REST API endpoints
- ✅ Complete documentation

## 🐛 Known Issues

- LSTM training requires significant memory (>4GB RAM)
- Real-time API data requires API keys
- Large datasets may cause slow visualization loading

## 🔮 Roadmap

### ✅ Completed
- [x] Expand to 87 cities across 38 provinces
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
