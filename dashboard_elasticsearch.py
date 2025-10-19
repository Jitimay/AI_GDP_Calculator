import streamlit as st
import requests
import plotly.graph_objects as go
from elasticsearch_client import ElasticsearchClient

st.set_page_config(page_title="AI GDP Calculator - Enhanced", layout="wide")

# Initialize Elasticsearch client
es_client = ElasticsearchClient()

def main():
    st.title("🌍 AI-Powered GDP Calculator with Elasticsearch")
    
    # Real-time search
    st.sidebar.header("Search & Analytics")
    province = st.sidebar.selectbox("Province", ['All', 'Bujumbura', 'Gitega', 'Ngozi'])
    hours = st.sidebar.slider("Time Range (hours)", 1, 168, 24)
    
    if st.sidebar.button("Search Trends"):
        results = es_client.search_gdp_trends(
            province if province != 'All' else None, 
            hours
        )
        
        # Display aggregated results
        if 'aggregations' in results:
            st.subheader("GDP Trends by Province")
            
            for bucket in results['aggregations']['provinces']['buckets']:
                prov_name = bucket['key']
                avg_gdp = bucket['avg_gdp']['value']
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(f"{prov_name} Avg GDP", f"{avg_gdp:.1f}")
                
                with col2:
                    # Plot trend
                    trend_data = bucket['trend']['buckets']
                    timestamps = [b['key_as_string'] for b in trend_data]
                    values = [b['gdp_avg']['value'] for b in trend_data]
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=timestamps, y=values, name=prov_name))
                    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
