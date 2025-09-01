#!/usr/bin/env python3
"""
TrainJatri Backend API - Complete Backend System
Provides comprehensive train tracking, scheduling, and crowd validation services
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import logging
from datetime import datetime, timedelta
import traceback

# Import our custom modules
from data_loader import get_data_loader
from position_calculator import get_position_calculator
from delay_simulator import get_delay_simulator
from train_timeline_generator import get_train_timeline_generator
from crowd_validation import get_crowd_validation

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize backend modules
data_loader = get_data_loader()
position_calculator = get_position_calculator(data_loader)
delay_simulator = get_delay_simulator()
timeline_generator = get_train_timeline_generator()
crowd_validation = get_crowd_validation()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint with system status"""
    try:
        # Load data status
        data_status = data_loader.load_all_data()
        
        # Get crowd validation summary
        crowd_summary = crowd_validation.get_all_train_validations()
        
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0",
            "data_sources": data_status,
            "crowd_validations": {
                "total_trains": len(crowd_summary),
                "active_validations": sum(data.get('active_confirmations', 0) for data in crowd_summary.values())
            },
            "modules": {
                "data_loader": "active",
                "position_calculator": "active",
                "delay_simulator": "active",
                "timeline_generator": "active",
                "crowd_validation": "active"
            }
        })
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@app.route('/api/stations', methods=['GET'])
def get_stations():
    """Get all stations with coordinates"""
    try:
        stations = data_loader.get_stations()
        return jsonify({
            "success": True,
            "stations": stations,
            "total_count": len(stations),
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error getting stations: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/trains/search', methods=['GET'])
def search_trains():
    """Search trains by station or train number"""
    try:
        from_station = request.args.get('from')
        to_station = request.args.get('to')
        train_number = request.args.get('number')
        
        if train_number:
            # Search by train number
            results = data_loader.search_trains_by_number(train_number)
            if results:
                return jsonify({
                    "success": True,
                    "search_type": "train_number",
                    "query": train_number,
                    "results": [result['schedule'] for result in results],
                    "total_count": len(results),
                    "timestamp": datetime.now().isoformat()
                })
            else:
                return jsonify({
                    "success": True,
                    "search_type": "train_number",
                    "query": train_number,
                    "results": [],
                    "total_count": 0,
                    "message": "No trains found with the specified number"
                })
        
        elif from_station and to_station:
            # Search by stations
            results = data_loader.search_trains_by_stations(from_station, to_station)
            if results:
                return jsonify({
                    "success": True,
                    "search_type": "station_to_station",
                    "from_station": from_station,
                    "to_station": to_station,
                    "results": [result['schedule'] for result in results],
                    "total_count": len(results),
                    "timestamp": datetime.now().isoformat()
                })
            else:
                return jsonify({
                    "success": True,
                    "search_type": "station_to_station",
                    "from_station": from_station,
                    "to_station": to_station,
                    "results": [],
                    "total_count": 0,
                    "message": f"No trains found between {from_station} and {to_station}"
                })
        
        else:
            return jsonify({
                "success": False,
                "error": "Invalid search parameters. Use 'from' and 'to' for station search or 'number' for train search."
            }), 400
            
    except Exception as e:
        logger.error(f"Error searching trains: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/trains/<train_number>/status', methods=['GET'])
def get_train_status(train_number):
    """Get comprehensive live train status with timeline"""
    try:
        # Generate complete train status
        status_data = timeline_generator.generate_train_status(train_number)
        
        if 'error' in status_data:
            return jsonify({
                "success": False,
                "error": status_data['error']
            }), 404
        
        # Apply crowd validation adjustments
        adjusted_status = crowd_validation.adjust_train_status_with_crowd_data(
            train_number, status_data
        )
        
        return jsonify({
            "success": True,
            "train_number": train_number,
            "status": adjusted_status,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting train status for {train_number}: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/trains/<train_number>/confirm', methods=['POST'])
def confirm_user_on_train(train_number):
    """Confirm user is on the train for crowd validation"""
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        station_name = data.get('station_name')
        coordinates = data.get('coordinates')
        
        if not user_id:
            return jsonify({
                "success": False,
                "error": "User ID is required"
            }), 400
        
        # Confirm user on train
        result = crowd_validation.confirm_user_on_train(
            train_number, user_id, station_name, coordinates
        )
        
        if result['success']:
            return jsonify({
                "success": True,
                "message": result['message'],
                "train_number": train_number,
                "user_id": user_id,
                "timestamp": result['timestamp'],
                "crowd_metrics": result['crowd_metrics']
            })
        else:
            return jsonify({
                "success": False,
                "error": result['error']
            }), 400
            
    except Exception as e:
        logger.error(f"Error confirming user on train {train_number}: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/trains/<train_number>/crowd-data', methods=['GET'])
def get_train_crowd_data(train_number):
    """Get crowd validation data for a specific train"""
    try:
        crowd_data = crowd_validation.get_train_crowd_data(train_number)
        
        if 'error' in crowd_data:
            return jsonify({
                "success": False,
                "error": crowd_data['error']
            }), 404
        
        return jsonify({
            "success": True,
            "train_number": train_number,
            "crowd_data": crowd_data,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting crowd data for train {train_number}: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/trains/<train_number>/summary', methods=['GET'])
def get_train_summary(train_number):
    """Get a summary of train information"""
    try:
        schedule = data_loader.get_schedule_by_train(train_number)
        if not schedule:
            return jsonify({
                "success": False,
                "error": "Train schedule not found"
            }), 404
        
        routes = schedule.get('data', {}).get('routes', [])
        
        # Calculate total distance
        total_distance = 0.0
        if len(routes) > 1:
            for i in range(len(routes) - 1):
                distance = position_calculator.calculate_distance_between_stations(
                    routes[i]['city'], routes[i + 1]['city']
                )
                total_distance += distance
        
        summary = {
            'train_number': train_number,
            'train_name': schedule.get('data', {}).get('train_name', 'Unknown'),
            'operating_days': schedule.get('data', {}).get('days', []),
            'total_stations': len(routes),
            'route_summary': {
                'origin': routes[0]['city'] if routes else 'Unknown',
                'destination': routes[-1]['city'] if routes else 'Unknown',
                'total_distance': round(total_distance, 2)
            },
            'schedule_info': {
                'departure_time': routes[0].get('departure_time') if routes else None,
                'arrival_time': routes[-1].get('arrival_time') if routes else None
            },
            'crowd_data': crowd_validation.get_train_crowd_data(train_number)
        }
        
        return jsonify({
            "success": True,
            "train_number": train_number,
            "summary": summary,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting train summary for {train_number}: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/stations/<station_name>/trains', methods=['GET'])
def get_trains_at_station(station_name):
    """Get all trains that pass through a specific station"""
    try:
        schedules = data_loader.get_schedules()
        trains_at_station = []
        
        for train_key, schedule in schedules.items():
            routes = schedule.get('data', {}).get('routes', [])
            route_stations = [route['city'] for route in routes]
            
            if station_name in route_stations:
                station_idx = route_stations.index(station_name)
                station_info = routes[station_idx]
                
                train_info = {
                    'train_number': train_key,
                    'train_name': schedule.get('data', {}).get('train_name', 'Unknown'),
                    'arrival_time': station_info.get('arrival_time'),
                    'departure_time': station_info.get('departure_time'),
                    'halt_duration': station_info.get('halt', '---'),
                    'operating_days': schedule.get('data', {}).get('days', [])
                }
                trains_at_station.append(train_info)
        
        return jsonify({
            "success": True,
            "station_name": station_name,
            "trains": trains_at_station,
            "total_count": len(trains_at_station),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error getting trains at station {station_name}: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/analytics/delays', methods=['GET'])
def get_delay_analytics():
    """Get delay analytics across all trains"""
    try:
        train_number = request.args.get('train')
        station_name = request.args.get('station')
        
        if train_number and station_name:
            # Get delay stats for specific train and station
            stats = delay_simulator.get_historical_delay_stats(train_number, station_name)
            return jsonify({
                "success": True,
                "analytics_type": "train_station_delays",
                "train_number": train_number,
                "station_name": station_name,
                "stats": stats,
                "timestamp": datetime.now().isoformat()
            })
        elif train_number:
            # Get delay stats for specific train
            stats = delay_simulator.get_historical_delay_stats(train_number)
            return jsonify({
                "success": True,
                "analytics_type": "train_delays",
                "train_number": train_number,
                "stats": stats,
                "timestamp": datetime.now().isoformat()
            })
        else:
            # Get overall delay analytics
            all_trains = data_loader.get_all_train_numbers()
            overall_stats = {
                'total_trains': len(all_trains),
                'trains_with_delays': 0,
                'average_delay': 0
            }
            
            return jsonify({
                "success": True,
                "analytics_type": "overall_delays",
                "stats": overall_stats,
                "timestamp": datetime.now().isoformat()
            })
            
    except Exception as e:
        logger.error(f"Error getting delay analytics: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/admin/refresh-data', methods=['POST'])
def refresh_data():
    """Admin endpoint to refresh all data"""
    try:
        # Refresh data loader
        data_status = data_loader.load_all_data(force_reload=True)
        
        # Clean up old crowd validations
        cleaned_count = crowd_validation.cleanup_old_validations()
        
        return jsonify({
            "success": True,
            "message": "Data refreshed successfully",
            "data_status": data_status,
            "cleaned_validations": cleaned_count,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error refreshing data: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/admin/system-status', methods=['GET'])
def get_system_status():
    """Get comprehensive system status"""
    try:
        # Get data status
        data_status = data_loader.load_all_data()
        
        # Get crowd validation summary
        crowd_summary = crowd_validation.get_all_train_validations()
        
        # Calculate system metrics
        total_schedules = len(data_loader.get_schedules())
        total_stations = len(data_loader.get_stations())
        total_segments = len(data_loader.get_segments())
        
        system_status = {
            "data_sources": {
                "schedules": total_schedules,
                "stations": total_stations,
                "segments": total_segments,
                "route_mappings": len(data_loader.get_route_mappings())
            },
            "crowd_validations": {
                "total_trains": len(crowd_summary),
                "total_confirmations": sum(data.get('total_confirmations', 0) for data in crowd_summary.values()),
                "active_confirmations": sum(data.get('active_confirmations', 0) for data in crowd_summary.values())
            },
            "system_health": {
                "data_loader": "healthy" if data_status.get('schedules_count', 0) > 0 else "unhealthy",
                "position_calculator": "healthy",
                "delay_simulator": "healthy",
                "timeline_generator": "healthy",
                "crowd_validation": "healthy"
            },
            "last_updated": datetime.now().isoformat()
        }
        
        return jsonify({
            "success": True,
            "system_status": system_status
        })
        
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint not found",
        "timestamp": datetime.now().isoformat()
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        "success": False,
        "error": "Internal server error",
        "timestamp": datetime.now().isoformat()
    }), 500

@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Unhandled exception: {e}")
    logger.error(traceback.format_exc())
    return jsonify({
        "success": False,
        "error": "An unexpected error occurred",
        "timestamp": datetime.now().isoformat()
    }), 500

if __name__ == '__main__':
    logger.info("Starting TrainJatri Backend API...")
    logger.info("Loading initial data...")
    
    # Load initial data
    try:
        data_status = data_loader.load_all_data()
        logger.info(f"Data loaded successfully: {data_status}")
    except Exception as e:
        logger.error(f"Error loading initial data: {e}")
    
    # Start the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
