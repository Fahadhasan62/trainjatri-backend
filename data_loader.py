#!/usr/bin/env python3
"""
Data Loader Module for TrainJatri Backend
Handles loading and caching of all JSON data files
"""

import json
import os
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import glob

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    """Centralized data loader for all TrainJatri data files"""
    
    def __init__(self, data_dir: str = "."):
        self.data_dir = data_dir
        self._stations = None
        self._segments = None
        self._schedules = {}
        self._route_mappings = {}
        self._last_loaded = None
        self._cache_duration = 300  # 5 minutes cache
        
    def load_all_data(self, force_reload: bool = False) -> Dict[str, Any]:
        """Load all data files and return status"""
        try:
            if not force_reload and self._is_cache_valid():
                logger.info("Using cached data")
                return self._get_cache_status()
            
            logger.info("Loading all data files...")
            
            # Load stations
            self._stations = self._load_stations()
            
            # Load segments
            self._segments = self._load_segments()
            
            # Load schedules
            self._schedules = self._load_schedules()
            
            # Load route mappings
            self._route_mappings = self._load_route_mappings()
            
            self._last_loaded = datetime.now()
            
            status = self._get_cache_status()
            logger.info(f"Data loaded successfully: {status}")
            return status
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return {"error": str(e)}
    
    def _is_cache_valid(self) -> bool:
        """Check if cached data is still valid"""
        if not self._last_loaded:
            return False
        
        elapsed = (datetime.now() - self._last_loaded).total_seconds()
        return elapsed < self._cache_duration
    
    def _get_cache_status(self) -> Dict[str, Any]:
        """Get status of loaded data"""
        return {
            "stations_count": len(self._stations) if self._stations else 0,
            "segments_count": len(self._segments) if self._segments else 0,
            "schedules_count": len(self._schedules),
            "route_mappings_count": len(self._route_mappings),
            "last_loaded": self._last_loaded.isoformat() if self._last_loaded else None,
            "cache_valid": self._is_cache_valid()
        }
    
    def _load_stations(self) -> Dict[str, List[float]]:
        """Load stations.json file"""
        try:
            stations_file = os.path.join(self.data_dir, "stations.json")
            if not os.path.exists(stations_file):
                logger.warning("stations.json not found")
                return {}
            
            with open(stations_file, 'r', encoding='utf-8') as f:
                stations = json.load(f)
            
            logger.info(f"Loaded {len(stations)} stations")
            return stations
            
        except Exception as e:
            logger.error(f"Error loading stations: {e}")
            return {}
    
    def _load_segments(self) -> Dict[str, Any]:
        """Load Bangladesh_500m_segments.json file"""
        try:
            segments_file = os.path.join(self.data_dir, "Bangladesh_500m_segments.json")
            if not os.path.exists(segments_file):
                logger.warning("Bangladesh_500m_segments.json not found")
                return {}
            
            with open(segments_file, 'r', encoding='utf-8') as f:
                segments = json.load(f)
            
            logger.info(f"Loaded {len(segments)} segments")
            return segments
            
        except Exception as e:
            logger.error(f"Error loading segments: {e}")
            return {}
    
    def _load_schedules(self) -> Dict[str, Dict[str, Any]]:
        """Load all schedule files from schedules/ directory"""
        try:
            schedules_dir = os.path.join(self.data_dir, "schedules")
            if not os.path.exists(schedules_dir):
                logger.warning("schedules/ directory not found")
                return {}
            
            schedules = {}
            schedule_files = glob.glob(os.path.join(schedules_dir, "*.json"))
            
            for schedule_file in schedule_files:
                try:
                    with open(schedule_file, 'r', encoding='utf-8') as f:
                        schedule_data = json.load(f)
                    
                    # Extract train number from filename
                    filename = os.path.basename(schedule_file)
                    train_key = filename.replace('.json', '')
                    schedules[train_key] = schedule_data
                    
                except Exception as e:
                    logger.warning(f"Error loading {schedule_file}: {e}")
                    continue
            
            logger.info(f"Loaded {len(schedules)} schedules")
            return schedules
            
        except Exception as e:
            logger.error(f"Error loading schedules: {e}")
            return {}
    
    def _load_route_mappings(self) -> Dict[str, Dict[str, Any]]:
        """Load all train route mapping files"""
        try:
            route_mappings = {}
            
            # Look for route mapping files
            mapping_files = glob.glob(os.path.join(self.data_dir, "*train_route_mapping*.json"))
            
            for mapping_file in mapping_files:
                try:
                    with open(mapping_file, 'r', encoding='utf-8') as f:
                        mapping_data = json.load(f)
                    
                    route_mappings.update(mapping_data)
                    
                except Exception as e:
                    logger.warning(f"Error loading {mapping_file}: {e}")
                    continue
            
            logger.info(f"Loaded {len(route_mappings)} route mappings")
            return route_mappings
            
        except Exception as e:
            logger.error(f"Error loading route mappings: {e}")
            return {}
    
    def get_stations(self) -> Dict[str, List[float]]:
        """Get loaded stations data"""
        if not self._stations:
            self.load_all_data()
        return self._stations or {}
    
    def get_segments(self) -> Dict[str, Any]:
        """Get loaded segments data"""
        if not self._segments:
            self.load_all_data()
        return self._segments or {}
    
    def get_schedules(self) -> Dict[str, Dict[str, Any]]:
        """Get loaded schedules data"""
        if not self._schedules:
            self.load_all_data()
        return self._schedules or {}
    
    def get_route_mappings(self) -> Dict[str, Dict[str, Any]]:
        """Get loaded route mappings data"""
        if not self._route_mappings:
            self.load_all_data()
        return self._route_mappings or {}
    
    def get_schedule_by_train(self, train_number: str) -> Optional[Dict[str, Any]]:
        """Get schedule for a specific train"""
        schedules = self.get_schedules()
        return schedules.get(train_number)
    
    def get_route_mapping_by_train(self, train_number: str) -> Optional[Dict[str, Any]]:
        """Get route mapping for a specific train"""
        route_mappings = self.get_route_mappings()
        return route_mappings.get(train_number)
    
    def search_trains_by_stations(self, from_station: str, to_station: str) -> List[Dict[str, Any]]:
        """Search trains that pass through both stations in correct order"""
        try:
            schedules = self.get_schedules()
            results = []
            
            for train_key, schedule in schedules.items():
                try:
                    routes = schedule.get('data', {}).get('routes', [])
                    route_stations = [route['city'] for route in routes]
                    
                    if from_station in route_stations and to_station in route_stations:
                        from_idx = route_stations.index(from_station)
                        to_idx = route_stations.index(to_station)
                        
                        if from_idx < to_idx:  # Correct direction
                            results.append({
                                'train_key': train_key,
                                'schedule': schedule
                            })
                
                except Exception as e:
                    logger.warning(f"Error processing schedule for {train_key}: {e}")
                    continue
            
            logger.info(f"Found {len(results)} trains between {from_station} and {to_station}")
            return results
            
        except Exception as e:
            logger.error(f"Error searching trains by stations: {e}")
            return []
    
    def search_trains_by_number(self, train_number: str) -> List[Dict[str, Any]]:
        """Search trains by number or partial name"""
        try:
            schedules = self.get_schedules()
            results = []
            
            train_number_lower = train_number.lower()
            
            for train_key, schedule in schedules.items():
                try:
                    train_name = schedule.get('data', {}).get('train_name', '')
                    train_key_lower = train_key.lower()
                    
                    if (train_number_lower in train_key_lower or 
                        train_number_lower in train_name.lower()):
                        results.append({
                            'train_key': train_key,
                            'schedule': schedule
                        })
                
                except Exception as e:
                    logger.warning(f"Error processing schedule for {train_key}: {e}")
                    continue
            
            logger.info(f"Found {len(results)} trains matching '{train_number}'")
            return results
            
        except Exception as e:
            logger.error(f"Error searching trains by number: {e}")
            return []
    
    def get_all_train_numbers(self) -> List[str]:
        """Get list of all available train numbers"""
        schedules = self.get_schedules()
        return list(schedules.keys())
    
    def refresh_cache(self) -> Dict[str, Any]:
        """Force refresh of all cached data"""
        return self.load_all_data(force_reload=True)

# Global instance
data_loader = DataLoader()

def get_data_loader() -> DataLoader:
    """Get the global data loader instance"""
    return data_loader
