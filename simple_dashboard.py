import streamlit as st
import requests
import json

st.set_page_config(page_title="AI GDP Calculator - Hackathon Demo", layout="wide")

st.markdown("# 🌍 AI-Powered GDP Calculator")
st.markdown("### Elasticsearch-Powered Economic Monitoring")

# API connection
API_BASE = "http://localhost:5000"

try:
    # Get current data
    response = requests.get(f"{API_BASE}/predict", timeout=5)
    if response.status_code == 200:
        data = response.json()
        
        st.success("✅ System Status: ONLINE - Elasticsearch Connected")
        
        # National Index with better styling
        st.markdown("### 🇧🇮 National GDP Index")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(f"""
            <div style="text-align: center; padding: 20px; background: linear-gradient(90deg, #1f77b4, #ff7f0e); border-radius: 10px; color: white;">
                <h1 style="margin: 0; font-size: 3em;">{national_idx:.1f}%</h1>
                <p style="margin: 0; font-size: 1.2em;">Real-time GDP Index</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Provincial data
        st.markdown("### 📊 Provincial GDP Indices")
        provincial_data = data.get('provincial_data', {})
        
        cols = st.columns(3)
        for i, (province, pdata) in enumerate(provincial_data.items()):
            with cols[i % 3]:
                gdp_val = pdata.get('composite_index', 0)
                st.metric(f"📍 {province}", f"{gdp_val:.1f}%")
        
        # Show raw data
        with st.expander("🔍 Raw API Response"):
            st.json(data)
            
    else:
        st.error("❌ API Connection Failed")
        
except Exception as e:
    st.error(f"❌ Error: {e}")
    st.info("Make sure API is running: python api.py")

# Show system info
st.markdown("---")
st.markdown("**🎯 Hackathon Features:**")
st.markdown("- ✅ Elasticsearch Integration (Required)")
st.markdown("- ✅ Real-time GDP Calculations") 
st.markdown("- ✅ Multi-source Data Fusion")
st.markdown("- ✅ 400K+ Economic Records")
st.markdown("- ✅ AI-Powered Predictions")
