# TrainJatri Backend System

A comprehensive, production-ready backend system for Bangladesh Railway train tracking and scheduling.

## 🚀 Features

### Core Functionality
- **Live Train Tracking**: Real-time train position calculation and status updates
- **Intelligent Delay Simulation**: Weather, time-of-day, and station-specific delay factors
- **Crowd Validation**: User confirmations to improve tracking accuracy
- **Comprehensive Data Management**: Efficient loading and caching of all railway data
- **Position Calculation**: Accurate distance and ETA calculations using GPS coordinates

### Advanced Capabilities
- **Multi-factor Delay Analysis**: Historical patterns, weather conditions, rush hours
- **Route Optimization**: Efficient train route mapping and segment analysis
- **Real-time Metrics**: Speed estimation, progress tracking, crowd levels
- **Data Integrity**: Comprehensive validation and error handling

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Flask API     │    │  Data Loader     │    │  JSON Files     │
│   (Main App)    │◄──►│  (Data Manager)  │◄──►│  (Data Store)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│Position Calc.   │    │Delay Simulator   │    │Crowd Validation│
│(GPS & Distance) │    │(Realistic Delays)│    │(User Confirm.)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│Timeline Gen.    │    │Config Management │    │Health Monitoring│
│(Status Builder) │    │(Env & Settings)  │    │(System Status)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 📁 Project Structure

