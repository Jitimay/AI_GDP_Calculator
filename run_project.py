#!/usr/bin/env python3
from api import app

if __name__ == '__main__':
    print("🚀 Starting GDP Calculator API on port 5001")
    app.run(host='0.0.0.0', port=5001, debug=True)
