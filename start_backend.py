#!/usr/bin/env python3
"""
TrainJatri Backend Startup Script
Comprehensive startup with health checks and data validation
"""

import os
import sys
import time
import logging
import subprocess
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        logger.error("Python 3.8 or higher is required")
        return False
    logger.info(f"Python version: {sys.version}")
    return True

def check_dependencies():
    """Check if required Python packages are installed"""
    required_packages = [
        'flask', 'flask_cors', 'werkzeug', 'jinja2'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"Missing packages: {', '.join(missing_packages)}")
        logger.info("Install missing packages with: pip install -r requirements.txt")
        return False
    
    logger.info("All required packages are installed")
    return True

def check_data_files():
    """Check if required data files exist"""
    required_files = [
        'stations.json',
        'Bangladesh_500m_segments.json',
        'schedules/'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        logger.error(f"Missing data files: {', '.join(missing_files)}")
        return False
    
    logger.info("All required data files are present")
    return True

def validate_data_integrity():
    """Validate data file integrity"""
    try:
        # Test data loader
        from data_loader import get_data_loader
        data_loader = get_data_loader()
        
        # Load all data
        data_status = data_loader.load_all_data()
        
        if 'error' in data_status:
            logger.error(f"Data loading error: {data_status['error']}")
            return False
        
        logger.info(f"Data loaded successfully: {data_status}")
        return True
        
    except Exception as e:
        logger.error(f"Data validation error: {e}")
        return False

def check_port_availability(port=5000):
    """Check if the specified port is available"""
    import socket
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            logger.info(f"Port {port} is available")
            return True
    except OSError:
        logger.error(f"Port {port} is already in use")
        return False

def install_dependencies():
    """Install required dependencies"""
    logger.info("Installing dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True, capture_output=True, text=True)
        logger.info("Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to install dependencies: {e}")
        logger.error(f"Error output: {e.stderr}")
        return False

def start_backend():
    """Start the backend server"""
    logger.info("Starting TrainJatri Backend...")
    
    try:
        # Import and start the Flask app
        from train_timeline_api import app
        from config import get_config
        
        # Get configuration
        config = get_config()
        
        logger.info(f"Starting server on {config.HOST}:{config.PORT}")
        logger.info(f"Debug mode: {config.DEBUG}")
        logger.info(f"API version: {config.API_VERSION}")
        
        # Start the server
        app.run(
            host=config.HOST,
            port=config.PORT,
            debug=config.DEBUG,
            use_reloader=False  # Disable reloader for production-like behavior
        )
        
    except Exception as e:
        logger.error(f"Failed to start backend: {e}")
        return False
    
    return True

def run_health_check():
    """Run a health check on the backend"""
    import requests
    import time
    
    logger.info("Running health check...")
    
    # Wait for server to start
    time.sleep(3)
    
    try:
        response = requests.get('http://localhost:5000/api/health', timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            logger.info("Backend is healthy!")
            logger.info(f"Status: {health_data.get('status')}")
            logger.info(f"Version: {health_data.get('version')}")
            logger.info(f"Data sources: {health_data.get('data_sources')}")
            return True
        else:
            logger.error(f"Health check failed with status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"Health check failed: {e}")
        return False

def main():
    """Main startup function"""
    logger.info("=" * 50)
    logger.info("TrainJatri Backend Startup")
    logger.info("=" * 50)
    
    # Step 1: Check Python version
    logger.info("Step 1: Checking Python version...")
    if not check_python_version():
        sys.exit(1)
    
    # Step 2: Check dependencies
    logger.info("Step 2: Checking dependencies...")
    if not check_dependencies():
        logger.info("Attempting to install dependencies...")
        if not install_dependencies():
            logger.error("Failed to install dependencies. Please install manually.")
            sys.exit(1)
    
    # Step 3: Check data files
    logger.info("Step 3: Checking data files...")
    if not check_data_files():
        logger.error("Required data files are missing. Please ensure all data files are present.")
        sys.exit(1)
    
    # Step 4: Validate data integrity
    logger.info("Step 4: Validating data integrity...")
    if not validate_data_integrity():
        logger.error("Data validation failed. Please check your data files.")
        sys.exit(1)
    
    # Step 5: Check port availability
    logger.info("Step 5: Checking port availability...")
    if not check_port_availability():
        logger.error("Port 5000 is not available. Please free up the port or change the configuration.")
        sys.exit(1)
    
    # Step 6: Start backend
    logger.info("Step 6: Starting backend server...")
    if not start_backend():
        logger.error("Failed to start backend server.")
        sys.exit(1)
    
    # Step 7: Health check (if running in background)
    logger.info("Backend startup completed successfully!")
    logger.info("=" * 50)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Startup interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error during startup: {e}")
        sys.exit(1)
