"""
Script untuk membuat visualisasi perbandingan model
Menghasilkan bar chart untuk membandingkan metrik R², MAE, dan RMSE
antara Random Forest, Gradient Boosting, dan LSTM
"""
import json
import matplotlib.pyplot as plt
import numpy as np
import os


def load_metrics():
    """Load metrics dari file JSON"""
    metrics_path = 'models/model_metrics.json'
    
    if not os.path.exists(metrics_path):
        raise FileNotFoundError(
            f"File {metrics_path} tidak ditemukan!\n"
            "Pastikan Anda sudah menjalankan training terlebih dahulu:\n"
            "  python3 src/model_training.py"
        )
    
    with open(metrics_path, 'r') as f:
        metrics = json.load(f)
    
    return metrics


def create_comparison_chart(metrics, save_path='models/model_comparison_bar.png'):
    """Membuat bar chart perbandingan model"""
    
    # Ambil data untuk setiap model
    models = []
    r2_scores = []
    mae_scores = []
    rmse_scores = []
    
    # Map nama model untuk label yang lebih rapi
    model_labels = {
        'random_forest': 'Random Forest',
        'gradient_boosting': 'Gradient Boosting',
        'lstm': 'LSTM'
    }
    
    # Prioritaskan test metrics, jika tidak ada gunakan val metrics
    for model_name, model_label in model_labels.items():
        if model_name in metrics:
            model_data = metrics[model_name]
            
            # Gunakan test metrics jika ada, fallback ke val metrics
            if 'test_r2' in model_data:
                r2 = model_data['test_r2']
                mae = model_data['test_mae']
                rmse = model_data['test_rmse']
                dataset_type = 'Test'
            else:
                r2 = model_data['val_r2']
                mae = model_data['val_mae']
                rmse = model_data['val_rmse']
                dataset_type = 'Validation'
            
            models.append(model_label)
            r2_scores.append(r2)
            mae_scores.append(mae)
            rmse_scores.append(rmse)
    
    if not models:
        raise ValueError("Tidak ada data model yang ditemukan dalam metrics!")
    
    # Setup plot dengan 3 subplot
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Perbandingan Performa Model Air Quality Prediction', 
                 fontsize=16, fontweight='bold', y=1.02)
    
    # Warna untuk setiap model
    colors = ['#3498db', '#2ecc71', '#e74c3c']  # Blue, Green, Red
    
    x_pos = np.arange(len(models))
    bar_width = 0.6
    
    # 1. R² Score (semakin tinggi semakin baik)
    axes[0].bar(x_pos, r2_scores, bar_width, color=colors, alpha=0.8, edgecolor='black', linewidth=1.2)
    axes[0].set_xlabel('Model', fontsize=11, fontweight='bold')
    axes[0].set_ylabel('R² Score', fontsize=11, fontweight='bold')
    axes[0].set_title('R² Score\n(Semakin tinggi semakin baik)', fontsize=12, fontweight='bold')
    axes[0].set_xticks(x_pos)
    axes[0].set_xticklabels(models, rotation=15, ha='right')
    axes[0].set_ylim([0, 1])
    axes[0].grid(axis='y', alpha=0.3, linestyle='--')
    
    # Tambahkan nilai di atas bar
    for i, (model, score) in enumerate(zip(models, r2_scores)):
        axes[0].text(i, score + 0.02, f'{score:.4f}', 
                     ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # 2. MAE (semakin rendah semakin baik)
    axes[1].bar(x_pos, mae_scores, bar_width, color=colors, alpha=0.8, edgecolor='black', linewidth=1.2)
    axes[1].set_xlabel('Model', fontsize=11, fontweight='bold')
    axes[1].set_ylabel('MAE', fontsize=11, fontweight='bold')
    axes[1].set_title('Mean Absolute Error (MAE)\n(Semakin rendah semakin baik)', fontsize=12, fontweight='bold')
    axes[1].set_xticks(x_pos)
    axes[1].set_xticklabels(models, rotation=15, ha='right')
    axes[1].grid(axis='y', alpha=0.3, linestyle='--')
    
    # Tambahkan nilai di atas bar
    for i, (model, score) in enumerate(zip(models, mae_scores)):
        axes[1].text(i, score + max(mae_scores)*0.02, f'{score:.2f}', 
                     ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # 3. RMSE (semakin rendah semakin baik)
    axes[2].bar(x_pos, rmse_scores, bar_width, color=colors, alpha=0.8, edgecolor='black', linewidth=1.2)
    axes[2].set_xlabel('Model', fontsize=11, fontweight='bold')
    axes[2].set_ylabel('RMSE', fontsize=11, fontweight='bold')
    axes[2].set_title('Root Mean Squared Error (RMSE)\n(Semakin rendah semakin baik)', fontsize=12, fontweight='bold')
    axes[2].set_xticks(x_pos)
    axes[2].set_xticklabels(models, rotation=15, ha='right')
    axes[2].grid(axis='y', alpha=0.3, linestyle='--')
    
    # Tambahkan nilai di atas bar
    for i, (model, score) in enumerate(zip(models, rmse_scores)):
        axes[2].text(i, score + max(rmse_scores)*0.02, f'{score:.2f}', 
                     ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Tambahkan keterangan dataset di bawah
    fig.text(0.5, -0.02, f'Data: {dataset_type} Set', 
             ha='center', fontsize=10, style='italic', color='gray')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"\n✅ Grafik perbandingan model berhasil disimpan ke: {save_path}")
    plt.close()
    
    # Print summary
    print("\n" + "="*60)
    print("📊 RINGKASAN PERBANDINGAN MODEL")
    print("="*60)
    
    # Cari model terbaik berdasarkan R²
    best_r2_idx = np.argmax(r2_scores)
    best_mae_idx = np.argmin(mae_scores)
    best_rmse_idx = np.argmin(rmse_scores)
    
    for i, model in enumerate(models):
        print(f"\n{model}:")
        print(f"  R² Score: {r2_scores[i]:.4f} {'🏆' if i == best_r2_idx else ''}")
        print(f"  MAE:      {mae_scores[i]:.2f} {'🏆' if i == best_mae_idx else ''}")
        print(f"  RMSE:     {rmse_scores[i]:.2f} {'🏆' if i == best_rmse_idx else ''}")
    
    # Kesimpulan
    print("\n" + "="*60)
    print("🎯 KESIMPULAN:")
    print("="*60)
    
    # Hitung score keseluruhan (normalize ke 0-1 dan rata-rata)
    # R² sudah 0-1, MAE dan RMSE perlu dinormalisasi (1 - normalized)
    overall_scores = []
    
    for i in range(len(models)):
        # R² score (higher is better)
        r2_normalized = r2_scores[i]
        
        # MAE score (lower is better, so invert)
        mae_normalized = 1 - (mae_scores[i] / max(mae_scores))
        
        # RMSE score (lower is better, so invert)
        rmse_normalized = 1 - (rmse_scores[i] / max(rmse_scores))
        
        # Overall score (rata-rata)
        overall = (r2_normalized + mae_normalized + rmse_normalized) / 3
        overall_scores.append(overall)
    
    best_overall_idx = np.argmax(overall_scores)
    
    print(f"Model terbaik secara keseluruhan: {models[best_overall_idx]} 🏆")
    print(f"  Overall Score: {overall_scores[best_overall_idx]:.4f}")
    
    print("\n" + "="*60)


def main():
    """Main function"""
    print("="*60)
    print("VISUALISASI PERBANDINGAN MODEL")
    print("="*60)
    
    try:
        # Load metrics
        print("\n📂 Loading model metrics...")
        metrics = load_metrics()
        print(f"✓ Loaded metrics untuk {len(metrics)} model(s)")
        
        # Create comparison chart
        print("\n📊 Membuat grafik perbandingan...")
        create_comparison_chart(metrics)
        
        print("\n" + "="*60)
        print("✅ SELESAI!")
        print("="*60)
        print("\nGrafik telah disimpan ke: models/model_comparison_bar.png")
        print("Anda dapat melihat perbandingan performa ketiga model.")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
    except Exception as e:
        print(f"\n❌ Error tidak terduga: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
