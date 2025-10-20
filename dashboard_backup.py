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

# Custom CSS - Modern Dark Theme
st.markdown("""
<style>
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
        min-height: 100vh;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    /* Metric cards */
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .stMetric label {
        color: rgba(255,255,255,0.8) !important;
        font-weight: 600;
    }
    
    .stMetric div[data-testid="metric-container"] > div {
        color: white !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Charts background */
    .js-plotly-plot {
        background: rgba(255,255,255,0.05) !important;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    
    /* Alert styling */
    .alert-success {
        background: linear-gradient(90deg, #56ab2f 0%, #a8e6cf 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(86, 171, 47, 0.3);
    }
    
    .alert-warning {
        background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);
    }
    
    /* Data tables */
    .stDataFrame {
        background: rgba(255,255,255,0.05);
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
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
    """Create a modern gauge chart for GDP index"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title, 'font': {'size': 24, 'color': 'white'}},
        delta = {'reference': 50, 'increasing': {'color': "#00ff88"}, 'decreasing': {'color': "#ff4444"}},
        gauge = {
            'axis': {'range': [None, 100], 'tickcolor': "white", 'tickfont': {'color': 'white'}},
            'bar': {'color': "#667eea", 'thickness': 0.8},
            'bgcolor': "rgba(255,255,255,0.1)",
            'borderwidth': 2,
            'bordercolor': "rgba(255,255,255,0.3)",
            'steps': [
                {'range': [0, 25], 'color': "rgba(255,68,68,0.3)"},
                {'range': [25, 50], 'color': "rgba(255,193,7,0.3)"},
                {'range': [50, 75], 'color': "rgba(0,255,136,0.3)"},
                {'range': [75, 100], 'color': "rgba(0,255,136,0.5)"}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white", 'family': "Arial"},
        height=300,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    return fig

def enhance_chart_styling(fig):
    """Apply modern dark theme styling to charts"""
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white", 'family': "Arial"},
        title_font_color="white",
        title_font_size=18,
        margin=dict(l=20, r=20, t=60, b=20),
        showlegend=True,
        legend=dict(
            bgcolor="rgba(255,255,255,0.1)",
            bordercolor="rgba(255,255,255,0.2)",
            borderwidth=1,
            font=dict(color="white")
        )
    )
    
    # Update axes
    fig.update_xaxes(
        gridcolor="rgba(255,255,255,0.1)",
        tickfont=dict(color="white"),
        titlefont=dict(color="white")
    )
    fig.update_yaxes(
        gridcolor="rgba(255,255,255,0.1)",
        tickfont=dict(color="white"),
        titlefont=dict(color="white")
    )
    
    return fig
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
        mapbox_style="carto-darkmatter",
        height=500,
        margin={"r":0,"t":0,"l":0,"b":0},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "white"}
    )
    
    return enhance_chart_styling(fig)

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
    
    return enhance_chart_styling(fig)

def main():
    # Modern Header with animations
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 3rem; font-weight: 700;">
            🌍 AI-Powered GDP Calculator
        </h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            Real-time estimation of Burundi's $2.3B informal economy using AI & multi-source data fusion
        </p>
        <div style="margin-top: 1rem;">
            <span style="background: rgba(255,255,255,0.2); padding: 0.3rem 1rem; border-radius: 20px; margin: 0 0.5rem;">
                🤖 Machine Learning
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.3rem 1rem; border-radius: 20px; margin: 0 0.5rem;">
                📊 Real-time Data
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 0.3rem 1rem; border-radius: 20px; margin: 0 0.5rem;">
                🌍 5 Data Sources
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Real-time auto-refresh controls
    auto_refresh = st.sidebar.checkbox("🔄 Real-time refresh", value=True)
    refresh_interval = st.sidebar.selectbox("Refresh interval", [2, 3, 5, 10], index=0)
    
    if st.sidebar.button("🔄 Refresh Now"):
        st.rerun()
    
    # Fetch data first
    data = fetch_dashboard_data()
    
    if data and data.get('status') == 'success':
        # Handle different response formats
        if 'current' in data:
            current_data = data['current']
        else:
            # Fallback format
            current_data = {
                'national_index': data.get('national_index', 0),
                'provincial_data': data.get('provincial_data', {})
            }
        
        historical_data = data.get('historical', data.get('historical_data', {}))
        alerts = data.get('alerts', [])
        
def show_loading_animation():
    """Show modern loading animation"""
    loading_html = """
    <div style="display: flex; justify-content: center; align-items: center; height: 200px;">
        <div style="text-align: center;">
            <div style="border: 4px solid rgba(102, 126, 234, 0.3); border-top: 4px solid #667eea; 
                        border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite; margin: 0 auto;"></div>
            <p style="color: white; margin-top: 1rem; font-size: 1.1rem;">🤖 AI Processing Economic Data...</p>
        </div>
    </div>
    <style>
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
    """
    return st.markdown(loading_html, unsafe_allow_html=True)

def create_enhanced_metric(title, value, delta=None, icon="📊"):
    """Create enhanced metric card with modern styling"""
    delta_html = ""
    if delta is not None:
        color = "#00ff88" if delta >= 0 else "#ff4444"
        arrow = "↗️" if delta >= 0 else "↘️"
        delta_html = f'<div style="color: {color}; font-size: 0.9rem; margin-top: 0.5rem;">{arrow} {delta}</div>'
    
    metric_html = f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 1.5rem; border-radius: 12px; color: white; 
                box-shadow: 0 4px 20px rgba(0,0,0,0.3); 
                border: 1px solid rgba(255,255,255,0.1); margin: 0.5rem 0;">
        <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
            <span style="font-size: 1.5rem; margin-right: 0.5rem;">{icon}</span>
            <span style="color: rgba(255,255,255,0.8); font-weight: 600;">{title}</span>
        </div>
        <div style="font-size: 2rem; font-weight: 700; margin: 0.5rem 0;">{value}</div>
        {delta_html}
    </div>
    """
    return st.markdown(metric_html, unsafe_allow_html=True)
        
        with col2:
            active_provinces = len([p for p, d in current_data['provincial_data'].items() 
                                 if d['composite_index'] > 60])
            create_enhanced_metric("Active Provinces", str(active_provinces), None, "🏛️")
        
        with col3:
            avg_activity = sum(d['composite_index'] for d in current_data['provincial_data'].values()) / len(current_data['provincial_data'])
            create_enhanced_metric("Avg Activity", f"{avg_activity:.1f}", None, "📈")
        
        with col4:
            create_enhanced_metric("Alert Count", str(len(alerts)), None, "🚨")
        
        # Alerts section
        if alerts:
            st.markdown("### 🚨 Active Alerts")
            for alert in alerts:
                index_val = alert.get('gdp_index', alert.get('index_value', 0))
                st.markdown(f"""
                <div class="alert-box">
                    <strong>{alert['province']}</strong>: High activity detected 
                    (Index: {index_val:.1f})
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
        
        # Auto-refresh only after successful data display
        if auto_refresh:
            time.sleep(refresh_interval)
            st.rerun()
            
    else:
        st.error("Unable to fetch data. Please ensure the API server is running on localhost:5000")
        st.info("Run: `python api.py` to start the backend server")

if __name__ == "__main__":
    main()
