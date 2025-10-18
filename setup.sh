#!/bin/bash

echo "🔧 Setting up AI-Powered GDP Calculator..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

echo "✅ Setup complete! Now run: ./start_system.sh"
