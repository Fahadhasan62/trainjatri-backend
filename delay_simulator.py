#!/usr/bin/env python3
"""
Delay Simulator Module for TrainJatri Backend
Generates realistic train delays based on various factors
"""

import random
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import math

logger = logging.getLogger(__name__)

class DelaySimulator:
    """Simulates realistic train delays based on various factors"""
    
    def __init__(self):
        # Base delay probabilities and ranges
        self.base_delay_probability = 0.3  # 30% chance of delay
        self.base_delay_range = (5, 25)  # 5-25 minutes base delay
        
        # Weather impact factors
        self.weather_factors = {
            'clear': 1.0,
            'cloudy': 1.2,
            'rainy': 1.5,
            'stormy': 2.0,
            'foggy': 1.8
        }
        
        # Time of day factors
        self.time_factors = {
            'early_morning': 0.8,    # 5-8 AM
            'morning_rush': 1.4,     # 8-10 AM
            'mid_morning': 1.0,      # 10-12 PM
            'afternoon': 1.1,        # 12-5 PM
            'evening_rush': 1.6,     # 5-8 PM
            'late_evening': 1.2,     # 8-10 PM
            'night': 0.9             # 10 PM - 5 AM
        }
        
        # Day of week factors
        self.day_factors = {
            'Monday': 1.3,
            'Tuesday': 1.1,
            'Wednesday': 1.0,
            'Thursday': 1.1,
            'Friday': 1.4,
            'Saturday': 0.9,
            'Sunday': 0.8
        }
        
        # Station-specific delay factors
        self.station_delay_factors = {
            'Dhaka': 1.5,           # Major hub, more delays
            'Chattogram': 1.4,
            'Rajshahi': 1.2,
            'Khulna': 1.2,
            'Sylhet': 1.1,
            'Barisal': 1.1,
            'Rangpur': 1.1,
            'Mymensingh': 1.0
        }
        
        # Historical delay patterns (simulated)
        self.historical_patterns = {}
    
    def simulate_delay(self, train_number: str, current_station: str, 
                      scheduled_time: datetime, current_time: datetime,
                      weather_condition: str = 'clear') -> Dict[str, Any]:
        """Simulate delay for a specific train at a specific station"""
        try:
            # Calculate base delay
            base_delay = self._calculate_base_delay()
            
            # Apply various factors
            weather_factor = self.weather_factors.get(weather_condition, 1.0)
            time_factor = self._get_time_factor(current_time)
            day_factor = self._get_day_factor(current_time)
            station_factor = self._get_station_factor(current_station)
            
            # Calculate final delay
            final_delay = base_delay * weather_factor * time_factor * day_factor * station_factor
            
            # Add some randomness
            random_factor = random.uniform(0.8, 1.2)
            final_delay = int(final_delay * random_factor)
            
            # Ensure delay is within reasonable bounds
            final_delay = max(0, min(final_delay, 120))  # Max 2 hours
            
            # Calculate actual time
            actual_time = scheduled_time + timedelta(minutes=final_delay)
            
            # Update historical patterns
            self._update_historical_patterns(train_number, current_station, final_delay)
            
            return {
                'delay_minutes': final_delay,
                'scheduled_time': scheduled_time.isoformat(),
                'actual_time': actual_time.isoformat(),
                'weather_condition': weather_condition,
                'factors_applied': {
                    'weather': weather_factor,
                    'time_of_day': time_factor,
                    'day_of_week': day_factor,
                    'station': station_factor
                }
            }
            
        except Exception as e:
            logger.error(f"Error simulating delay: {e}")
            return {
                'delay_minutes': 0,
                'scheduled_time': scheduled_time.isoformat(),
                'actual_time': scheduled_time.isoformat(),
                'weather_condition': weather_condition,
                'factors_applied': {}
            }
    
    def _calculate_base_delay(self) -> int:
        """Calculate base delay based on probability"""
        if random.random() < self.base_delay_probability:
            return random.randint(*self.base_delay_range)
        return 0
    
    def _get_time_factor(self, current_time: datetime) -> float:
        """Get delay factor based on time of day"""
        hour = current_time.hour
        
        if 5 <= hour < 8:
            return self.time_factors['early_morning']
        elif 8 <= hour < 10:
            return self.time_factors['morning_rush']
        elif 10 <= hour < 12:
            return self.time_factors['mid_morning']
        elif 12 <= hour < 17:
            return self.time_factors['afternoon']
        elif 17 <= hour < 20:
            return self.time_factors['evening_rush']
        elif 20 <= hour < 22:
            return self.time_factors['late_evening']
        else:
            return self.time_factors['night']
    
    def _get_day_factor(self, current_time: datetime) -> float:
        """Get delay factor based on day of week"""
        day_name = current_time.strftime('%A')
        return self.day_factors.get(day_name, 1.0)
    
    def _get_station_factor(self, station_name: str) -> float:
        """Get delay factor based on station"""
        for station_pattern, factor in self.station_delay_factors.items():
            if station_pattern.lower() in station_name.lower():
                return factor
        return 1.0
    
    def _update_historical_patterns(self, train_number: str, station: str, delay: int):
        """Update historical delay patterns for analysis"""
        try:
            if train_number not in self.historical_patterns:
                self.historical_patterns[train_number] = {}
            
            if station not in self.historical_patterns[train_number]:
                self.historical_patterns[train_number][station] = []
            
            # Keep only last 100 delays for memory management
            delays = self.historical_patterns[train_number][station]
            delays.append({
                'delay': delay,
                'timestamp': datetime.now().isoformat()
            })
            
            if len(delays) > 100:
                delays.pop(0)
                
        except Exception as e:
            logger.warning(f"Error updating historical patterns: {e}")
    
    def get_historical_delay_stats(self, train_number: str, station: str = None) -> Dict[str, Any]:
        """Get historical delay statistics for a train or station"""
        try:
            if train_number not in self.historical_patterns:
                return {'error': 'No historical data available'}
            
            if station:
                # Station-specific stats
                if station not in self.historical_patterns[train_number]:
                    return {'error': 'No data for this station'}
                
                delays = [d['delay'] for d in self.historical_patterns[train_number][station]]
            else:
                # All stations for this train
                all_delays = []
                for station_delays in self.historical_patterns[train_number].values():
                    all_delays.extend([d['delay'] for d in station_delays])
                delays = all_delays
            
            if not delays:
                return {'error': 'No delay data available'}
            
            return {
                'total_delays': len(delays),
                'average_delay': round(sum(delays) / len(delays), 1),
                'max_delay': max(delays),
                'min_delay': min(delays),
                'delay_distribution': self._get_delay_distribution(delays)
            }
            
        except Exception as e:
            logger.error(f"Error getting historical delay stats: {e}")
            return {'error': str(e)}
    
    def _get_delay_distribution(self, delays: List[int]) -> Dict[str, int]:
        """Get distribution of delays by ranges"""
        distribution = {
            '0-15 min': 0,
            '16-30 min': 0,
            '31-60 min': 0,
            '60+ min': 0
        }
        
        for delay in delays:
            if delay <= 15:
                distribution['0-15 min'] += 1
            elif delay <= 30:
                distribution['16-30 min'] += 1
            elif delay <= 60:
                distribution['31-60 min'] += 1
            else:
                distribution['60+ min'] += 1
        
        return distribution
    
    def predict_delay_probability(self, train_number: str, station: str, 
                                scheduled_time: datetime) -> Dict[str, Any]:
        """Predict probability of delay for a specific train at a specific station"""
        try:
            # Get historical stats
            stats = self.get_historical_delay_stats(train_number, station)
            if 'error' in stats:
                return stats
            
            # Calculate delay probability based on historical data
            total_delays = stats['total_delays']
            if total_delays == 0:
                return {'delay_probability': 0.3, 'confidence': 'low'}
            
            # Calculate probability based on historical patterns
            delayed_count = sum(1 for d in self.historical_patterns[train_number][station] if d['delay'] > 0)
            historical_probability = delayed_count / total_delays
            
            # Apply time and day factors
            time_factor = self._get_time_factor(scheduled_time)
            day_factor = self._get_day_factor(scheduled_time)
            
            # Adjust probability based on factors
            adjusted_probability = historical_probability * time_factor * day_factor
            
            # Ensure probability is within reasonable bounds
            adjusted_probability = max(0.1, min(adjusted_probability, 0.9))
            
            # Determine confidence level
            if total_delays >= 50:
                confidence = 'high'
            elif total_delays >= 20:
                confidence = 'medium'
            else:
                confidence = 'low'
            
            return {
                'delay_probability': round(adjusted_probability, 3),
                'confidence': confidence,
                'historical_data_points': total_delays,
                'factors_applied': {
                    'time_of_day': time_factor,
                    'day_of_week': day_factor
                }
            }
            
        except Exception as e:
            logger.error(f"Error predicting delay probability: {e}")
            return {'error': str(e)}
    
    def get_weather_condition(self, location: str = None) -> str:
        """Get current weather condition (simulated)"""
        # In a real system, this would call a weather API
        # For now, simulate based on time and random factors
        
        current_hour = datetime.now().hour
        
        # Simulate weather patterns
        if 6 <= current_hour <= 18:  # Daytime
            conditions = ['clear', 'cloudy', 'rainy']
            weights = [0.6, 0.3, 0.1]
        else:  # Nighttime
            conditions = ['clear', 'cloudy', 'foggy']
            weights = [0.7, 0.2, 0.1]
        
        return random.choices(conditions, weights=weights)[0]
    
    def simulate_route_delays(self, route_stations: List[Dict[str, Any]], 
                             start_time: datetime) -> List[Dict[str, Any]]:
        """Simulate delays for an entire route"""
        try:
            simulated_route = []
            current_time = start_time
            
            for i, station in enumerate(route_stations):
                # Simulate delay for this station
                weather = self.get_weather_condition(station.get('city', ''))
                
                if 'departure_time' in station and station['departure_time']:
                    scheduled_departure = self._parse_time_string(station['departure_time'])
                    if scheduled_departure:
                        delay_info = self.simulate_delay(
                            'ROUTE_SIMULATION', 
                            station['city'], 
                            scheduled_departure, 
                            current_time, 
                            weather
                        )
                        
                        simulated_station = station.copy()
                        simulated_station['simulated_delay'] = delay_info
                        simulated_station['weather_condition'] = weather
                        
                        simulated_route.append(simulated_station)
                        
                        # Update current time for next station
                        if delay_info['actual_time']:
                            current_time = datetime.fromisoformat(delay_info['actual_time'])
                    else:
                        simulated_route.append(station)
                else:
                    simulated_route.append(station)
            
            return simulated_route
            
        except Exception as e:
            logger.error(f"Error simulating route delays: {e}")
            return route_stations
    
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

def get_delay_simulator() -> DelaySimulator:
    """Get a delay simulator instance"""
    return DelaySimulator()
