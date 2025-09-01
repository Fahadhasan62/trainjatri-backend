#!/usr/bin/env python3
"""
Crowd Validation Module for TrainJatri Backend
Handles user confirmations and crowd-based train status adjustments
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json
import os
import random

logger = logging.getLogger(__name__)

class CrowdValidation:
    """Manages crowd validation for train tracking accuracy"""
    
    def __init__(self, data_file: str = "crowd_validations.json"):
        self.data_file = data_file
        self.validations = self._load_validations()
        
    def _load_validations(self) -> Dict[str, Any]:
        """Load existing validations from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Error loading validations: {e}")
            return {}
    
    def _save_validations(self):
        """Save validations to file"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.validations, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Error saving validations: {e}")
    
    def confirm_user_on_train(self, train_number: str, user_id: str, 
                             station_name: str = None, coordinates: Dict[str, float] = None) -> Dict[str, Any]:
        """Confirm a user is on a specific train"""
        try:
            timestamp = datetime.now().isoformat()
            
            if train_number not in self.validations:
                self.validations[train_number] = {
                    'confirmations': [],
                    'last_updated': timestamp,
                    'total_confirmations': 0
                }
            
            # Check if user already confirmed
            existing_confirmation = None
            for conf in self.validations[train_number]['confirmations']:
                if conf.get('user_id') == user_id:
                    existing_confirmation = conf
                    break
            
            if existing_confirmation:
                # Update existing confirmation
                existing_confirmation.update({
                    'timestamp': timestamp,
                    'station_name': station_name,
                    'coordinates': coordinates
                })
                message = "Confirmation updated"
            else:
                # Add new confirmation
                confirmation = {
                    'user_id': user_id,
                    'timestamp': timestamp,
                    'station_name': station_name,
                    'coordinates': coordinates
                }
                self.validations[train_number]['confirmations'].append(confirmation)
                self.validations[train_number]['total_confirmations'] += 1
                message = "Confirmation added"
            
            self.validations[train_number]['last_updated'] = timestamp
            self._save_validations()
            
            # Calculate crowd metrics
            crowd_metrics = self._calculate_crowd_metrics(train_number)
            
            return {
                'success': True,
                'message': message,
                'train_number': train_number,
                'user_id': user_id,
                'timestamp': timestamp,
                'crowd_metrics': crowd_metrics
            }
            
        except Exception as e:
            logger.error(f"Error confirming user on train: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def remove_user_confirmation(self, train_number: str, user_id: str) -> Dict[str, Any]:
        """Remove a user's confirmation"""
        try:
            if train_number not in self.validations:
                return {
                    'success': False,
                    'error': 'No validations found for this train'
                }
            
            # Find and remove confirmation
            confirmations = self.validations[train_number]['confirmations']
            for i, conf in enumerate(confirmations):
                if conf.get('user_id') == user_id:
                    del confirmations[i]
                    self.validations[train_number]['total_confirmations'] -= 1
                    self.validations[train_number]['last_updated'] = datetime.now().isoformat()
                    self._save_validations()
                    
                    return {
                        'success': True,
                        'message': 'Confirmation removed',
                        'train_number': train_number,
                        'user_id': user_id
                    }
            
            return {
                'success': False,
                'error': 'User confirmation not found'
            }
            
        except Exception as e:
            logger.error(f"Error removing user confirmation: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_train_crowd_data(self, train_number: str) -> Dict[str, Any]:
        """Get crowd data for a specific train"""
        try:
            if train_number not in self.validations:
                return {
                    'train_number': train_number,
                    'total_confirmations': 0,
                    'active_confirmations': 0,
                    'crowd_level': 'low',
                    'last_updated': None,
                    'confirmations': []
                }
            
            train_data = self.validations[train_number]
            active_confirmations = self._get_active_confirmations(train_data['confirmations'])
            
            crowd_level = self._determine_crowd_level(len(active_confirmations))
            
            return {
                'train_number': train_number,
                'total_confirmations': train_data['total_confirmations'],
                'active_confirmations': len(active_confirmations),
                'crowd_level': crowd_level,
                'last_updated': train_data['last_updated'],
                'confirmations': active_confirmations
            }
            
        except Exception as e:
            logger.error(f"Error getting train crowd data: {e}")
            return {
                'error': str(e)
            }
    
    def _get_active_confirmations(self, confirmations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get confirmations that are still active (within last 2 hours)"""
        try:
            active = []
            cutoff_time = datetime.now() - timedelta(hours=2)
            
            for conf in confirmations:
                try:
                    conf_time = datetime.fromisoformat(conf['timestamp'])
                    if conf_time > cutoff_time:
                        active.append(conf)
                except:
                    continue
            
            return active
            
        except Exception as e:
            logger.warning(f"Error getting active confirmations: {e}")
            return []
    
    def _determine_crowd_level(self, active_count: int) -> str:
        """Determine crowd level based on active confirmations"""
        if active_count == 0:
            return 'low'
        elif active_count <= 5:
            return 'medium'
        elif active_count <= 15:
            return 'high'
        else:
            return 'very_high'
    
    def _calculate_crowd_metrics(self, train_number: str) -> Dict[str, Any]:
        """Calculate various crowd metrics"""
        try:
            crowd_data = self.get_train_crowd_data(train_number)
            
            # Calculate confidence level based on number of confirmations
            active_count = crowd_data['active_confirmations']
            if active_count == 0:
                confidence = 'none'
            elif active_count <= 3:
                confidence = 'low'
            elif active_count <= 10:
                confidence = 'medium'
            else:
                confidence = 'high'
            
            # Calculate average time since confirmations
            if crowd_data['confirmations']:
                timestamps = [datetime.fromisoformat(conf['timestamp']) for conf in crowd_data['confirmations']]
                avg_time_diff = sum([(datetime.now() - ts).total_seconds() for ts in timestamps]) / len(timestamps)
                avg_minutes_ago = int(avg_time_diff / 60)
            else:
                avg_minutes_ago = 0
            
            return {
                'crowd_level': crowd_data['crowd_level'],
                'confidence': confidence,
                'active_users': active_count,
                'average_time_since_confirmation': f"{avg_minutes_ago} minutes ago",
                'data_freshness': 'high' if avg_minutes_ago < 30 else 'medium' if avg_minutes_ago < 60 else 'low'
            }
            
        except Exception as e:
            logger.error(f"Error calculating crowd metrics: {e}")
            return {
                'crowd_level': 'unknown',
                'confidence': 'none',
                'active_users': 0,
                'average_time_since_confirmation': 'unknown',
                'data_freshness': 'unknown'
            }
    
    def adjust_train_status_with_crowd_data(self, train_number: str, 
                                          base_status: Dict[str, Any]) -> Dict[str, Any]:
        """Adjust train status based on crowd validation data"""
        try:
            crowd_data = self.get_train_crowd_data(train_number)
            
            if 'error' in crowd_data:
                return base_status
            
            # Adjust delay based on crowd data
            adjusted_status = base_status.copy()
            
            if crowd_data['confidence'] in ['medium', 'high']:
                # Use crowd data to refine status
                crowd_delay_adjustment = self._calculate_crowd_delay_adjustment(crowd_data)
                
                if 'delay_minutes' in adjusted_status:
                    adjusted_status['delay_minutes'] = max(0, 
                        adjusted_status['delay_minutes'] + crowd_delay_adjustment)
                
                # Add crowd validation info
                adjusted_status['crowd_validation'] = {
                    'confidence': crowd_data['confidence'],
                    'active_users': crowd_data['active_confirmations'],
                    'crowd_level': crowd_data['crowd_level'],
                    'last_updated': crowd_data['last_updated']
                }
                
                # Adjust ETA if we have high confidence crowd data
                if crowd_data['confidence'] == 'high' and crowd_data['active_confirmations'] > 5:
                    adjusted_status['eta_adjusted_by_crowd'] = True
                    adjusted_status['crowd_eta_confidence'] = 'high'
            
            return adjusted_status
            
        except Exception as e:
            logger.error(f"Error adjusting train status with crowd data: {e}")
            return base_status
    
    def _calculate_crowd_delay_adjustment(self, crowd_data: Dict[str, Any]) -> int:
        """Calculate delay adjustment based on crowd data"""
        try:
            # Simple heuristic: more users = more accurate delay
            active_users = crowd_data['active_confirmations']
            crowd_level = crowd_data['crowd_level']
            
            # Base adjustment
            if crowd_level == 'low':
                adjustment = 0
            elif crowd_level == 'medium':
                adjustment = random.randint(-2, 2)  # Small adjustment
            elif crowd_level == 'high':
                adjustment = random.randint(-5, 5)  # Medium adjustment
            else:  # very_high
                adjustment = random.randint(-8, 8)  # Larger adjustment
            
            # Scale by number of users
            if active_users > 10:
                adjustment = int(adjustment * 1.5)
            elif active_users > 20:
                adjustment = int(adjustment * 2.0)
            
            return adjustment
            
        except Exception as e:
            logger.warning(f"Error calculating crowd delay adjustment: {e}")
            return 0
    
    def get_all_train_validations(self) -> Dict[str, Any]:
        """Get validation data for all trains"""
        try:
            summary = {}
            for train_number, data in self.validations.items():
                crowd_data = self.get_train_crowd_data(train_number)
                summary[train_number] = {
                    'total_confirmations': data['total_confirmations'],
                    'active_confirmations': crowd_data['active_confirmations'],
                    'crowd_level': crowd_data['crowd_level'],
                    'last_updated': data['last_updated']
                }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting all train validations: {e}")
            return {}
    
    def cleanup_old_validations(self, max_age_hours: int = 24):
        """Clean up old validations to prevent data bloat"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
            cleaned_count = 0
            
            for train_number in list(self.validations.keys()):
                train_data = self.validations[train_number]
                
                # Remove old confirmations
                old_confirmations = []
                for conf in train_data['confirmations']:
                    try:
                        conf_time = datetime.fromisoformat(conf['timestamp'])
                        if conf_time > cutoff_time:
                            old_confirmations.append(conf)
                    except:
                        continue
                
                # Update train data
                self.validations[train_number]['confirmations'] = old_confirmations
                self.validations[train_number]['total_confirmations'] = len(old_confirmations)
                
                # Remove train if no confirmations left
                if len(old_confirmations) == 0:
                    del self.validations[train_number]
                    cleaned_count += 1
            
            if cleaned_count > 0:
                self._save_validations()
                logger.info(f"Cleaned up {cleaned_count} trains with old validations")
            
            return cleaned_count
            
        except Exception as e:
            logger.error(f"Error cleaning up old validations: {e}")
            return 0

def get_crowd_validation() -> CrowdValidation:
    """Get crowd validation instance"""
    return CrowdValidation()
