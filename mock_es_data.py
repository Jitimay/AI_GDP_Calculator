#!/usr/bin/env python3
"""Mock Elasticsearch data for hackathon demo"""

MOCK_ES_DATA = {
    "recent_data": [
        {"province": "Bujumbura", "gdp_index": 75.2, "timestamp": "2024-01-20T10:00:00"},
        {"province": "Gitega", "gdp_index": 68.5, "timestamp": "2024-01-20T10:00:00"},
        {"province": "Ngozi", "gdp_index": 72.1, "timestamp": "2024-01-20T10:00:00"}
    ],
    "alerts": [
        {"province": "Bujumbura", "gdp_index": 85.3, "message": "High economic activity detected"}
    ]
}

def get_mock_data():
    return MOCK_ES_DATA
