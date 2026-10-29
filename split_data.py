"""
Script untuk split data menjadi train/val/test sets
"""
import pandas as pd
from sklearn.model_selection import train_test_split

print("="*60)
print("SPLITTING DATA INTO TRAIN/VAL/TEST SETS")
print("="*60)

# Load full dataset
print("\nLoading air_quality_data.csv...")
df = pd.read_csv('data/air_quality_data.csv')
print(f"✓ Loaded {len(df)} records from {df['city'].nunique()} cities")

# Create target column (pm2_5 is what we want to predict)
# We'll use pm2_5 as target and remove it from features
print("\n📊 Preparing features and target...")

# Drop non-feature columns
features_to_drop = ['city', 'timestamp', 'pm2_5']
target_col = 'pm2_5'

# Create a copy with target column
df_with_target = df.copy()
df_with_target['target'] = df_with_target[target_col]

# Drop columns we don't need for training
columns_to_keep = [col for col in df_with_target.columns if col not in ['city', 'timestamp', 'pm2_5']]
df_processed = df_with_target[columns_to_keep]

print(f"  Features: {', '.join([c for c in columns_to_keep if c != 'target'])}")
print(f"  Target: pm2_5 (renamed to 'target')")

# Sort by index (since we dropped timestamp)
df_processed = df_processed.reset_index(drop=True)

# Split: 70% train, 15% val, 15% test
# PENTING: shuffle=False untuk time series data agar urutan temporal terjaga
train_df, temp_df = train_test_split(df_processed, test_size=0.3, random_state=42, shuffle=False)
val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42, shuffle=False)

print(f"\n📊 Split Statistics:")
print(f"  Train: {len(train_df):,} records ({len(train_df)/len(df)*100:.1f}%)")
print(f"  Val:   {len(val_df):,} records ({len(val_df)/len(df)*100:.1f}%)")
print(f"  Test:  {len(test_df):,} records ({len(test_df)/len(df)*100:.1f}%)")

# Save splits
print("\n💾 Saving split datasets...")
train_df.to_csv('data/train_data.csv', index=False)
print(f"  ✓ Saved train_data.csv ({len(train_df.columns)} columns)")

val_df.to_csv('data/val_data.csv', index=False)
print(f"  ✓ Saved val_data.csv ({len(val_df.columns)} columns)")

test_df.to_csv('data/test_data.csv', index=False)
print(f"  ✓ Saved test_data.csv ({len(test_df.columns)} columns)")

# Show sample
print(f"\n📋 Sample data:")
print(train_df.head(2))

print("\n" + "="*60)
print("✅ DATA SPLIT COMPLETE!")
print("="*60)
print("Now you can run: python3 src/model_training.py")
