import streamlit as st
import requests
import time
import plotly.graph_objects as go

st.set_page_config(page_title="Real-time GDP Monitor", layout="wide")

API_BASE = "http://localhost:5001"

@st.fragment(run_every=3)  # Updates every 3 seconds
def realtime_metrics():
    try:
        response = requests.get(f"{API_BASE}/predict", timeout=15)  # Increased timeout
        data = response.json()
        
        if data.get('status') == 'success':
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("National GDP Index", f"{data['national_index']:.1f}")
            
            with col2:
                provinces = data['provincial_data']
                top_province = max(provinces.items(), key=lambda x: x[1]['composite_index'])
                st.metric("Top Province", f"{top_province[0]}: {top_province[1]['composite_index']:.1f}")
            
            with col3:
                st.metric("Last Update", time.strftime("%H:%M:%S"))
                
            # Real-time chart
            fig = go.Figure()
            provinces_list = []
            values_list = []
            
            for province, pdata in provinces.items():
                provinces_list.append(province)
                values_list.append(pdata['composite_index'])
            
            fig.add_trace(go.Bar(
                x=provinces_list,
                y=values_list,
                marker_color='lightblue'
            ))
            
            fig.update_layout(
                title="Live GDP by Province", 
                height=400,
                xaxis_title="Province",
                yaxis_title="GDP Index"
            )
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.error("API returned error status")
            
    except requests.exceptions.Timeout:
        st.error("API timeout - server may be busy")
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to API - check if server is running")
    except Exception as e:
        st.error(f"Error: {str(e)}")

st.title("🌍 Real-time GDP Monitor")
st.write("Connecting to API...")
realtime_metrics()
