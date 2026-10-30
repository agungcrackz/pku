# 🤖 Ensemble Method Implementation

## Overview

Sistem Air Quality Prediction Indonesia menggunakan **metode Ensemble** untuk prediksi PM2.5 yang lebih akurat dan stabil.

## What is Ensemble?

Ensemble adalah teknik Machine Learning yang menggabungkan prediksi dari beberapa model untuk menghasilkan prediksi final yang lebih baik daripada model individual.

**Formula:**
```
Ensemble Prediction = (RF_prediction + GB_prediction + LSTM_prediction) / 3
```

## Models Used

### 1. Random Forest (RF)
- **Type**: Tree-based ensemble
- **Performance**: R² = 0.886, MAE = 0.78
- **Strengths**: Robust, handles non-linear relationships well
- **Weaknesses**: Can overfit on noisy data

### 2. Gradient Boosting (GB)
- **Type**: Sequential ensemble
- **Performance**: R² = 0.892, MAE = 0.77
- **Strengths**: High accuracy, learns from previous errors
- **Weaknesses**: Slower training, sensitive to hyperparameters

### 3. LSTM Neural Network
- **Type**: Deep learning (RNN variant)
- **Performance**: R² = 0.899, MAE = 0.76
- **Strengths**: Best for time-series, captures temporal patterns
- **Weaknesses**: Requires more data and training time

## Ensemble Performance

| Metric | Random Forest | Gradient Boosting | LSTM | **Ensemble** |
|--------|---------------|-------------------|------|--------------|
| R² Score | 0.886 | 0.892 | 0.899 | **~0.892** |
| MAE (μg/m³) | 0.78 | 0.77 | 0.76 | **~0.77** |
| RMSE (μg/m³) | 1.15 | 1.12 | 1.09 | **~1.12** |
| Stability | Medium | High | Medium | **Very High** |

## Why Ensemble?

### ✅ Advantages

1. **Reduced Variance**: Averaging reduces individual model errors
2. **Better Generalization**: Less prone to overfitting
3. **Stable Predictions**: Smooths out extreme predictions
4. **Production-Ready**: Industry standard for critical applications
5. **Proven Track Record**: Used in winning Kaggle competitions

### ⚠️ Trade-offs

1. **Inference Time**: 3x slower (need to run 3 models)
2. **Model Size**: 3x larger (need to store 3 models)
3. **Complexity**: More complex deployment and monitoring

## Implementation

### Code Structure

**File: `src/prediction.py`**

```python
def predict_ensemble(self, features):
    """Prediksi menggunakan ensemble (average dari semua model)"""
    predictions = []
    
    if self.rf_model:
        rf_pred = self.rf_model.predict(features)[0]
        predictions.append(rf_pred)
    
    if self.gb_model:
        gb_pred = self.gb_model.predict(features)[0]
        predictions.append(gb_pred)
    
    if self.lstm_model:
        lstm_features = np.array(features).reshape((1, 1, features.shape[1]))
        lstm_pred = self.lstm_model.predict(lstm_features, verbose=0)[0][0]
        predictions.append(lstm_pred)
    
    return np.mean(predictions)  # Simple average
```

### API Integration

**Endpoint: `/predict` (POST)**

```python
@app.route('/predict', methods=['POST'])
def predict():
    city = request.form.get('city')
    X_sample = load_features_for_city(city)
    
    # Use Ensemble method
    result = predictor.predict_ensemble_and_classify(X_sample)
    
    return render_template('predict_result.html', result=result)
```

## Testing

### Unit Test

```bash
# Test individual models
python -m pytest tests/test_models.py

# Test ensemble
python -m pytest tests/test_ensemble.py
```

### Validation

```python
from src.prediction import AirQualityPredictor

predictor = AirQualityPredictor()
predictor.load_models()

# Load test data
test_df = pd.read_csv('data/test_data.csv')
X_test = test_df.drop('target', axis=1)

# Run ensemble prediction
result = predictor.predict_ensemble_and_classify(X_test.iloc[0:1])

print(f"Ensemble Prediction: {result['pm25_predicted']:.2f} μg/m³")
print(f"Status: {result['air_quality']['status']}")
```

## Monitoring

### Key Metrics to Track

1. **Prediction Distribution**: Monitor for drift
2. **Model Agreement**: Track when models disagree significantly
3. **Inference Time**: Ensure < 500ms for good UX
4. **Error Rate**: Compare ensemble vs individual models

### Alert Conditions

- ⚠️ Model predictions differ by > 20%
- ⚠️ Inference time > 1 second
- ⚠️ Any model fails to load
- ⚠️ Prediction outside reasonable range (0-500 μg/m³)

## Future Improvements

### Short-term (1-3 months)
- [ ] **Weighted Ensemble**: Use R² scores as weights instead of simple average
- [ ] **Model Confidence**: Add confidence intervals
- [ ] **A/B Testing**: Compare ensemble vs best single model

### Medium-term (3-6 months)
- [ ] **Stacking**: Train meta-model on top of base models
- [ ] **Dynamic Weighting**: Adjust weights based on recent performance
- [ ] **Model Versioning**: Support multiple ensemble versions

### Long-term (6-12 months)
- [ ] **AutoML**: Automated model selection and hyperparameter tuning
- [ ] **Online Learning**: Update models incrementally with new data
- [ ] **Explainable AI**: Add SHAP/LIME for prediction explanations

## References

- [Kaggle Ensemble Guide](https://www.kaggle.com/code/arthurtok/introduction-to-ensembling-stacking-in-python)
- [Scikit-learn Ensemble Methods](https://scikit-learn.org/stable/modules/ensemble.html)
- [Netflix: How We Use Ensemble Models](https://netflixtechblog.com/)

## Changelog

### Version 1.1.0 (2026-10-30)
- ✅ Implemented Ensemble method (RF + GB + LSTM)
- ✅ Updated `/predict` route to use ensemble
- ✅ Added ensemble info badges in UI
- ✅ Updated README with ensemble explanation
- ✅ Created this documentation

### Version 1.0.0 (2026-10)
- Initial release with individual models only

---

**Last Updated**: October 30, 2026  
**Maintained by**: Nexora Team - STMIK Kaputama
