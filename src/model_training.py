"""
Module untuk training model machine learning
"""
import pandas as pd
import numpy as np
import joblib
import json
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt
import os


class AirQualityModelTrainer:
    """Kelas untuk training model prediksi kualitas udara"""
    
    def __init__(self):
        self.rf_model = None
        self.gb_model = None
        self.lstm_model = None
        self.metrics = {}
    
    def load_data(self):
        """Load preprocessed data"""
        train_df = pd.read_csv('data/train_data.csv')
        val_df = pd.read_csv('data/val_data.csv')
        test_df = pd.read_csv('data/test_data.csv')
        
        X_train = train_df.drop('target', axis=1)
        y_train = train_df['target']
        
        X_val = val_df.drop('target', axis=1)
        y_val = val_df['target']
        
        X_test = test_df.drop('target', axis=1)
        y_test = test_df['target']
        
        return X_train, X_val, X_test, y_train, y_val, y_test
    
    def train_random_forest(self, X_train, y_train, X_val, y_val):
        """Train Random Forest model"""
        print("\nTraining Random Forest...")
        
        self.rf_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1,
            verbose=1
        )
        
        self.rf_model.fit(X_train, y_train)
        
        # Predictions
        train_pred = self.rf_model.predict(X_train)
        val_pred = self.rf_model.predict(X_val)
        
        # Metrics
        train_rmse = np.sqrt(mean_squared_error(y_train, train_pred))
        val_rmse = np.sqrt(mean_squared_error(y_val, val_pred))
        train_mae = mean_absolute_error(y_train, train_pred)
        val_mae = mean_absolute_error(y_val, val_pred)
        train_r2 = r2_score(y_train, train_pred)
        val_r2 = r2_score(y_val, val_pred)
        
        self.metrics['random_forest'] = {
            'train_rmse': float(train_rmse),
            'val_rmse': float(val_rmse),
            'train_mae': float(train_mae),
            'val_mae': float(val_mae),
            'train_r2': float(train_r2),
            'val_r2': float(val_r2)
        }
        
        print(f"  Train RMSE: {train_rmse:.4f}, MAE: {train_mae:.4f}, R²: {train_r2:.4f}")
        print(f"  Val RMSE: {val_rmse:.4f}, MAE: {val_mae:.4f}, R²: {val_r2:.4f}")
        
        return self.rf_model
    
    def train_gradient_boosting(self, X_train, y_train, X_val, y_val):
        """Train Gradient Boosting model"""
        print("\nTraining Gradient Boosting...")
        
        self.gb_model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            verbose=1
        )
        
        self.gb_model.fit(X_train, y_train)
        
        # Predictions
        train_pred = self.gb_model.predict(X_train)
        val_pred = self.gb_model.predict(X_val)
        
        # Metrics
        train_rmse = np.sqrt(mean_squared_error(y_train, train_pred))
        val_rmse = np.sqrt(mean_squared_error(y_val, val_pred))
        train_mae = mean_absolute_error(y_train, train_pred)
        val_mae = mean_absolute_error(y_val, val_pred)
        train_r2 = r2_score(y_train, train_pred)
        val_r2 = r2_score(y_val, val_pred)
        
        self.metrics['gradient_boosting'] = {
            'train_rmse': float(train_rmse),
            'val_rmse': float(val_rmse),
            'train_mae': float(train_mae),
            'val_mae': float(val_mae),
            'train_r2': float(train_r2),
            'val_r2': float(val_r2)
        }
        
        print(f"  Train RMSE: {train_rmse:.4f}, MAE: {train_mae:.4f}, R²: {train_r2:.4f}")
        print(f"  Val RMSE: {val_rmse:.4f}, MAE: {val_mae:.4f}, R²: {val_r2:.4f}")
        
        return self.gb_model
    
    def prepare_lstm_data(self, X, y, time_steps=24):
        """Prepare data untuk LSTM (sequence data)"""
        X_seq = []
        y_seq = []
        
        for i in range(time_steps, len(X)):
            X_seq.append(X[i-time_steps:i])
            y_seq.append(y[i])
        
        return np.array(X_seq), np.array(y_seq)
    
    def build_lstm_model(self, input_shape):
        """Build LSTM model"""
        model = keras.Sequential([
            layers.LSTM(64, return_sequences=True, input_shape=input_shape),
            layers.Dropout(0.2),
            layers.LSTM(32, return_sequences=False),
            layers.Dropout(0.2),
            layers.Dense(16, activation='relu'),
            layers.Dense(1)
        ])
        
        # Learning rate diturunkan untuk stabilitas training
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.0001),
            loss='mse',
            metrics=['mae']
        )
        
        return model
    
    def train_lstm(self, X_train, y_train, X_val, y_val, epochs=50, batch_size=64):
        """Train LSTM model dengan batch size lebih besar untuk stabilitas"""
        print("\nPreparing LSTM data...")
        
        # Convert to numpy arrays
        X_train_np = X_train.values if hasattr(X_train, 'values') else X_train
        X_val_np = X_val.values if hasattr(X_val, 'values') else X_val
        y_train_np = y_train.values if hasattr(y_train, 'values') else y_train
        y_val_np = y_val.values if hasattr(y_val, 'values') else y_val
        
        # Prepare sequences
        time_steps = 24
        X_train_seq, y_train_seq = self.prepare_lstm_data(X_train_np, y_train_np, time_steps)
        X_val_seq, y_val_seq = self.prepare_lstm_data(X_val_np, y_val_np, time_steps)
        
        print(f"LSTM training data shape: {X_train_seq.shape}")
        print(f"LSTM validation data shape: {X_val_seq.shape}")
        
        print("\nBuilding LSTM model...")
        self.lstm_model = self.build_lstm_model((time_steps, X_train_seq.shape[2]))
        
        print("\nTraining LSTM...")
        
        # Callbacks untuk stabilitas training
        early_stopping = keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=15,  # Patience dinaikkan untuk learning rate lebih rendah
            restore_best_weights=True,
            verbose=1
        )
        
        reduce_lr = keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=7,  # Patience dinaikkan
            min_lr=0.00001,
            verbose=1
        )
        
        # Train
        history = self.lstm_model.fit(
            X_train_seq, y_train_seq,
            validation_data=(X_val_seq, y_val_seq),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=[early_stopping, reduce_lr],
            verbose=1
        )
        
        # Metrics
        train_loss = history.history['loss'][-1]
        val_loss = history.history['val_loss'][-1]
        train_mae = history.history['mae'][-1]
        val_mae = history.history['val_mae'][-1]
        
        # Calculate R²
        train_pred = self.lstm_model.predict(X_train_seq, verbose=0)
        val_pred = self.lstm_model.predict(X_val_seq, verbose=0)
        train_r2 = r2_score(y_train_seq, train_pred)
        val_r2 = r2_score(y_val_seq, val_pred)
        
        self.metrics['lstm'] = {
            'train_rmse': float(np.sqrt(train_loss)),
            'val_rmse': float(np.sqrt(val_loss)),
            'train_mae': float(train_mae),
            'val_mae': float(val_mae),
            'train_r2': float(train_r2),
            'val_r2': float(val_r2),
            'epochs_trained': len(history.history['loss'])
        }
        
        print(f"\n  Train RMSE: {np.sqrt(train_loss):.4f}, MAE: {train_mae:.4f}, R²: {train_r2:.4f}")
        print(f"  Val RMSE: {np.sqrt(val_loss):.4f}, MAE: {val_mae:.4f}, R²: {val_r2:.4f}")
        
        # Plot training history
        self.plot_training_history(history)
        
        return self.lstm_model
    
    def plot_training_history(self, history):
        """Plot LSTM training history"""
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        
        # Loss
        axes[0].plot(history.history['loss'], label='Train Loss')
        axes[0].plot(history.history['val_loss'], label='Val Loss')
        axes[0].set_xlabel('Epoch')
        axes[0].set_ylabel('Loss (MSE)')
        axes[0].set_title('Model Loss')
        axes[0].legend()
        axes[0].grid(True)
        
        # MAE
        axes[1].plot(history.history['mae'], label='Train MAE')
        axes[1].plot(history.history['val_mae'], label='Val MAE')
        axes[1].set_xlabel('Epoch')
        axes[1].set_ylabel('MAE')
        axes[1].set_title('Model MAE')
        axes[1].legend()
        axes[1].grid(True)
        
        plt.tight_layout()
        plt.savefig('models/lstm_training_history.png', dpi=100)
        print("  Training history plot saved to models/lstm_training_history.png")
        plt.close()
    
    def evaluate_on_test(self, X_test, y_test):
        """Evaluate all models on test set"""
        print("\n" + "="*50)
        print("Evaluating on Test Set")
        print("="*50)
        
        # Random Forest
        if self.rf_model:
            rf_pred = self.rf_model.predict(X_test)
            rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))
            rf_mae = mean_absolute_error(y_test, rf_pred)
            rf_r2 = r2_score(y_test, rf_pred)
            
            self.metrics['random_forest']['test_rmse'] = float(rf_rmse)
            self.metrics['random_forest']['test_mae'] = float(rf_mae)
            self.metrics['random_forest']['test_r2'] = float(rf_r2)
            
            print(f"\nRandom Forest:")
            print(f"  RMSE: {rf_rmse:.4f}, MAE: {rf_mae:.4f}, R²: {rf_r2:.4f}")
        
        # Gradient Boosting
        if self.gb_model:
            gb_pred = self.gb_model.predict(X_test)
            gb_rmse = np.sqrt(mean_squared_error(y_test, gb_pred))
            gb_mae = mean_absolute_error(y_test, gb_pred)
            gb_r2 = r2_score(y_test, gb_pred)
            
            self.metrics['gradient_boosting']['test_rmse'] = float(gb_rmse)
            self.metrics['gradient_boosting']['test_mae'] = float(gb_mae)
            self.metrics['gradient_boosting']['test_r2'] = float(gb_r2)
            
            print(f"\nGradient Boosting:")
            print(f"  RMSE: {gb_rmse:.4f}, MAE: {gb_mae:.4f}, R²: {gb_r2:.4f}")
        
        # LSTM
        if self.lstm_model:
            X_test_np = X_test.values if hasattr(X_test, 'values') else X_test
            y_test_np = y_test.values if hasattr(y_test, 'values') else y_test
            
            X_test_seq, y_test_seq = self.prepare_lstm_data(X_test_np, y_test_np, 24)
            
            lstm_pred = self.lstm_model.predict(X_test_seq, verbose=0)
            lstm_rmse = np.sqrt(mean_squared_error(y_test_seq, lstm_pred))
            lstm_mae = mean_absolute_error(y_test_seq, lstm_pred)
            lstm_r2 = r2_score(y_test_seq, lstm_pred)
            
            self.metrics['lstm']['test_rmse'] = float(lstm_rmse)
            self.metrics['lstm']['test_mae'] = float(lstm_mae)
            self.metrics['lstm']['test_r2'] = float(lstm_r2)
            
            print(f"\nLSTM:")
            print(f"  RMSE: {lstm_rmse:.4f}, MAE: {lstm_mae:.4f}, R²: {lstm_r2:.4f}")
    
    def save_models(self):
        """Save trained models"""
        print("\n" + "="*50)
        print("Saving Models")
        print("="*50)
        
        if self.rf_model:
            joblib.dump(self.rf_model, 'models/random_forest_model.pkl')
            print("  ✓ Random Forest saved to models/random_forest_model.pkl")
        
        if self.gb_model:
            joblib.dump(self.gb_model, 'models/gradient_boosting_model.pkl')
            print("  ✓ Gradient Boosting saved to models/gradient_boosting_model.pkl")
        
        if self.lstm_model:
            self.lstm_model.save('models/lstm_model.h5')
            print("  ✓ LSTM saved to models/lstm_model.h5")
        
        # Save metrics
        with open('models/model_metrics.json', 'w') as f:
            json.dump(self.metrics, f, indent=2)
        print("  ✓ Metrics saved to models/model_metrics.json")


def main():
    """Main function untuk training"""
    trainer = AirQualityModelTrainer()
    
    print("="*50)
    print("Air Quality Prediction Model Training")
    print("="*50)
    
    # Load data
    print("\nLoading data...")
    X_train, X_val, X_test, y_train, y_val, y_test = trainer.load_data()
    
    print(f"Train set: {X_train.shape}")
    print(f"Validation set: {X_val.shape}")
    print(f"Test set: {X_test.shape}")
    
    # Train Random Forest
    trainer.train_random_forest(X_train, y_train, X_val, y_val)
    
    # Train Gradient Boosting
    trainer.train_gradient_boosting(X_train, y_train, X_val, y_val)
    
    # Train LSTM dengan parameter yang sudah dioptimalkan
    trainer.train_lstm(X_train, y_train, X_val, y_val, epochs=50, batch_size=64)
    
    # Evaluate on test set
    trainer.evaluate_on_test(X_test, y_test)
    
    # Save models
    trainer.save_models()
    
    print("\n" + "="*50)
    print("Training completed successfully!")
    print("="*50)


if __name__ == "__main__":
    main()
