#!/usr/bin/env python3
"""
Position Calculator Module for TrainJatri Backend
Handles train position calculations, distance measurements, and GPS coordinate matching
"""

import math
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import random

logger = logging.getLogger(__name__)

class PositionCalculator:
    """Calculates train positions, distances, and coordinates"""
    
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.earth_radius = 6371  # Earth radius in kilometers
        
    def calculate_distance_between_stations(self, station1: str, station2: str) -> float:
        """Calculate distance between two stations using Haversine formula"""
        try:
            stations = self.data_loader.get_stations()
            
            if station1 not in stations or station2 not in stations:
                logger.warning(f"Station not found: {station1} or {station2}")
                return 0.0
            
            # Get coordinates [longitude, latitude]
            lon1, lat1 = stations[station1]
            lon2, lat2 = stations[station2]
            
            # Convert to radians
            lat1_rad = math.radians(lat1)
            lat2_rad = math.radians(lat2)
            delta_lat = math.radians(lat2 - lat1)
            delta_lon = math.radians(lon2 - lon1)
            
            # Haversine formula
            a = (math.sin(delta_lat / 2) ** 2 + 
                 math.cos(lat1_rad) * math.cos(lat2_rad) * 
                 math.sin(delta_lon / 2) ** 2)
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            
            distance = self.earth_radius * c
            return round(distance, 2)
            
        except Exception as e:
            logger.error(f"Error calculating distance between stations: {e}")
            return 0.0
    
    def calculate_total_route_distance(self, route_stations: List[str]) -> float:
        """Calculate total distance of a route"""
        try:
            total_distance = 0.0
            
            for i in range(len(route_stations) - 1):
                distance = self.calculate_distance_between_stations(
                    route_stations[i], route_stations[i + 1]
                )
                total_distance += distance
            
            return round(total_distance, 2)
            
        except Exception as e:
            logger.error(f"Error calculating total route distance: {e}")
            return 0.0
    
    def calculate_train_position(self, train_number: str, current_time: datetime) -> Dict[str, Any]:
        """Calculate current train position based on schedule and time"""
        try:
            schedule = self.data_loader.get_schedule_by_train(train_number)
            if not schedule:
                return {"error": "Train schedule not found"}
            
            routes = schedule.get('data', {}).get('routes', [])
            if not routes:
                return {"error": "No routes found in schedule"}
            
            # Find current position based on time
            current_station_idx = self._find_current_station_index(routes, current_time)
            
            if current_station_idx is None:
                return {"error": "Unable to determine current position"}
            
            # Calculate progress
            total_stations = len(routes)
            progress_percentage = (current_station_idx / (total_stations - 1)) * 100
            
            # Calculate distances
            distance_covered = self._calculate_distance_covered(routes, current_station_idx)
            distance_to_next = self._calculate_distance_to_next(routes, current_station_idx)
            
            # Calculate ETA to next station
            eta_to_next = self._calculate_eta_to_next(routes, current_station_idx, current_time)
            
            return {
                "current_station_idx": current_station_idx,
                "current_station": routes[current_station_idx]['city'],
                "next_station": routes[current_station_idx + 1]['city'] if current_station_idx + 1 < total_stations else None,
                "progress_percentage": round(progress_percentage, 2),
                "distance_covered": round(distance_covered, 2),
                "distance_to_next": round(distance_to_next, 2),
                "eta_to_next": eta_to_next,
                "total_stations": total_stations,
                "current_time": current_time.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error calculating train position: {e}")
            return {"error": str(e)}
    
    def _find_current_station_index(self, routes: List[Dict[str, Any]], current_time: datetime) -> Optional[int]:
        """Find the current station index based on time"""
        try:
            for i, route in enumerate(routes):
                if 'departure_time' in route and route['departure_time']:
                    try:
                        departure_time = self._parse_time_string(route['departure_time'])
                        if departure_time and departure_time > current_time:
                            return max(0, i - 1)
                    except:
                        continue
            
            return len(routes) - 1
            
        except Exception as e:
            logger.error(f"Error finding current station index: {e}")
            return None
    
    def _parse_time_string(self, time_str: str) -> Optional[datetime]:
        """Parse time string in format 'HH:MM am/pm BST'"""
        try:
            time_part = time_str.replace(' BST', '').strip()
            time_obj = datetime.strptime(time_part, '%I:%M %p')
            today = datetime.now()
            parsed_time = today.replace(
                hour=time_obj.hour,
                minute=time_obj.minute,
                second=0,
                microsecond=0
            )
            return parsed_time
            
        except Exception as e:
            logger.warning(f"Error parsing time string '{time_str}': {e}")
            return None
    
    def _calculate_distance_covered(self, routes: List[Dict[str, Any]], current_idx: int) -> float:
        """Calculate total distance covered up to current station"""
        try:
            total_distance = 0.0
            
            for i in range(current_idx):
                if i + 1 < len(routes):
                    distance = self.calculate_distance_between_stations(
                        routes[i]['city'], routes[i + 1]['city']
                    )
                    total_distance += distance
            
            return total_distance
            
        except Exception as e:
            logger.error(f"Error calculating distance covered: {e}")
            return 0.0
    
    def _calculate_distance_to_next(self, routes: List[Dict[str, Any]], current_idx: int) -> float:
        """Calculate distance to next station"""
        try:
            if current_idx + 1 >= len(routes):
                return 0.0
            
            return self.calculate_distance_between_stations(
                routes[current_idx]['city'], routes[current_idx + 1]['city']
            )
            
        except Exception as e:
            logger.error(f"Error calculating distance to next: {e}")
            return 0.0
    
    def _calculate_eta_to_next(self, routes: List[Dict[str, Any]], current_idx: int, current_time: datetime) -> Optional[str]:
        """Calculate ETA to next station"""
        try:
            if current_idx + 1 >= len(routes):
                return None
            
            next_route = routes[current_idx + 1]
            if 'arrival_time' not in next_route or not next_route['arrival_time']:
                return None
            
            arrival_time = self._parse_time_string(next_route['arrival_time'])
            if not arrival_time:
                return None
            
            time_diff = arrival_time - current_time
            
            if time_diff.total_seconds() <= 0:
                return "Arrived"
            
            hours = int(time_diff.total_seconds() // 3600)
            minutes = int((time_diff.total_seconds() % 3600) // 60)
            
            if hours > 0:
                return f"{hours}h {minutes}m"
            else:
                return f"{minutes}m"
                
        except Exception as e:
            logger.error(f"Error calculating ETA to next: {e}")
            return None
    
    def estimate_train_speed(self, train_number: str, current_time: datetime) -> float:
        """Estimate current train speed based on schedule and position"""
        try:
            position = self.calculate_train_position(train_number, current_time)
            if 'error' in position:
                return 0.0
            
            base_speed = 60.0  # km/h base speed
            
            hour = current_time.hour
            if 6 <= hour <= 9 or 17 <= hour <= 20:
                speed_multiplier = 0.8
            elif 22 <= hour or hour <= 5:
                speed_multiplier = 1.2
            else:
                speed_multiplier = 1.0
            
            random_factor = random.uniform(0.9, 1.1)
            estimated_speed = base_speed * speed_multiplier * random_factor
            return round(estimated_speed, 1)
            
        except Exception as e:
            logger.error(f"Error estimating train speed: {e}")
            return 0.0

def get_position_calculator(data_loader) -> PositionCalculator:
    """Get a position calculator instance"""
    return PositionCalculator(data_loader)
