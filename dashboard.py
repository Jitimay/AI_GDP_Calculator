import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import json

# Page config
st.set_page_config(
    page_title="AI-Powered Informal Sector GDP Calculator",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .alert-box {
        background-color: #ff6b6b;
        padding: 1rem;
        border-radius: 5px;
        color: white;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# API base URL
API_BASE = "http://localhost:5000"

def fetch_dashboard_data():
    """Fetch data from API"""
    try:
        response = requests.get(f"{API_BASE}/dashboard-data", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Connection Error: {str(e)}")
        return None

def create_gdp_gauge(value, title="National GDP Index"):
    """Create a gauge chart for GDP index"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title},
        delta = {'reference': 50},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 25], 'color': "lightgray"},
                {'range': [25, 50], 'color': "gray"},
                {'range': [50, 75], 'color': "lightgreen"},
                {'range': [75, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig.update_layout(height=300)
    return fig

def create_province_map(provincial_data):
    """Create a map visualization of provinces"""
    # Simplified coordinates for Burundi provinces
    coordinates = {
        'Bujumbura': [-3.3614, 29.3599],
        'Gitega': [-3.4271, 29.9246],
        'Ngozi': [-2.9077, 29.8307],
        'Kayanza': [-2.9222, 29.6292],
        'Bururi': [-3.9489, 29.6244],
        'Cibitoke': [-2.8833, 29.1333]
    }
    
    map_data = []
    for province, coords in coordinates.items():
        if province in provincial_data:
            gdp_value = provincial_data[province].get('ml_prediction', 
                       provincial_data[province]['composite_index'])
            map_data.append({
                'Province': province,
                'Latitude': coords[0],
                'Longitude': coords[1],
                'GDP_Index': gdp_value,
                'Size': gdp_value
            })
    
    df_map = pd.DataFrame(map_data)
    
    fig = px.scatter_mapbox(
        df_map,
        lat="Latitude",
        lon="Longitude",
        size="Size",
        color="GDP_Index",
        hover_name="Province",
        hover_data=["GDP_Index"],
        color_continuous_scale="Viridis",
        size_max=30,
        zoom=6,
        center={"lat": -3.3, "lon": 29.9}
    )
    
    fig.update_layout(
        mapbox_style="open-street-map",
        height=500,
        margin={"r":0,"t":0,"l":0,"b":0}
    )
    
    return fig

def create_time_series(historical_data):
    """Create time series chart"""
    fig = go.Figure()
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    for i, (province, data) in enumerate(historical_data.items()):
        if data:  # Check if data exists
            timestamps = [item['timestamp'] for item in data]
            values = [item['value'] for item in data]
            
            fig.add_trace(go.Scatter(
                x=timestamps,
                y=values,
                mode='lines+markers',
                name=province,
                line=dict(color=colors[i % len(colors)])
            ))
    
    fig.update_layout(
        title="GDP Index Trends (Last 24 Hours)",
        xaxis_title="Time",
        yaxis_title="GDP Index",
        height=400,
        showlegend=True
    )
    
    return fig

def main():
    # Header
    st.markdown('<div class="main-header">🌍 AI-Powered Informal Sector GDP Calculator</div>', 
                unsafe_allow_html=True)
    st.markdown('<div style="text-align: center; color: #666; margin-bottom: 2rem;">Real-time Economic Pulse of Burundi</div>', 
                unsafe_allow_html=True)
    
    # Auto-refresh
    if st.sidebar.button("🔄 Refresh Data"):
        st.rerun()
    
    # Auto-refresh every 30 seconds
    placeholder = st.empty()
    
    # Fetch data
    data = fetch_dashboard_data()
    
    if data and data.get('status') == 'success':
        current_data = data['current']
        historical_data = data.get('historical', {})
        alerts = data.get('alerts', [])
        
        # Main metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "National GDP Index",
                f"{current_data['national_index']:.1f}",
                delta=f"{current_data['national_index'] - 50:.1f}"
            )
        
        with col2:
            active_provinces = len([p for p, d in current_data['provincial_data'].items() 
                                 if d['composite_index'] > 60])
            st.metric("Active Provinces", active_provinces, delta=None)
        
        with col3:
            avg_activity = sum(d['composite_index'] for d in current_data['provincial_data'].values()) / len(current_data['provincial_data'])
            st.metric("Avg Activity", f"{avg_activity:.1f}", delta=None)
        
        with col4:
            st.metric("Alert Count", len(alerts), delta=None)
        
        # Alerts section
        if alerts:
            st.markdown("### 🚨 Active Alerts")
            for alert in alerts:
                st.markdown(f"""
                <div class="alert-box">
                    <strong>{alert['province']}</strong>: High activity detected 
                    (Index: {alert['index_value']:.1f})
                </div>
                """, unsafe_allow_html=True)
        
        # Main dashboard row
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # GDP Gauge
            st.markdown("### Economic Pulse")
            gauge_fig = create_gdp_gauge(current_data['national_index'])
            st.plotly_chart(gauge_fig, use_container_width=True)
            
            # Provincial rankings
            st.markdown("### Provincial Rankings")
            rankings = []
            for province, data in current_data['provincial_data'].items():
                rankings.append({
                    'Province': province,
                    'GDP Index': data.get('ml_prediction', data['composite_index'])
                })
            
            rankings_df = pd.DataFrame(rankings).sort_values('GDP Index', ascending=False)
            st.dataframe(rankings_df, use_container_width=True)
        
        with col2:
            # Map visualization
            st.markdown("### Geographic Distribution")
            map_fig = create_province_map(current_data['provincial_data'])
            st.plotly_chart(map_fig, use_container_width=True)
        
        # Time series
        if historical_data:
            st.markdown("### Trends Analysis")
            ts_fig = create_time_series(historical_data)
            st.plotly_chart(ts_fig, use_container_width=True)
        
        # Detailed indicators
        st.markdown("### Detailed Indicators")
        
        indicator_data = []
        for province, data in current_data['provincial_data'].items():
            indicators = data['indicators']
            indicator_data.append({
                'Province': province,
                'Mobile Money': indicators['mobile_money'],
                'Electricity': indicators['electricity'],
                'Internet': indicators['internet'],
                'Satellite': indicators['satellite'],
                'Social Media': indicators['social_media'],
                'GDP Index': data.get('ml_prediction', data['composite_index'])
            })
        
        indicators_df = pd.DataFrame(indicator_data)
        st.dataframe(indicators_df, use_container_width=True)
        
        # Footer
        st.markdown("---")
        st.markdown(f"Last updated: {data['timestamp']}")
        
    else:
        st.error("Unable to fetch data. Please ensure the API server is running on localhost:5000")
        st.info("Run: `python api.py` to start the backend server")

if __name__ == "__main__":
    main()