```
backend/
├── train_timeline_api.py      # Main Flask application
├── data_loader.py             # Data loading and caching
├── position_calculator.py     # GPS and distance calculations
├── delay_simulator.py         # Realistic delay simulation
├── train_timeline_generator.py # Timeline and status generation
├── crowd_validation.py        # User confirmation management
├── config.py                  # Configuration management
├── start_backend.py           # Comprehensive startup script
├── requirements.txt           # Python dependencies
├── BACKEND_README.md          # This file
└── data/                      # Data files directory
    ├── stations.json          # Station coordinates
    ├── Bangladesh_500m_segments.json  # Railway segments
    ├── schedules/             # Train schedules (132 files)
    └── crowd_validations.json # User confirmations
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- All required JSON data files

### Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify Data Files**
   ```bash
   python -c "from data_loader import get_data_loader; dl = get_data_loader(); print(dl.load_all_data())"
   ```

3. **Start Backend**
   ```bash
   python start_backend.py
   ```

4. **Verify Health**
   ```bash
   curl http://localhost:5000/api/health
   ```

### Advanced Setup

#### Environment Variables
```bash
export FLASK_ENV=production
export FLASK_DEBUG=false
export HOST=0.0.0.0
export PORT=5000
export DATA_DIR=/path/to/data
export CACHE_DURATION=600
export LOG_LEVEL=INFO
```

#### Configuration Classes
- **DevelopmentConfig**: Debug mode, verbose logging
- **ProductionConfig**: Optimized for production
- **TestingConfig**: Testing environment settings

## 🔌 API Endpoints

### Core Endpoints

#### Health Check
```http
GET /api/health
```
Returns system status, data sources, and module health.

#### Stations
```http
GET /api/stations
```
Returns all stations with coordinates.

#### Train Search
```http
GET /api/trains/search?from=Dhaka&to=Chattogram
GET /api/trains/search?number=UPAKUL_EXPRESS_712
```
Search trains by station pairs or train number.

#### Live Train Status
```http
GET /api/trains/{train_number}/status
```
Returns comprehensive live status with timeline.

#### User Confirmation
```http
POST /api/trains/{train_number}/confirm
{
  "user_id": "user123",
  "station_name": "Dhaka",
  "coordinates": {"lat": 23.7346, "lng": 90.4261}
}
```

### Analytics Endpoints

#### Crowd Data
```http
GET /api/trains/{train_number}/crowd-data
```

#### Delay Analytics
```http
GET /api/analytics/delays?train=UPAKUL_EXPRESS_712&station=Dhaka
```

#### System Status
```http
GET /api/admin/system-status
```

### Admin Endpoints

#### Data Refresh
```http
POST /api/admin/refresh-data
```

## 📊 Data Models

### Train Status Response
```json
{
  "success": true,
  "train_number": "UPAKUL_EXPRESS_712",
  "status": {
    "train_name": "UPAKUL EXPRESS",
    "station_statuses": [
      {
        "station_name": "Dhaka",
        "status": "completed",
        "scheduled_arrival": null,
        "scheduled_departure": "2024-01-15T15:10:00",
        "actual_departure": "2024-01-15T15:15:00",
        "delay_minutes": 5,
        "halt_duration": null,
        "distance_from_start": 0.0,
        "weather_condition": "clear",
        "crowd_level": "high"
      }
    ],
    "current_speed": 65.2,
    "distance_covered": 45.3,
    "distance_to_next": 18.7,
    "delay_minutes": 5,
    "estimated_arrival": "25m",
    "progress_percentage": 45.2,
    "current_station": "Bhairab_Bazar",
    "next_station": "Ashuganj",
    "weather_condition": "clear",
    "last_updated": "2024-01-15T16:30:00"
  }
}
```

### Station Status
```json
{
  "station_name": "Dhaka",
  "status": "completed|current|next|upcoming",
  "scheduled_arrival": "2024-01-15T15:10:00",
  "scheduled_departure": "2024-01-15T15:10:00",
  "actual_arrival": "2024-01-15T15:15:00",
  "actual_departure": "2024-01-15T15:15:00",
  "delay_minutes": 5,
  "halt_duration": "05",
  "distance_from_start": 0.0,
  "weather_condition": "clear|cloudy|rainy|stormy|foggy",
  "crowd_level": "low|normal|medium|high"
}
```

## 🔧 Configuration

### Data Settings
- **Cache Duration**: 5 minutes (configurable)
- **Data Directory**: Current directory (configurable)
- **Validation Timeout**: 2 hours for crowd confirmations

### Delay Simulation
- **Base Probability**: 30% chance of delay
- **Weather Factors**: Clear (1.0x) to Stormy (2.0x)
- **Time Factors**: Rush hours (1.6x) to Night (0.9x)
- **Station Factors**: Major hubs (1.5x) to Small stations (1.0x)

### Performance Settings
- **Rate Limiting**: 100 requests/minute (configurable)
- **Data Caching**: 5-minute cache with force refresh option
- **Error Handling**: Comprehensive error logging and recovery

## 📈 Performance & Monitoring

### Health Monitoring
- Real-time system status
- Data source validation
- Module health checks
- Performance metrics

### Data Management
- Efficient JSON loading
- Smart caching strategies
- Memory management
- Data integrity validation

### Error Handling
- Comprehensive logging
- Graceful degradation
- User-friendly error messages
- Recovery mechanisms

## 🧪 Testing

### Unit Tests
```bash
pytest tests/ -v --cov=.
```

### Integration Tests
```bash
python -m pytest tests/integration/ -v
```

### Load Testing
```bash
python tests/load_test.py
```

## 🚀 Deployment

### Development
```bash
python start_backend.py
```

### Production
```bash
export FLASK_ENV=production
gunicorn -w 4 -b 0.0.0.0:5000 train_timeline_api:app
```

### Docker
```dockerfile
FROM python:3.9-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "start_backend.py"]
```

## 🔍 Troubleshooting

### Common Issues

#### Data Loading Errors
```bash
# Check data file integrity
python -c "from data_loader import get_data_loader; dl = get_data_loader(); print(dl.load_all_data())"
```

#### Port Conflicts
```bash
# Check port usage
netstat -an | grep :5000
# Kill process using port
lsof -ti:5000 | xargs kill -9
```

#### Import Errors
```bash
# Verify module installation
python -c "import flask, flask_cors; print('Modules OK')"
```

### Debug Mode
```bash
export FLASK_DEBUG=true
export LOG_LEVEL=DEBUG
python start_backend.py
```

## 📚 API Documentation

### Request/Response Examples

#### Search Trains Between Stations
```bash
curl "http://localhost:5000/api/trains/search?from=Dhaka&to=Chattogram"
```

#### Get Live Train Status
```bash
curl "http://localhost:5000/api/trains/UPAKUL_EXPRESS_712/status"
```

#### Confirm User on Train
```bash
curl -X POST "http://localhost:5000/api/trains/UPAKUL_EXPRESS_712/confirm" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user123", "station_name": "Dhaka"}'
```

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Submit a pull request

### Code Standards
- Follow PEP 8 style guide
- Add comprehensive docstrings
- Include unit tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Documentation
- This README
- API endpoint documentation
- Code comments and docstrings

### Issues
- GitHub Issues for bug reports
- Feature requests welcome
- Performance optimization suggestions

### Contact
- Development team
- Railway authorities
- Community contributors

---

**TrainJatri Backend v2.0.0** - Comprehensive Railway Tracking System
