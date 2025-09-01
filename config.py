#!/usr/bin/env python3
"""
Configuration file for TrainJatri Backend
"""

import os
from typing import Dict, Any

class Config:
    """Base configuration class"""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'train-jatri-secret-key-2024'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Server settings
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5000))
    
    # Data settings
    DATA_DIR = os.environ.get('DATA_DIR', '.')
    CACHE_DURATION = int(os.environ.get('CACHE_DURATION', 300))  # 5 minutes
    
    # File paths
    STATIONS_FILE = os.path.join(DATA_DIR, 'stations.json')
    SEGMENTS_FILE = os.path.join(DATA_DIR, 'Bangladesh_500m_segments.json')
    SCHEDULES_DIR = os.path.join(DATA_DIR, 'schedules')
    CROWD_VALIDATIONS_FILE = os.path.join(DATA_DIR, 'crowd_validations.json')
    
    # Crowd validation settings
    CROWD_VALIDATION_TIMEOUT = int(os.environ.get('CROWD_VALIDATION_TIMEOUT', 7200))  # 2 hours
    MAX_VALIDATIONS_PER_TRAIN = int(os.environ.get('MAX_VALIDATIONS_PER_TRAIN', 1000))
    
    # Delay simulation settings
    BASE_DELAY_PROBABILITY = float(os.environ.get('BASE_DELAY_PROBABILITY', 0.3))
    MAX_DELAY_MINUTES = int(os.environ.get('MAX_DELAY_MINUTES', 120))
    
    # Position calculation settings
    EARTH_RADIUS_KM = 6371.0
    GPS_ACCURACY_METERS = float(os.environ.get('GPS_ACCURACY_METERS', 100.0))
    
    # Logging settings
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # API settings
    API_VERSION = '2.0.0'
    API_TITLE = 'TrainJatri Backend API'
    API_DESCRIPTION = 'Comprehensive train tracking and scheduling API for Bangladesh Railway'
    
    # Rate limiting (requests per minute)
    RATE_LIMIT = int(os.environ.get('RATE_LIMIT', 100))
    
    # CORS settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    @classmethod
    def get_data_paths(cls) -> Dict[str, str]:
        """Get all data file paths"""
        return {
            'stations': cls.STATIONS_FILE,
            'segments': cls.SEGMENTS_FILE,
            'schedules': cls.SCHEDULES_DIR,
            'crowd_validations': cls.CROWD_VALIDATIONS_FILE
        }
    
    @classmethod
    def validate_paths(cls) -> Dict[str, bool]:
        """Validate that all required data paths exist"""
        paths = cls.get_data_paths()
        validation = {}
        
        for name, path in paths.items():
            if name == 'schedules':
                # Check if directory exists
                validation[name] = os.path.isdir(path)
            else:
                # Check if file exists
                validation[name] = os.path.isfile(path)
        
        return validation

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    CACHE_DURATION = 600  # 10 minutes
    RATE_LIMIT = 50

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    CACHE_DURATION = 60  # 1 minute

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(config_name: str = None) -> Config:
    """Get configuration class by name"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    return config.get(config_name, config['default'])

# Current configuration
current_config = get_config()
