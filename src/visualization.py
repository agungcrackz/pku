"""
Module untuk visualisasi dan pemetaan kualitas udara
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import folium
from folium.plugins import HeatMap, MarkerCluster
import json


class AirQualityVisualizer:
    """Kelas untuk visualisasi data kualitas udara"""
    
    def __init__(self):
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
        
        self.aqi_colors = {
            'Good': '#00e400',
            'Moderate': '#ffff00',
            'Unhealthy for Sensitive Groups': '#ff7e00',
            'Unhealthy': '#ff0000',
            'Very Unhealthy': '#8f3f97',
            'Hazardous': '#7e0023'
        }
    
    def get_aqi_category(self, pm25):
        """Dapatkan kategori AQI dari nilai PM2.5"""
        if pm25 <= 15:
            return 'Good'
        elif pm25 <= 35:
            return 'Moderate'
        elif pm25 <= 55:
            return 'Unhealthy for Sensitive Groups'
        elif pm25 <= 150:
            return 'Unhealthy'
        elif pm25 <= 250:
            return 'Very Unhealthy'
        else:
            return 'Hazardous'
    
    def create_indonesia_map(self, city_data, output_file='map.html'):
        """
        Buat peta interaktif Indonesia dengan data kualitas udara
        city_data: dict dengan format {city_name: pm25_value}
        """
        # Center map pada Indonesia
        m = folium.Map(
            location=[-2.5, 118.0],
            zoom_start=5,
            tiles='OpenStreetMap'
        )
        
        # Add markers untuk setiap kota
        for city_name, pm25_value in city_data.items():
            if city_name in self.cities:
                coords = self.cities[city_name]
                category = self.get_aqi_category(pm25_value)
                color_map = {
                    'Good': 'green',
                    'Moderate': 'lightgreen',
                    'Unhealthy for Sensitive Groups': 'orange',
                    'Unhealthy': 'red',
                    'Very Unhealthy': 'darkred',
                    'Hazardous': 'black'
                }
                
                folium.CircleMarker(
                    location=[coords['lat'], coords['lon']],
                    radius=15,
                    popup=f"""
                        <b>{city_name}</b><br>
                        PM2.5: {pm25_value:.2f} μg/m³<br>
                        Status: {category}
                    """,
                    tooltip=f"{city_name}: {pm25_value:.1f} μg/m³",
                    color=color_map.get(category, 'gray'),
                    fill=True,
                    fillColor=color_map.get(category, 'gray'),
                    fillOpacity=0.7,
                    weight=2
                ).add_to(m)
                
                # Add label
                folium.Marker(
                    location=[coords['lat'], coords['lon']],
                    icon=folium.DivIcon(html=f"""
                        <div style="font-size: 10pt; color: black; font-weight: bold;">
                            {city_name}<br>{pm25_value:.1f}
                        </div>
                    """)
                ).add_to(m)
        
        # Add legend
        legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; right: 50px; width: 200px; height: 220px; 
                    background-color: white; z-index:9999; font-size:14px;
                    border:2px solid grey; border-radius: 5px; padding: 10px">
            <p style="margin: 0; font-weight: bold;">Kualitas Udara (PM2.5)</p>
            <p style="margin: 5px 0;"><span style="color: green;">●</span> Good (0-15)</p>
            <p style="margin: 5px 0;"><span style="color: lightgreen;">●</span> Moderate (15-35)</p>
            <p style="margin: 5px 0;"><span style="color: orange;">●</span> Unhealthy-Sensitive (35-55)</p>
            <p style="margin: 5px 0;"><span style="color: red;">●</span> Unhealthy (55-150)</p>
            <p style="margin: 5px 0;"><span style="color: darkred;">●</span> Very Unhealthy (150-250)</p>
            <p style="margin: 5px 0;"><span style="color: black;">●</span> Hazardous (250+)</p>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))
        
        # Save map
        m.save(output_file)
        print(f"Map saved to {output_file}")
        
        return m
    
    def plot_time_series(self, df, city='Jakarta', pollutant='pm2_5'):
        """Plot time series untuk satu kota"""
        city_data = df[df['city'] == city].copy()
        city_data = city_data.sort_values('timestamp')
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=city_data['timestamp'],
            y=city_data[pollutant],
            mode='lines',
            name=pollutant.upper(),
            line=dict(color='blue', width=2)
        ))
        
        # Add WHO standard line
        who_standards = {'pm2_5': 15, 'pm10': 45, 'no2': 25, 'so2': 40, 'o3': 100}
        if pollutant in who_standards:
            fig.add_hline(
                y=who_standards[pollutant],
                line_dash="dash",
                line_color="red",
                annotation_text=f"WHO Standard ({who_standards[pollutant]})"
            )
        
        fig.update_layout(
            title=f'{pollutant.upper()} Time Series - {city}',
            xaxis_title='Timestamp',
            yaxis_title=f'{pollutant.upper()} (μg/m³)',
            hovermode='x unified',
            height=500
        )
        
        return fig
    
    def plot_all_pollutants(self, df, city='Jakarta'):
        """Plot semua polutan untuk satu kota"""
        city_data = df[df['city'] == city].copy()
        city_data = city_data.sort_values('timestamp')
        
        pollutants = ['pm2_5', 'pm10', 'no2', 'so2', 'o3', 'co']
        
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=[p.upper() for p in pollutants]
        )
        
        positions = [(1,1), (1,2), (2,1), (2,2), (3,1), (3,2)]
        
        for pollutant, (row, col) in zip(pollutants, positions):
            if pollutant in city_data.columns:
                fig.add_trace(
                    go.Scatter(
                        x=city_data['timestamp'],
                        y=city_data[pollutant],
                        mode='lines',
                        name=pollutant.upper()
                    ),
                    row=row, col=col
                )
        
        fig.update_layout(
            title_text=f"All Pollutants - {city}",
            height=900,
            showlegend=False
        )
        
        return fig
    
    def plot_city_comparison(self, df, pollutant='pm2_5'):
        """Plot perbandingan antar kota"""
        # Calculate mean per city
        city_means = df.groupby('city')[pollutant].mean().sort_values(ascending=False)
        
        fig = go.Figure()
        
        colors = [self.aqi_colors.get(self.get_aqi_category(val), 'gray') 
                 for val in city_means.values]
        
        fig.add_trace(go.Bar(
            x=city_means.index,
            y=city_means.values,
            marker_color=colors,
            text=[f'{v:.1f}' for v in city_means.values],
            textposition='auto',
        ))
        
        # Add WHO standard line
        who_standards = {'pm2_5': 15, 'pm10': 45, 'no2': 25}
        if pollutant in who_standards:
            fig.add_hline(
                y=who_standards[pollutant],
                line_dash="dash",
                line_color="red",
                annotation_text=f"WHO Standard"
            )
        
        fig.update_layout(
            title=f'Average {pollutant.upper()} by City',
            xaxis_title='City',
            yaxis_title=f'{pollutant.upper()} (μg/m³)',
            height=500
        )
        
        return fig
    
    def plot_correlation_heatmap(self, df):
        """Plot correlation heatmap untuk polutan"""
        pollutants = ['pm2_5', 'pm10', 'no2', 'so2', 'o3', 'co']
        available_pollutants = [p for p in pollutants if p in df.columns]
        
        corr = df[available_pollutants].corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            colorscale='RdBu',
            zmid=0,
            text=corr.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 10},
            colorbar=dict(title="Correlation")
        ))
        
        fig.update_layout(
            title='Pollutant Correlation Matrix',
            height=600,
            width=700
        )
        
        return fig
    
    def plot_prediction_vs_actual(self, y_true, y_pred, title='Prediction vs Actual'):
        """Plot predicted vs actual values"""
        fig = go.Figure()
        
        # Scatter plot
        fig.add_trace(go.Scatter(
            x=y_true,
            y=y_pred,
            mode='markers',
            name='Predictions',
            marker=dict(size=5, opacity=0.6)
        ))
        
        # Perfect prediction line
        max_val = max(y_true.max(), y_pred.max())
        fig.add_trace(go.Scatter(
            x=[0, max_val],
            y=[0, max_val],
            mode='lines',
            name='Perfect Prediction',
            line=dict(color='red', dash='dash')
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title='Actual PM2.5 (μg/m³)',
            yaxis_title='Predicted PM2.5 (μg/m³)',
            height=500,
            width=600
        )
        
        return fig
    
    def create_dashboard_data(self, df):
        """Prepare data untuk dashboard"""
        # Overall statistics
        stats = {
            'total_records': len(df),
            'cities': df['city'].nunique(),
            'avg_pm25': float(df['pm2_5'].mean()),
            'max_pm25': float(df['pm2_5'].max()),
            'min_pm25': float(df['pm2_5'].min()),
            'who_compliant_pct': float((df['pm2_5'] <= 15).mean() * 100)
        }
        
        # City statistics
        city_stats = df.groupby('city').agg({
            'pm2_5': ['mean', 'max', 'min'],
            'timestamp': 'count'
        }).round(2).to_dict()
        
        # Recent data (last 24 hours)
        recent_data = df.nlargest(24, 'timestamp')[['city', 'timestamp', 'pm2_5', 'aqi']].to_dict('records')
        
        return {
            'overall_stats': stats,
            'city_stats': city_stats,
            'recent_data': recent_data
        }


def main():
    """Main function untuk testing visualization"""
    visualizer = AirQualityVisualizer()
    
    # Load data
    print("Loading data...")
    df = pd.read_csv('data/air_quality_data.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    print(f"Loaded {len(df)} records")
    
    # Create map
    print("\nCreating Indonesia map...")
    city_pm25 = df.groupby('city')['pm2_5'].mean().to_dict()
    visualizer.create_indonesia_map(city_pm25, 'static/indonesia_air_quality_map.html')
    
    # Create plots
    print("\nCreating visualizations...")
    
    # Time series
    fig1 = visualizer.plot_time_series(df, 'Jakarta', 'pm2_5')
    fig1.write_html('static/time_series.html')
    print("  ✓ Time series plot saved")
    
    # City comparison
    fig2 = visualizer.plot_city_comparison(df, 'pm2_5')
    fig2.write_html('static/city_comparison.html')
    print("  ✓ City comparison plot saved")
    
    # Correlation heatmap
    fig3 = visualizer.plot_correlation_heatmap(df)
    fig3.write_html('static/correlation_heatmap.html')
    print("  ✓ Correlation heatmap saved")
    
    # Dashboard data
    print("\nPreparing dashboard data...")
    dashboard_data = visualizer.create_dashboard_data(df)
    with open('static/dashboard_data.json', 'w') as f:
        json.dump(dashboard_data, f, indent=2)
    print("  ✓ Dashboard data saved")
    
    print("\n" + "="*50)
    print("Visualization completed!")
    print("="*50)


if __name__ == "__main__":
    main()
