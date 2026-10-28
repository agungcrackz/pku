"""
Module untuk mengumpulkan data kualitas udara dari berbagai sumber
"""
import pandas as pd
import requests
import json
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class AirQualityDataCollector:
    """Kelas untuk mengumpulkan data kualitas udara"""
    
    def __init__(self):
        self.openweather_api_key = os.getenv('OPENWEATHER_API_KEY', '')
        self.iqair_api_key = os.getenv('IQAIR_API_KEY', '')
        
        # Koordinat kota-kota per provinsi (38 provinsi, max 10 kota untuk provinsi besar)
        # Total: 88 kota untuk coverage optimal nasional 100%
        self.cities = {
            # ============ SUMATERA (10 provinsi) ============
            # 1. ACEH
            'Banda Aceh': {'lat': 5.5483, 'lon': 95.3238},
            'Lhokseumawe': {'lat': 5.1801, 'lon': 97.1507},
            'Sabang': {'lat': 5.8933, 'lon': 95.3214},
            
            # 2. SUMATERA UTARA
            'Medan': {'lat': 3.5952, 'lon': 98.6722},
            'Binjai': {'lat': 3.6001, 'lon': 98.4854},
            'Pematangsiantar': {'lat': 2.9596, 'lon': 99.0687},
            'Tebing Tinggi': {'lat': 3.3273, 'lon': 99.1625},
            
            # 3. SUMATERA BARAT
            'Padang': {'lat': -0.9471, 'lon': 100.4172},
            'Bukittinggi': {'lat': -0.3055, 'lon': 100.3693},
            'Payakumbuh': {'lat': -0.2291, 'lon': 100.6333},
            
            # 4. RIAU
            'Pekanbaru': {'lat': 0.5071, 'lon': 101.4478},
            'Dumai': {'lat': 1.6812, 'lon': 101.4478},
            
            # 5. KEPULAUAN RIAU
            'Tanjung Pinang': {'lat': 0.9183, 'lon': 104.4588},
            'Batam': {'lat': 1.0456, 'lon': 104.0305},
            
            # 6. JAMBI
            'Jambi': {'lat': -1.6101, 'lon': 103.6131},
            
            # 7. SUMATERA SELATAN
            'Palembang': {'lat': -2.9761, 'lon': 104.7754},
            'Lubuklinggau': {'lat': -3.2947, 'lon': 102.8597},
            
            # 8. BENGKULU
            'Bengkulu': {'lat': -3.8008, 'lon': 102.2655},
            
            # 9. LAMPUNG
            'Bandar Lampung': {'lat': -5.4500, 'lon': 105.2667},
            'Metro': {'lat': -5.1130, 'lon': 105.3067},
            
            # 10. BANGKA BELITUNG
            'Pangkal Pinang': {'lat': -2.1316, 'lon': 106.1139},
            
            # ============ JAWA (6 provinsi) ============
            # 11. DKI JAKARTA
            'Jakarta Pusat': {'lat': -6.1862, 'lon': 106.8341},
            'Jakarta Utara': {'lat': -6.1382, 'lon': 106.8826},
            'Jakarta Selatan': {'lat': -6.2615, 'lon': 106.8106},
            'Jakarta Timur': {'lat': -6.2250, 'lon': 106.9004},
            'Jakarta Barat': {'lat': -6.1668, 'lon': 106.7594},
            
            # 12. JAWA BARAT
            'Bandung': {'lat': -6.9175, 'lon': 107.6191},
            'Bekasi': {'lat': -6.2383, 'lon': 106.9756},
            'Depok': {'lat': -6.4025, 'lon': 106.7942},
            'Bogor': {'lat': -6.5971, 'lon': 106.8060},
            'Cimahi': {'lat': -6.8723, 'lon': 107.5425},
            'Tasikmalaya': {'lat': -7.3274, 'lon': 108.2207},
            'Cirebon': {'lat': -6.7063, 'lon': 108.5571},
            'Sukabumi': {'lat': -6.9278, 'lon': 106.9271},
            
            # 13. JAWA TENGAH
            'Semarang': {'lat': -6.9667, 'lon': 110.4167},
            'Surakarta': {'lat': -7.5755, 'lon': 110.8243},
            'Salatiga': {'lat': -7.3317, 'lon': 110.4920},
            'Tegal': {'lat': -6.8694, 'lon': 109.1402},
            'Pekalongan': {'lat': -6.8886, 'lon': 109.6753},
            'Magelang': {'lat': -7.4797, 'lon': 110.2172},
            
            # 14. DI YOGYAKARTA
            'Yogyakarta': {'lat': -7.7956, 'lon': 110.3695},
            
            # 15. JAWA TIMUR
            'Surabaya': {'lat': -7.2575, 'lon': 112.7521},
            'Malang': {'lat': -7.9797, 'lon': 112.6304},
            'Kediri': {'lat': -7.8167, 'lon': 112.0167},
            'Blitar': {'lat': -8.0983, 'lon': 112.1681},
            'Mojokerto': {'lat': -7.4664, 'lon': 112.4338},
            'Madiun': {'lat': -7.6298, 'lon': 111.5239},
            'Pasuruan': {'lat': -7.6453, 'lon': 112.9075},
            'Probolinggo': {'lat': -7.7543, 'lon': 113.2159},
            
            # 16. BANTEN
            'Serang': {'lat': -6.1204, 'lon': 106.1503},
            'Tangerang': {'lat': -6.1783, 'lon': 106.6319},
            'Tangerang Selatan': {'lat': -6.2886, 'lon': 106.7188},
            'Cilegon': {'lat': -6.0024, 'lon': 106.0191},
            
            # ============ KALIMANTAN (5 provinsi) ============
            # 17. KALIMANTAN BARAT
            'Pontianak': {'lat': -0.0263, 'lon': 109.3425},
            'Singkawang': {'lat': 0.9063, 'lon': 108.9896},
            
            # 18. KALIMANTAN TENGAH
            'Palangkaraya': {'lat': -2.2089, 'lon': 113.9168},
            
            # 19. KALIMANTAN SELATAN
            'Banjarmasin': {'lat': -3.3194, 'lon': 114.5906},
            'Banjarbaru': {'lat': -3.4542, 'lon': 114.8383},
            
            # 20. KALIMANTAN TIMUR
            'Samarinda': {'lat': -0.5022, 'lon': 117.1536},
            'Balikpapan': {'lat': -1.2379, 'lon': 116.8529},
            'Bontang': {'lat': 0.1332, 'lon': 117.5000},
            
            # 21. KALIMANTAN UTARA
            'Tanjung Selor': {'lat': 2.8350, 'lon': 117.3625},
            'Tarakan': {'lat': 3.3000, 'lon': 117.6333},
            
            # ============ SULAWESI (6 provinsi) ============
            # 22. SULAWESI UTARA
            'Manado': {'lat': 1.4748, 'lon': 124.8421},
            'Bitung': {'lat': 1.4404, 'lon': 125.1828},
            'Tomohon': {'lat': 1.3250, 'lon': 124.8378},
            
            # 23. SULAWESI TENGAH
            'Palu': {'lat': -0.8999, 'lon': 119.8707},
            
            # 24. SULAWESI SELATAN
            'Makassar': {'lat': -5.1477, 'lon': 119.4327},
            'Parepare': {'lat': -4.0167, 'lon': 119.6333},
            'Palopo': {'lat': -2.9925, 'lon': 120.1989},
            
            # 25. SULAWESI TENGGARA
            'Kendari': {'lat': -3.9778, 'lon': 122.5150},
            'Baubau': {'lat': -5.4669, 'lon': 122.6333},
            
            # 26. GORONTALO
            'Gorontalo': {'lat': 0.5435, 'lon': 123.0567},
            
            # 27. SULAWESI BARAT
            'Mamuju': {'lat': -2.6739, 'lon': 118.8896},
            
            # ============ BALI & NUSA TENGGARA (3 provinsi) ============
            # 28. BALI
            'Denpasar': {'lat': -8.6705, 'lon': 115.2126},
            
            # 29. NUSA TENGGARA BARAT
            'Mataram': {'lat': -8.5833, 'lon': 116.1167},
            'Bima': {'lat': -8.4600, 'lon': 118.7267},
            
            # 30. NUSA TENGGARA TIMUR
            'Kupang': {'lat': -10.1772, 'lon': 123.6070},
            
            # ============ MALUKU (2 provinsi) ============
            # 31. MALUKU
            'Ambon': {'lat': -3.6954, 'lon': 128.1814},
            'Tual': {'lat': -5.6288, 'lon': 132.7522},
            
            # 32. MALUKU UTARA
            'Ternate': {'lat': 0.7893, 'lon': 127.3614},
            'Tidore': {'lat': 0.6833, 'lon': 127.5000},
            
            # ============ PAPUA (6 provinsi) ============
            # 33. PAPUA
            'Jayapura': {'lat': -2.5916, 'lon': 140.6692},
            
            # 34. PAPUA BARAT
            'Manokwari': {'lat': -0.8618, 'lon': 134.0640},
            
            # 35. PAPUA TENGAH
            'Nabire': {'lat': -3.3596, 'lon': 135.4960},
            
            # 36. PAPUA PEGUNUNGAN
            'Wamena': {'lat': -4.0951, 'lon': 138.9496},
            
            # 37. PAPUA SELATAN
            'Merauke': {'lat': -8.4667, 'lon': 140.4000},
            
            # 38. PAPUA BARAT DAYA
            'Sorong': {'lat': -0.8790, 'lon': 131.2526},
        }
    
    def get_openweather_data(self, lat, lon):
        """
        Mengambil data dari OpenWeatherMap Air Pollution API
        """
        if not self.openweather_api_key:
            print("Warning: OpenWeatherMap API key not found")
            return None
            
        url = f"http://api.openweathermap.org/data/2.5/air_pollution"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.openweather_api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
    
    def get_historical_data(self, lat, lon, start_date, end_date):
        """
        Mengambil data historis kualitas udara
        """
        if not self.openweather_api_key:
            print("Warning: OpenWeatherMap API key not found")
            return None
            
        start_timestamp = int(start_date.timestamp())
        end_timestamp = int(end_date.timestamp())
        
        url = f"http://api.openweathermap.org/data/2.5/air_pollution/history"
        params = {
            'lat': lat,
            'lon': lon,
            'start': start_timestamp,
            'end': end_timestamp,
            'appid': self.openweather_api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching historical data: {e}")
            return None
    
    def parse_air_quality_data(self, data, city_name):
        """
        Parse data dari API ke format DataFrame
        """
        if not data or 'list' not in data:
            return pd.DataFrame()
        
        records = []
        for item in data['list']:
            record = {
                'city': city_name,
                'timestamp': datetime.fromtimestamp(item['dt']),
                'aqi': item['main']['aqi'],
                'co': item['components'].get('co', None),
                'no': item['components'].get('no', None),
                'no2': item['components'].get('no2', None),
                'o3': item['components'].get('o3', None),
                'so2': item['components'].get('so2', None),
                'pm2_5': item['components'].get('pm2_5', None),
                'pm10': item['components'].get('pm10', None),
                'nh3': item['components'].get('nh3', None),
            }
            records.append(record)
        
        return pd.DataFrame(records)
    
    def collect_all_cities_data(self, days_back=30):
        """
        Mengumpulkan data untuk semua kota
        """
        all_data = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        print(f"Collecting data from {start_date.date()} to {end_date.date()}")
        
        for city_name, coords in self.cities.items():
            print(f"Fetching data for {city_name}...")
            
            # Get historical data
            data = self.get_historical_data(
                coords['lat'], 
                coords['lon'], 
                start_date, 
                end_date
            )
            
            if data:
                df = self.parse_air_quality_data(data, city_name)
                all_data.append(df)
                print(f"  ✓ Collected {len(df)} records for {city_name}")
            else:
                print(f"  ✗ Failed to collect data for {city_name}")
        
        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
            return combined_df
        else:
            return pd.DataFrame()
    
    def generate_sample_data(self, num_days=90):
        """
        Generate data sampel untuk testing (jika API key tidak tersedia)
        Dengan variasi PM2.5 yang realistis per kota
        """
        import numpy as np
        
        print("Generating sample data with realistic city variations...")
        
        # Karakteristik PM2.5 per kota (mean, std_dev)
        # Berdasarkan data REAL 2024 dari IQAir & CREA Indonesia
        city_pm25_profiles = {
            'Jakarta': (40, 12),      # Annual avg ~39-40 (CREA 2024)
            'Tangerang': (42, 13),    # Jabodetabek area, sedikit lebih tinggi
            'Depok': (38, 12),        # Jabodetabek suburban
            'Bekasi': (45, 13),       # Industrial area di Jabodetabek
            'Surabaya': (46, 14),     # 2nd largest city (IQAir 2024)
            'Bandung': (35, 11),      # Mountain city, cooler, lebih bersih
            'Medan': (32, 10),        # Sumatera, moderate
            'Semarang': (30, 10),     # Coastal, moderate industry
            'Palembang': (28, 10),    # Sumatera, forest fires season vary
            'Makassar': (22, 8),      # Sulawesi, coastal, sea breeze (< WHO IT3)
        }
        
        records = []
        end_date = datetime.now()
        
        for city_name, coords in self.cities.items():
            # Get city-specific PM2.5 profile
            mean_pm25, std_pm25 = city_pm25_profiles.get(city_name, (50, 15))
            
            for day in range(num_days):
                for hour in range(0, 24, 3):  # Data setiap 3 jam
                    timestamp = end_date - timedelta(days=day, hours=hour)
                    
                    # Generate PM2.5 dengan normal distribution per kota
                    base_pm25 = np.clip(
                        np.random.normal(mean_pm25, std_pm25),
                        10,  # minimum
                        150  # maximum
                    )
                    
                    # Tambah variasi diurnal (siang vs malam)
                    hour_of_day = timestamp.hour
                    if 6 <= hour_of_day <= 9 or 17 <= hour_of_day <= 20:
                        # Rush hour - PM2.5 lebih tinggi
                        base_pm25 *= np.random.uniform(1.1, 1.3)
                    elif 2 <= hour_of_day <= 5:
                        # Dini hari - PM2.5 lebih rendah
                        base_pm25 *= np.random.uniform(0.7, 0.9)
                    
                    # PM10 biasanya 1.5-2.5x dari PM2.5
                    base_pm10 = base_pm25 * np.random.uniform(1.5, 2.5)
                    
                    record = {
                        'city': city_name,
                        'timestamp': timestamp,
                        'aqi': int(np.clip(base_pm25 / 12.5, 1, 5)),
                        'co': np.random.uniform(200, 2000),
                        'no': np.random.uniform(0, 50),
                        'no2': np.random.uniform(10, 80),
                        'o3': np.random.uniform(40, 150),
                        'so2': np.random.uniform(5, 60),
                        'pm2_5': base_pm25,
                        'pm10': base_pm10,
                        'nh3': np.random.uniform(1, 30),
                    }
                    records.append(record)
        
        df = pd.DataFrame(records)
        print(f"Generated {len(df)} sample records with city-specific variations")
        
        # Print summary per city
        print("\nPM2.5 Average per City:")
        city_avg = df.groupby('city')['pm2_5'].mean().sort_values(ascending=False)
        for city, avg_pm25 in city_avg.items():
            print(f"  {city}: {avg_pm25:.2f} μg/m³")
        
        return df
    
    def save_data(self, df, filename='air_quality_data.csv'):
        """
        Simpan data ke CSV
        """
        filepath = os.path.join('data', filename)
        df.to_csv(filepath, index=False)
        print(f"Data saved to {filepath}")
        return filepath


def main():
    """Main function untuk mengumpulkan data"""
    collector = AirQualityDataCollector()
    
    print("="*60)
    print("AIR QUALITY DATA COLLECTION")
    print("="*60)
    
    # Check if API key is available
    if collector.openweather_api_key:
        print("\n✓ OpenWeatherMap API key found!")
        print("Collecting REAL-TIME data from API...")
        print("-"*60)
        
        # Collect real data
        df = collector.collect_all_cities_data(days_back=90)
        
        if not df.empty:
            print("\n✓ Real-time data collection successful!")
        else:
            print("\n✗ API data collection failed. Generating sample data...")
            df = collector.generate_sample_data(num_days=90)
    else:
        print("\n⚠ OpenWeatherMap API key not found!")
        print("To get REAL-TIME data:")
        print("  1. Sign up at: https://openweathermap.org/api")
        print("  2. Get FREE API key (Air Pollution API)")
        print("  3. Add to .env file: OPENWEATHER_API_KEY=your_key_here")
        print("\nFor now, generating realistic sample data based on 2024 averages...")
        print("-"*60)
        df = collector.generate_sample_data(num_days=90)
    
    # Save data
    if not df.empty:
        collector.save_data(df)
        print("\n" + "="*60)
        print("DATA COLLECTION SUMMARY")
        print("="*60)
        print(f"Total records: {len(df)}")
        print(f"Cities: {df['city'].nunique()}")
        print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
        print("\nPM2.5 Statistics per City:")
        print("-"*60)
        city_stats = df.groupby('city')['pm2_5'].agg(['mean', 'min', 'max']).round(2)
        city_stats = city_stats.sort_values('mean', ascending=False)
        for city, row in city_stats.iterrows():
            status = "🔴" if row['mean'] > 55 else "🟠" if row['mean'] > 35 else "🟡" if row['mean'] > 15 else "🟢"
            print(f"{status} {city:12s} Avg: {row['mean']:5.1f} | Min: {row['min']:5.1f} | Max: {row['max']:5.1f} μg/m³")
        
        print("\n" + "="*60)
        print("✓ Data saved to data/air_quality_data.csv")
        print("="*60)
        
        if not collector.openweather_api_key:
            print("\n💡 TIP: For REAL-TIME data, add OpenWeatherMap API key to .env")
    else:
        print("\n✗ No data collected!")


if __name__ == "__main__":
    main()
