#!/usr/bin/env python3
"""
TrainJatri App Runner Script
This script helps you run the TrainJatri application with both backend and frontend.
"""

import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def check_python_dependencies():
    """Check if required Python packages are installed"""
    try:
        import flask
        import flask_cors
        print("✅ Python dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing Python dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def check_flutter():
    """Check if Flutter is installed and available"""
    try:
        result = subprocess.run(['flutter', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Flutter is installed")
            return True
        else:
            print("❌ Flutter is not working properly")
            return False
    except FileNotFoundError:
        print("❌ Flutter is not installed or not in PATH")
        print("Please install Flutter from: https://flutter.dev/docs/get-started/install")
        return False

def run_backend():
    """Run the Flask backend server"""
    print("\n🚀 Starting Flask Backend Server...")
    
    # Check if backend files exist
    if not Path("train_timeline_api.py").exists():
        print("❌ Backend file 'train_timeline_api.py' not found!")
        return False
    
    if not Path("stations.json").exists():
        print("❌ Data file 'stations.json' not found!")
        return False
    
    if not Path("schedules").exists():
        print("❌ Schedules directory not found!")
        return False
    
    try:
        # Start the Flask server
        print("📡 Backend server starting on http://localhost:5000")
        print("🔧 API endpoints:")
        print("   - GET  /api/stations")
        print("   - GET  /api/trains/search?from={station}&to={station}")
        print("   - GET  /api/trains/search?number={train_number}")
        print("   - GET  /api/trains/{train_number}/status")
        print("   - POST /api/trains/{train_number}/confirm")
        print("   - GET  /api/health")
        print("\n⏹️  Press Ctrl+C to stop the backend server")
        
        # Run the Flask app
        subprocess.run([sys.executable, "train_timeline_api.py"])
        
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")
        return True
    except Exception as e:
        print(f"❌ Error running backend: {e}")
        return False

def run_flutter():
    """Provide instructions for running Flutter app"""
    print("\n📱 Flutter App Instructions:")
    print("1. Open a new terminal/command prompt")
    print("2. Navigate to the project directory")
    print("3. Run: flutter pub get")
    print("4. Run: flutter run")
    print("\n💡 Make sure the backend server is running first!")

def main():
    """Main function to coordinate the app startup"""
    print("🚂 TrainJatri App Runner")
    print("=" * 40)
    
    # Check dependencies
    if not check_python_dependencies():
        return
    
    if not check_flutter():
        return
    
    print("\n📋 Project Status:")
    print("✅ Python backend ready")
    print("✅ Flutter frontend ready")
    print("✅ Data files available")
    
    # Ask user what they want to do
    print("\n🎯 What would you like to do?")
    print("1. Run backend server only")
    print("2. Get Flutter instructions")
    print("3. Run both (backend + Flutter instructions)")
    print("4. Exit")
    
    while True:
        try:
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                run_backend()
                break
            elif choice == "2":
                run_flutter()
                break
            elif choice == "3":
                print("\n🔄 Starting both backend and Flutter...")
                run_backend()
                run_flutter()
                break
            elif choice == "4":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()


