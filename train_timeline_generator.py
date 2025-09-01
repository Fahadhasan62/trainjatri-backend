#!/usr/bin/env python3
"""
Train Timeline Generator Module for TrainJatri Backend
Generates comprehensive train status timelines
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from data_loader import get_data_loader
from position_calculator import get_position_calculator
from delay_simulator import get_delay_simulator

logger = logging.getLogger(__name__)

class TrainTimelineGenerator:
    """Generates comprehensive train status timelines"""
    
    def __init__(self):
        self.data_loader = get_data_loader()
        self.position_calculator = get_position_calculator(self.data_loader)
        self.delay_simulator = get_delay_simulator()
    
    def generate_train_status(self, train_number: str) -> Dict[str, Any]:
        """Generate complete train status with timeline"""
        try:
            schedule = self.data_loader.get_schedule_by_train(train_number)
            if not schedule:
                return {"error": "Train schedule not found"}
            
            current_time = datetime.now()
            routes = schedule.get('data', {}).get('routes', [])
            
            # Generate station statuses
            station_statuses = self._generate_station_statuses(routes, current_time)
            
            # Calculate position and metrics
            position_info = self.position_calculator.calculate_train_position(
                train_number, current_time
            )
            
            current_speed = self.position_calculator.estimate_train_speed(
                train_number, current_time
            )
            
            # Create status response
            status_data = {
                'train_number': train_number,
                'train_name': schedule.get('data', {}).get('train_name', 'Unknown'),
                'station_statuses': station_statuses,
                'current_speed': current_speed,
                'distance_covered': position_info.get('distance_covered', 0),
                'distance_to_next': position_info.get('distance_to_next', 0),
                'delay_minutes': self._calculate_total_delay(station_statuses),
                'estimated_arrival': position_info.get('eta_to_next', 'Unknown'),
                'progress_percentage': position_info.get('progress_percentage', 0),
                'current_station': position_info.get('current_station', 'Unknown'),
                'next_station': position_info.get('next_station', 'Unknown'),
                'weather_condition': self.delay_simulator.get_weather_condition(),
                'last_updated': current_time.isoformat()
            }
            
            return status_data
            
        except Exception as e:
            logger.error(f"Error generating train status: {e}")
            return {"error": str(e)}
    
    def _generate_station_statuses(self, routes: List[Dict[str, Any]], current_time: datetime) -> List[Dict[str, Any]]:
        """Generate status for each station"""
        try:
            station_statuses = []
            
            for i, route in enumerate(routes):
                station_name = route['city']
                status = self._determine_station_status(i, routes, current_time)
                
                # Parse times and simulate delays
                scheduled_arrival = self._parse_time_string(route.get('arrival_time'))
                scheduled_departure = self._parse_time_string(route.get('departure_time'))
                
                delay_info = self._simulate_station_delays(
                    station_name, scheduled_arrival, scheduled_departure, current_time
                )
                
                # Calculate distance
                distance_from_start = self._calculate_distance_from_start(routes, i)
                
                station_status = {
                    'station_name': station_name,
                    'status': status,
                    'scheduled_arrival': scheduled_arrival.isoformat() if scheduled_arrival else None,
                    'scheduled_departure': scheduled_departure.isoformat() if scheduled_departure else None,
                    'actual_arrival': delay_info.get('actual_arrival'),
                    'actual_departure': delay_info.get('actual_departure'),
                    'delay_minutes': delay_info.get('delay_minutes', 0),
                    'halt_duration': route.get('halt', '---'),
                    'duration': route.get('duration', '---'),
                    'distance_from_start': round(distance_from_start, 2),
                    'weather_condition': self.delay_simulator.get_weather_condition(station_name),
                    'crowd_level': self._estimate_crowd_level(station_name, scheduled_arrival)
                }
                
                station_statuses.append(station_status)
            
            return station_statuses
            
        except Exception as e:
            logger.error(f"Error generating station statuses: {e}")
            return []
    
    def _determine_station_status(self, station_idx: int, routes: List[Dict[str, Any]], 
                                 current_time: datetime) -> str:
        """Determine station status"""
        try:
            current_position = self._find_current_position(routes, current_time)
            
            if station_idx < current_position:
                return 'completed'
            elif station_idx == current_position:
                return 'current'
            elif station_idx == current_position + 1:
                return 'next'
            else:
                return 'upcoming'
                
        except Exception as e:
            return 'upcoming'
    
    def _find_current_position(self, routes: List[Dict[str, Any]], current_time: datetime) -> int:
        """Find current train position"""
        try:
            for i, route in enumerate(routes):
                if 'departure_time' in route and route['departure_time']:
                    departure_time = self._parse_time_string(route['departure_time'])
                    if departure_time and departure_time > current_time:
                        return max(0, i - 1)
            return len(routes) - 1
            
        except Exception as e:
            return 0
    
    def _simulate_station_delays(self, station_name: str, scheduled_arrival: datetime, 
                                scheduled_departure: datetime, current_time: datetime) -> Dict[str, Any]:
        """Simulate station delays"""
        try:
            weather = self.delay_simulator.get_weather_condition(station_name)
            
            arrival_delay = 0
            actual_arrival = scheduled_arrival
            if scheduled_arrival:
                arrival_delay_info = self.delay_simulator.simulate_delay(
                    'STATION_SIMULATION', station_name, scheduled_arrival, current_time, weather
                )
                arrival_delay = arrival_delay_info.get('delay_minutes', 0)
                if arrival_delay > 0:
                    actual_arrival = scheduled_arrival + timedelta(minutes=arrival_delay)
            
            departure_delay = 0
            actual_departure = scheduled_departure
            if scheduled_departure:
                departure_delay_info = self.delay_simulator.simulate_delay(
                    'STATION_SIMULATION', station_name, scheduled_departure, current_time, weather
                )
                departure_delay = departure_delay_info.get('delay_minutes', 0)
                if departure_delay > 0:
                    actual_departure = scheduled_departure + timedelta(minutes=departure_delay)
            
            total_delay = max(arrival_delay, departure_delay)
            
            return {
                'delay_minutes': total_delay,
                'actual_arrival': actual_arrival.isoformat() if actual_arrival else None,
                'actual_departure': actual_departure.isoformat() if actual_departure else None,
                'weather_condition': weather
            }
            
        except Exception as e:
            return {
                'delay_minutes': 0,
                'actual_arrival': scheduled_arrival.isoformat() if scheduled_arrival else None,
                'actual_departure': scheduled_departure.isoformat() if scheduled_departure else None,
                'weather_condition': 'clear'
            }
    
    def _calculate_distance_from_start(self, routes: List[Dict[str, Any]], station_idx: int) -> float:
        """Calculate distance from start"""
        try:
            if station_idx == 0:
                return 0.0
            
            total_distance = 0.0
            for i in range(station_idx):
                if i + 1 < len(routes):
                    distance = self.position_calculator.calculate_distance_between_stations(
                        routes[i]['city'], routes[i + 1]['city']
                    )
                    total_distance += distance
            
            return total_distance
            
        except Exception as e:
            return 0.0
    
    def _calculate_total_delay(self, station_statuses: List[Dict[str, Any]]) -> int:
        """Calculate total delay across all stations"""
        try:
            return max([status.get('delay_minutes', 0) for status in station_statuses])
        except Exception as e:
            return 0
    
    def _estimate_crowd_level(self, station_name: str, scheduled_time: datetime) -> str:
        """Estimate crowd level"""
        try:
            if not scheduled_time:
                return 'normal'
            
            hour = scheduled_time.hour
            major_stations = ['Dhaka', 'Chattogram', 'Rajshahi', 'Khulna', 'Sylhet']
            is_major_station = any(major in station_name for major in major_stations)
            
            if 7 <= hour <= 9 or 17 <= hour <= 19:
                return 'high' if is_major_station else 'medium'
            elif 22 <= hour or hour <= 5:
                return 'low'
            else:
                return 'medium' if is_major_station else 'normal'
                
        except Exception as e:
            return 'normal'
    
    def _parse_time_string(self, time_str: str) -> Optional[datetime]:
        """Parse time string"""
        try:
            if not time_str or time_str == '---':
                return None
            
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
            return None

def get_train_timeline_generator() -> TrainTimelineGenerator:
    """Get timeline generator instance"""
    return TrainTimelineGenerator()
