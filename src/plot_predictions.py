"""
Script untuk membuat visualisasi Actual vs Predicted
Plot grafik garis waktu (time series) yang menumpukkan data aktual dengan
hasil prediksi dari model LSTM
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
import joblib
import os


def load_models_and_data():
    """Load model dan data test"""
    print("📂 Loading model dan data...")
    
    # Load LSTM model
    if not os.path.exists('models/lstm_model.h5'):
        raise FileNotFoundError(
            "Model LSTM tidak ditemukan!\n"
            "Pastikan Anda sudah menjalankan training:\n"
            "  python3 src/model_training.py"
        )
    
    # Custom objects for backward compatibility
    from tensorflow.keras import metrics
    custom_objects = {
        'mse': metrics.MeanSquaredError(),
        'mae': metrics.MeanAbsoluteError()
    }
    
    try:
        # Try loading with custom objects
        lstm_model = keras.models.load_model('models/lstm_model.h5', 
                                            custom_objects=custom_objects,
                                            compile=False)
        # Recompile model
        lstm_model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )
        print("  ✓ LSTM model loaded (with custom objects)")
    except Exception as e:
        print(f"  ⚠ Warning: {e}")
        print("  Trying alternative loading method...")
        # Alternative: load without compilation
        lstm_model = keras.models.load_model('models/lstm_model.h5', compile=False)
        lstm_model.compile(
            optimizer='adam',
            loss='mse',
            metrics=['mae']
        )
        print("  ✓ LSTM model loaded (recompiled)")
    
    # Load test data
    if not os.path.exists('data/test_data.csv'):
        raise FileNotFoundError(
            "Test data tidak ditemukan!\n"
            "Pastikan Anda sudah menjalankan data splitting:\n"
            "  python3 split_data.py"
        )
    
    test_df = pd.read_csv('data/test_data.csv')
    print(f"  ✓ Test data loaded: {len(test_df)} records")
    
    return lstm_model, test_df


def prepare_lstm_sequences(X, y, time_steps=24):
    """Prepare data sequences untuk LSTM (sama seperti saat training)"""
    X_seq = []
    y_seq = []
    indices = []
    
    for i in range(time_steps, len(X)):
        X_seq.append(X[i-time_steps:i])
        y_seq.append(y[i])
        indices.append(i)
    
    return np.array(X_seq), np.array(y_seq), indices


def create_actual_vs_predicted_plot(y_actual, y_predicted, 
                                   sample_size=500,
                                   save_path='models/actual_vs_predicted.png'):
    """
    Membuat line chart actual vs predicted
    
    Args:
        y_actual: Array nilai aktual
        y_predicted: Array nilai prediksi
        sample_size: Jumlah sampel yang ditampilkan (default 500 untuk clarity)
        save_path: Path untuk menyimpan plot
    """
    
    # Ambil sampel untuk visualisasi (terlalu banyak data membuat plot susah dibaca)
    if len(y_actual) > sample_size:
        print(f"\n📊 Mengambil {sample_size} sampel terakhir untuk visualisasi...")
        y_actual_plot = y_actual[-sample_size:]
        y_predicted_plot = y_predicted[-sample_size:]
    else:
        y_actual_plot = y_actual
        y_predicted_plot = y_predicted
    
    # Create plot
    fig, ax = plt.subplots(figsize=(16, 6))
    
    x_axis = np.arange(len(y_actual_plot))
    
    # Plot actual vs predicted
    ax.plot(x_axis, y_actual_plot, 
            label='Data Aktual', 
            color='#2c3e50', 
            linewidth=2, 
            alpha=0.8,
            marker='o',
            markersize=3,
            markevery=max(1, len(x_axis)//50))  # Show markers sparsely
    
    ax.plot(x_axis, y_predicted_plot, 
            label='Prediksi LSTM', 
            color='#e74c3c', 
            linewidth=2, 
            alpha=0.7,
            linestyle='--',
            marker='s',
            markersize=3,
            markevery=max(1, len(x_axis)//50))
    
    # Styling
    ax.set_xlabel('Waktu (Time Steps)', fontsize=12, fontweight='bold')
    ax.set_ylabel('PM2.5 Concentration (μg/m³)', fontsize=12, fontweight='bold')
    ax.set_title('Grafik Prediksi vs Data Aktual (LSTM Model)\nActual vs Predicted Time Series', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper right', fontsize=11, framealpha=0.9)
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.7)
    
    # Tambahkan statistik
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    
    mae = mean_absolute_error(y_actual_plot, y_predicted_plot)
    rmse = np.sqrt(mean_squared_error(y_actual_plot, y_predicted_plot))
    r2 = r2_score(y_actual_plot, y_predicted_plot)
    
    # Text box dengan metrics
    textstr = f'MAE: {mae:.2f}\nRMSE: {rmse:.2f}\nR²: {r2:.4f}'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, 
            fontsize=11, verticalalignment='top', bbox=props)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"\n✅ Grafik actual vs predicted berhasil disimpan ke: {save_path}")
    plt.close()
    
    return mae, rmse, r2


def create_scatter_plot(y_actual, y_predicted, 
                       save_path='models/prediction_scatter.png'):
    """
    Membuat scatter plot untuk melihat korelasi actual vs predicted
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Scatter plot
    ax.scatter(y_actual, y_predicted, 
               alpha=0.5, 
               s=20, 
               color='#3498db',
               edgecolors='navy',
               linewidth=0.5)
    
    # Perfect prediction line (y=x)
    min_val = min(y_actual.min(), y_predicted.min())
    max_val = max(y_actual.max(), y_predicted.max())
    ax.plot([min_val, max_val], [min_val, max_val], 
            'r--', 
            linewidth=2, 
            label='Perfect Prediction (y=x)',
            alpha=0.8)
    
    # Styling
    ax.set_xlabel('Actual PM2.5 (μg/m³)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Predicted PM2.5 (μg/m³)', fontsize=12, fontweight='bold')
    ax.set_title('Scatter Plot: Actual vs Predicted\n(LSTM Model)', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper left', fontsize=11)
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Tambahkan R² pada plot
    from sklearn.metrics import r2_score
    r2 = r2_score(y_actual, y_predicted)
    ax.text(0.95, 0.05, f'R² = {r2:.4f}', 
            transform=ax.transAxes,
            fontsize=12,
            verticalalignment='bottom',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"✅ Scatter plot berhasil disimpan ke: {save_path}")
    plt.close()


def create_error_distribution_plot(y_actual, y_predicted,
                                   save_path='models/error_distribution.png'):
    """
    Membuat histogram distribusi error prediksi
    """
    errors = y_actual - y_predicted
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # 1. Histogram error
    axes[0].hist(errors, bins=50, color='#9b59b6', alpha=0.7, edgecolor='black')
    axes[0].axvline(x=0, color='red', linestyle='--', linewidth=2, label='Zero Error')
    axes[0].set_xlabel('Prediction Error (Actual - Predicted)', fontsize=11, fontweight='bold')
    axes[0].set_ylabel('Frequency', fontsize=11, fontweight='bold')
    axes[0].set_title('Distribusi Error Prediksi', fontsize=12, fontweight='bold')
    axes[0].legend()
    axes[0].grid(axis='y', alpha=0.3)
    
    # Tambahkan mean dan std
    mean_error = errors.mean()
    std_error = errors.std()
    axes[0].text(0.02, 0.98, 
                 f'Mean: {mean_error:.2f}\nStd: {std_error:.2f}',
                 transform=axes[0].transAxes,
                 fontsize=10,
                 verticalalignment='top',
                 bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # 2. Box plot error
    bp = axes[1].boxplot([errors], 
                         vert=True, 
                         patch_artist=True,
                         widths=0.5)
    
    # Customize box plot
    for patch in bp['boxes']:
        patch.set_facecolor('#e67e22')
        patch.set_alpha(0.7)
    
    # Add x-axis label manually
    axes[1].set_xticks([1])
    axes[1].set_xticklabels(['Prediction Error'])
    
    axes[1].axhline(y=0, color='red', linestyle='--', linewidth=2, label='Zero Error')
    axes[1].set_ylabel('Error (Actual - Predicted)', fontsize=11, fontweight='bold')
    axes[1].set_title('Box Plot Error Prediksi', fontsize=12, fontweight='bold')
    axes[1].legend()
    axes[1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"✅ Error distribution plot berhasil disimpan ke: {save_path}")
    plt.close()


def main():
    """Main function"""
    print("="*60)
    print("VISUALISASI ACTUAL VS PREDICTED (LSTM)")
    print("="*60)
    
    try:
        # Load model dan data
        lstm_model, test_df = load_models_and_data()
        
        # Prepare data
        print("\n📊 Preparing data untuk prediksi...")
        X_test = test_df.drop('target', axis=1).values
        y_test = test_df['target'].values
        
        # Create sequences
        time_steps = 24
        X_test_seq, y_test_seq, indices = prepare_lstm_sequences(X_test, y_test, time_steps)
        print(f"  ✓ Test sequences: {X_test_seq.shape}")
        
        # Predict
        print("\n🔮 Melakukan prediksi...")
        y_pred = lstm_model.predict(X_test_seq, verbose=0).flatten()
        print(f"  ✓ Prediksi selesai: {len(y_pred)} predictions")
        
        # Create visualizations
        print("\n📈 Membuat visualisasi...")
        print("-" * 60)
        
        # 1. Actual vs Predicted Line Chart (UTAMA)
        mae, rmse, r2 = create_actual_vs_predicted_plot(
            y_test_seq, 
            y_pred,
            sample_size=500  # Tampilkan 500 data point terakhir
        )
        
        # 2. Scatter Plot
        create_scatter_plot(y_test_seq, y_pred)
        
        # 3. Error Distribution
        create_error_distribution_plot(y_test_seq, y_pred)
        
        # Print summary
        print("\n" + "="*60)
        print("📊 RINGKASAN HASIL PREDIKSI")
        print("="*60)
        print(f"Total data test (setelah sequencing): {len(y_test_seq)}")
        print(f"\nMetrik Performa:")
        print(f"  MAE (Mean Absolute Error):  {mae:.4f}")
        print(f"  RMSE (Root Mean Squared Error): {rmse:.4f}")
        print(f"  R² Score: {r2:.4f}")
        
        print("\n" + "="*60)
        print("✅ SELESAI!")
        print("="*60)
        print("\nGrafik yang dihasilkan:")
        print("  1. models/actual_vs_predicted.png  (Line Chart - UTAMA)")
        print("  2. models/prediction_scatter.png   (Scatter Plot)")
        print("  3. models/error_distribution.png   (Error Analysis)")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
    except Exception as e:
        print(f"\n❌ Error tidak terduga: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
