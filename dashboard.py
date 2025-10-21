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

# Custom CSS - Modern Theme
st.markdown("""
<style>
    .main .block-container {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
        min-height: 100vh;
    }
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .js-plotly-plot {
        background: rgba(255,255,255,0.05) !important;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# API base URL
API_BASE = "http://localhost:5000"

def fetch_dashboard_data():
    """Fetch dashboard data from API"""
    try:
        response = requests.get(f"{API_BASE}/dashboard-data", timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Connection error: {e}")
        return None

def get_forecast_data(province, months):
    """Get 12-month forecast data from API"""
    try:
        response = requests.get(f"{API_BASE}/forecast",
                              params={'province': province, 'months': months}, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Forecast failed: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Forecast error: {e}")
        return None

def display_forecast():
    """Display forecast results if available"""
    if 'forecast_data' in st.session_state:
        forecast = st.session_state['forecast_data']
        st.markdown("### 🔮 12-Month GDP Forecast")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Forecast Period", f"{forecast['forecast_months']} months")
        with col2:
            st.metric("Province", forecast['province'])
        with col3:
            st.metric("AI Powered", "✅ Gemini AI")

        if forecast['data']:
            # Create forecast chart
            chart_data = []
            for month_data in forecast['data']:
                for province, data in month_data['provinces'].items():
                    chart_data.append({
                        'Month': month_data['date'],
                        'Province': province,
                        'GDP_Forecast': data['gdp_forecast'],
                        'Confidence': data['confidence']
                    })

            if chart_data:
                df = pd.DataFrame(chart_data)

                # Forecast line chart
                fig = px.line(df, x='Month', y='GDP_Forecast', color='Province',
                            title="12-Month GDP Forecast (Gemini AI Enhanced)")
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig, use_container_width=True)

                # Confidence chart
                fig2 = px.line(df, x='Month', y='Confidence', color='Province',
                             title="Forecast Confidence Over Time")
                fig2.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font_color='white'
                )
                st.plotly_chart(fig2, use_container_width=True)

                # Data table
                st.subheader("Forecast Data")
                st.dataframe(df, use_container_width=True)
        else:
            st.info("No forecast data available")

def search_province_data(province, metric, days):
    """Search province data using API"""
    try:
        response = requests.get(f"{API_BASE}/search",
                              params={'province': province, 'metric': metric, 'days': days},
                              timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Search failed: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Search error: {e}")
        return None

def get_all_history(days):
    """Get historical data for all provinces"""
    try:
        response = requests.get(f"{API_BASE}/history",
                              params={'days': days}, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"History fetch failed: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"History error: {e}")
        return None

def display_search_results():
    """Display search results if available"""
    if 'search_results' in st.session_state:
        results = st.session_state['search_results']
        st.markdown("### 🔍 Search Results")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Province", results['province'])
        with col2:
            st.metric("Records Found", results['total_records'])
        with col3:
            st.metric("Days Searched", results['days'])

        if results['data']:
            df = pd.DataFrame(results['data'])
            st.dataframe(df, use_container_width=True)

            # Create chart if numeric data available
            if len(df) > 1 and any(col for col in df.columns if col not in ['province', 'timestamp']):
                numeric_cols = [col for col in df.columns if col not in ['province', 'timestamp']]
                if numeric_cols:
                    fig = px.line(df, x='timestamp', y=numeric_cols[0],
                                title=f"{results['province']} - {numeric_cols[0]} Over Time")
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data found for the selected criteria")

def display_history():
    """Display historical data if available"""
    if 'history_data' in st.session_state:
        history = st.session_state['history_data']
        st.markdown("### 📊 Historical Data")

        st.metric("Provinces", len(history['provinces']))

        # Province selector for detailed view
        selected_prov = st.selectbox("View Province Details", history['provinces'])

        if selected_prov in history['data']:
            prov_data = history['data'][selected_prov]
            df = pd.DataFrame(prov_data)

            if not df.empty:
                st.subheader(f"{selected_prov} Historical Data")
                st.dataframe(df, use_container_width=True)

                # Chart
                if 'composite_index' in df.columns:
                    fig = px.line(df, x='timestamp', y='composite_index',
                                title=f"{selected_prov} GDP Index Over Time")
                    st.plotly_chart(fig, use_container_width=True)
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

def chatbot_dialog():
    """The chatbot UI and logic, to be displayed in a dialog."""
    # Gemini-like CSS
    st.markdown("""
    <style>
        .chat-container {
            background: #161b22;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            border: 1px solid #30363d;
        }

        .user-message {
            background: #1f6feb;
            color: white;
            padding: 12px 16px;
            border-radius: 18px;
            margin: 8px 0;
            max-width: 80%;
            margin-left: auto;
            text-align: right;
        }

        .ai-message {
            background: #21262d;
            color: #f0f6fc;
            padding: 12px 16px;
            border-radius: 18px;
            margin: 8px 0;
            max-width: 80%;
            border-left: 3px solid #1f6feb;
        }

        .gemini-header {
            text-align: center;
            padding: 2rem;
            background: linear-gradient(135deg, #1f6feb 0%, #8b5cf6 100%);
            border-radius: 12px;
            margin-bottom: 2rem;
        }

        .sample-questions {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin: 1rem 0;
        }

        .sample-btn {
            background: #21262d;
            border: 1px solid #30363d;
            color: #f0f6fc;
            padding: 8px 12px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 14px;
        }

        .sample-btn:hover {
            background: #30363d;
        }
    </style>
    """, unsafe_allow_html=True)

    def send_message(question):
        """Send message to Gemini API"""
        try:
            response = requests.post(f"{API_BASE}/ask",
                                   json={"question": question},
                                   timeout=15)
            if response.status_code == 200:
                return response.json()['response']['answer']
            else:
                return "Sorry, I couldn't process your request right now."
        except Exception as e:
            return f"Connection error: {str(e)}"

    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    st.markdown("""
    <div class="gemini-header">
        <h1 style="margin: 0; font-size: 2.5rem;">🤖 Gemini AI</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.1rem;">GDP Economic Analysis Assistant</p>
    </div>
    """, unsafe_allow_html=True)

    # Sample questions
    st.markdown("### 💡 Try asking:")
    sample_questions = [
        "Which provinces show unusual economic activity?",
        "What's the GDP forecast for Bujumbura?",
        "Which province has the highest activity?",
        "How is the overall economic situation?",
        "Compare Gitega with other provinces"
    ]

    cols = st.columns(3)
    for i, question in enumerate(sample_questions):
        with cols[i % 3]:
            if st.button(f"💬 {question}", key=f"sample_{i}"):
                st.session_state.chat_history.append({"role": "user", "content": question})
                with st.spinner("🤖 Gemini is thinking..."):
                    response = send_message(question)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()

    # Chat input
    st.markdown("---")
    user_input = st.text_input("💬 Ask Gemini about GDP data:",
                              placeholder="e.g., Which provinces show high economic activity?",
                              key="chat_input")

    if st.button("Send 🚀") and user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.spinner("🤖 Gemini is analyzing..."):
            response = send_message(user_input)
            st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()

    # Display chat history
    st.markdown("### 💬 Chat History")
    chat_container = st.container()

    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="user-message">
                    👤 {message["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="ai-message">
                    🤖 {message["content"]}
                </div>
                """, unsafe_allow_html=True)

    # Clear chat button
    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()

    # Footer
    st.markdown("---")
    st.markdown("**Powered by Google Gemini AI** | Real-time GDP Analysis")


def main():
    # Modern Header
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 3rem;">🌍 AI-Powered GDP Calculator</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem;">Real-time estimation of Burundi's $2.3B informal economy</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar for search functionality and navigation
    with st.sidebar:
        st.markdown("### 🚀 Navigation")

        # Add Chatbot button
        with st.popover("🤖 Ask Gemini AI", use_container_width=True):
            chatbot_dialog()

        st.markdown("---")
        st.markdown("### 🔍 Search & History")

        # Province search
        provinces = ['Bujumbura', 'Gitega', 'Ngozi', 'Kayanza', 'Bururi', 'Cibitoke']
        selected_province = st.selectbox("Select Province", provinces)

        # Metric selection
        metrics = {
            'all': 'All Metrics',
            'mobile_money': 'Mobile Money Sales',
            'electricity': 'Electricity Usage',
            'internet': 'Internet Activity',
            'social_media': 'Social Media'
        }
        selected_metric = st.selectbox("Select Metric", list(metrics.keys()),
                                     format_func=lambda x: metrics[x])

        # Time range
        days = st.slider("Days of History", 1, 30, 7)

        # Search button
        if st.button("🔍 Search Data"):
            search_results = search_province_data(selected_province, selected_metric, days)
            if search_results:
                st.session_state['search_results'] = search_results

        # History button
        if st.button("📊 View All History"):
            history_data = get_all_history(days)
            if history_data:
                st.session_state['history_data'] = history_data

        st.markdown("---")
        st.markdown("### 📈 12-Month Forecast")

        # Forecast controls
        forecast_province = st.selectbox("Forecast Province", ['all'] + provinces, key='forecast_prov')
        forecast_months = st.slider("Forecast Months", 1, 12, 6)

        # Forecast button
        if st.button("🔮 Generate Forecast"):
            forecast_data = get_forecast_data(forecast_province, forecast_months)
            if forecast_data:
                st.session_state['forecast_data'] = forecast_data

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

        # Display search results and history
        display_search_results()
        display_history()
        display_forecast()

        # Auto-refresh only after successful data display
        if auto_refresh:
            time.sleep(refresh_interval)
            st.rerun()

    else:
        st.error("Unable to fetch data. Please ensure the API server is running on localhost:5000")
        st.info("Run: `python api.py` to start the backend server")

        # Still show search functionality even if main data fails
        display_search_results()
        display_history()
        display_forecast()

if __name__ == "__main__":
    main()
