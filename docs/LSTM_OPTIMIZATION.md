# Optimisasi LSTM untuk Mengatasi Fluktuasi Training

## 🔍 Masalah yang Diidentifikasi

Berdasarkan analisis grafik training history, ditemukan 3 masalah utama:

### 1. Validation Loss & MAE Mengalami Fluktuasi Parah (Zig-zag)
- Garis Val Loss dan Val MAE (oranye) naik-turun drastis dari epoch ke epoch
- Menandakan proses pembelajaran model sangat tidak stabil

### 2. Train Loss & Validation Loss Tidak Konvergen Berdampingan
- Train Loss turun perlahan di ~54.0
- Val Loss berada di bawahnya (~53.6 - 54.0) dengan pola tidak beraturan
- Mengindikasikan data leakage atau pembagian dataset tidak tepat untuk time-series

### 3. Learning Rate Terlalu Tinggi
- Optimizer melompati titik minimum lokal saat update bobot

---

## ✅ Solusi yang Diterapkan

### 1. **Learning Rate Diturunkan** (Critical Fix)

**File**: `src/model_training.py`

```python
# SEBELUM (Learning Rate terlalu tinggi)
optimizer=keras.optimizers.Adam(learning_rate=0.001)

# SESUDAH (Learning Rate optimal untuk stabilitas)
optimizer=keras.optimizers.Adam(learning_rate=0.0001)
```

**Dampak**: 
- Learning rate diturunkan dari `0.001` → `0.0001` (10x lebih kecil)
- Mengurangi fluktuasi gradien dan membuat konvergensi lebih stabil
- Update bobot lebih halus dan konsisten

---

### 2. **Data Splitting Tanpa Shuffle** (Critical Fix untuk Time Series)

**File**: `split_data.py`

```python
# SEBELUM (SALAH untuk time series - data diacak!)
train_df, temp_df = train_test_split(df_processed, test_size=0.3, random_state=42, shuffle=True)

# SESUDAH (BENAR untuk time series - urutan temporal dijaga)
train_df, temp_df = train_test_split(df_processed, test_size=0.3, random_state=42, shuffle=False)
```

**Dampak**:
- **shuffle=False** memastikan urutan waktu tetap terjaga
- LSTM dapat mempelajari pola temporal dengan benar
- Menghilangkan data leakage yang terjadi saat data time series diacak
- Train/Val/Test split sekarang mengikuti urutan kronologis

**PENTING**: Ini adalah masalah paling kritis! Mengacak data time series akan membuat:
- Model "melihat masa depan" saat training (data leakage)
- LSTM kehilangan kemampuan mempelajari pola temporal
- Validasi loss tidak dapat dipercaya

---

### 3. **Batch Size Dinaikkan**

**File**: `src/model_training.py`

```python
# SEBELUM (Batch size terlalu kecil)
def train_lstm(..., batch_size=32):

# SESUDAH (Batch size optimal)
def train_lstm(..., batch_size=64):
```

**Dampak**:
- Batch size dinaikkan dari `32` → `64` (2x lebih besar)
- Estimasi gradien lebih stabil dan smooth
- Mengurangi noise dalam update parameter
- Training lebih cepat dan efisien

---

### 4. **Callback Patience Dinaikkan**

**File**: `src/model_training.py`

```python
# Early Stopping patience: 10 → 15 epoch
# ReduceLROnPlateau patience: 5 → 7 epoch
# Verbose ditambahkan untuk monitoring
```

**Dampak**:
- Patience dinaikkan untuk mengakomodasi learning rate yang lebih rendah
- Model punya waktu lebih banyak untuk konvergen
- Verbose memberikan feedback real-time saat training

---

## 🚀 Cara Menjalankan Ulang Training

### Langkah 1: Re-split Data dengan Urutan Temporal yang Benar
```bash
python3 split_data.py
```

**Output yang diharapkan**:
```
✓ Saved train_data.csv (X columns)
✓ Saved val_data.csv (X columns)
✓ Saved test_data.csv (X columns)
```

### Langkah 2: Training Ulang Model dengan Parameter Baru
```bash
python3 src/model_training.py
```

**Monitoring saat training**:
- Perhatikan epoch progress
- ReduceLROnPlateau akan muncul jika val_loss plateau
- Early stopping akan berhenti jika tidak ada improvement

---

## 📊 Hasil yang Diharapkan

Setelah optimisasi ini, grafik training history seharusnya menunjukkan:

### ✅ Karakteristik Training yang Baik:
1. **Val Loss turun secara smooth** (tidak zig-zag)
2. **Train Loss dan Val Loss konvergen berdampingan** dengan gap yang konsisten
3. **MAE turun secara konsisten** tanpa fluktuasi besar
4. **Gap Train-Val Loss stabil** (menandakan tidak ada overfitting/underfitting)

### 📈 Contoh Pattern yang Diharapkan:
```
Epoch 10: loss: 52.3, val_loss: 53.1, mae: 5.4, val_mae: 5.6
Epoch 20: loss: 48.7, val_loss: 49.2, mae: 5.1, val_mae: 5.2
Epoch 30: loss: 46.2, val_loss: 46.8, mae: 4.9, val_mae: 5.0
...
```

---

## 🎯 Parameter Summary

| Parameter | Sebelum | Sesudah | Alasan |
|-----------|---------|---------|--------|
| **Learning Rate** | 0.001 | 0.0001 | Mengurangi fluktuasi gradient |
| **Batch Size** | 32 | 64 | Estimasi gradient lebih stabil |
| **Data Shuffle** | True ❌ | False ✅ | Jaga urutan temporal untuk time series |
| **Early Stop Patience** | 10 | 15 | Lebih toleran dengan LR rendah |
| **ReduceLR Patience** | 5 | 7 | Lebih toleran dengan LR rendah |

---

## 🔧 Troubleshooting

### Jika Val Loss masih fluktuatif:
1. Coba turunkan learning rate lebih lanjut ke `0.00005`
2. Naikkan batch size ke `128` (jika RAM cukup)
3. Tambahkan dropout lebih besar (0.3 atau 0.4)

### Jika Train Loss tidak turun:
1. Naikkan learning rate sedikit ke `0.0002`
2. Kurangi regularization (dropout)
3. Pastikan data sudah dinormalisasi dengan benar

### Jika Overfitting (Val Loss > Train Loss jauh):
1. Naikkan dropout rate
2. Tambahkan L2 regularization
3. Kurangi kompleksitas model (jumlah unit LSTM)

---

## 📝 Catatan Penting

⚠️ **WAJIB menjalankan `split_data.py` ulang** sebelum training!
- Data lama sudah ter-shuffle (salah untuk time series)
- Data baru akan menggunakan urutan temporal yang benar

⚠️ **Backup model lama** sudah ada di `models_backup/`

⚠️ **Monitoring training** sangat penting:
- Lihat apakah val_loss turun smooth
- Cek apakah early stopping trigger atau tidak
- Perhatikan kapan ReduceLROnPlateau aktif

---

## 📚 Referensi
Bukti kualitatif bahwa hasil prediksi menempel presisi dengan data kejadian di lapangan.
- [Time Series Forecasting Best Practices](https://www.tensorflow.org/tutorials/structured_data/time_series)
- [LSTM Hyperparameter Tuning](https://keras.io/guides/keras_tuner/)
- [Avoiding Data Leakage in Time Series](https://machinelearningmastery.com/train-test-split-for-evaluating-machine-learning-algorithms/)

---

**Dibuat**: Oktober 2026  
**Versi**: 1.0  
**Status**: Implementasi selesai, siap untuk re-training
