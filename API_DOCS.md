# TrainJatri Backend API Documentation

## Base URL

```
https://trainjatri-backend.onrender.com/api
```

This API provides endpoints for train schedules, live status, stations, crowd validation, analytics, and system administration.

## 🩺 Health Check

### Endpoint

```
GET /health
```

### Description

Check if the backend is running and healthy.

### Response Example

```json
{
  "status": "healthy",
  "timestamp": "2025-09-02T13:00:00",
  "version": "2.0.0",
  "data_sources": {
    "stations_count": 328,
    "segments_count": 1,
    "schedules_count": 132,
    "route_mappings_count": 1
  },
  "crowd_validations": {
    "total_trains": 12,
    "active_validations": 3
  },
  "modules": {
    "data_loader": "active",
    "position_calculator": "active",
    "delay_simulator": "active",
    "timeline_generator": "active",
    "crowd_validation": "active"
  }
}
```

## 🏙️ Stations

### Endpoint

```
GET /stations
```

### Description

Retrieve the list of all stations with coordinates.

### Response Example

```json
{
  "success": true,
  "stations": [
    { "id": "DHA", "name": "Dhaka", "lat": 23.777, "lon": 90.399 },
    { "id": "TGL", "name": "Tangail", "lat": 24.25, "lon": 89.91 }
  ],
  "total_count": 328,
  "timestamp": "2025-09-02T13:00:00"
}
```

## 🚆 Train Search

### By Number

```
GET /trains/search?number=735
```

### By Stations

```
GET /trains/search?from=Dhaka&to=Tarakandi
```

### Response Example

```json
{
  "success": true,
  "search_type": "station_to_station",
  "from_station": "Dhaka",
  "to_station": "Tarakandi",
  "results": [ { "train_number": "AGHNIBINA_EXPRESS_735", "train_name": "AGHNIBINA EXPRESS (735)" } ],
  "total_count": 1,
  "timestamp": "2025-09-02T13:00:00"
}
```

## 📍 Train Status (Live Timeline)

### Endpoint

```
GET /trains/<train_number>/status
```

### Example

```
GET /trains/AGHNIBINA_EXPRESS_735/status
```

### Description

Returns the live status and timeline of the given train.

## 📑 Train Summary

### Endpoint

```
GET /trains/<train_number>/summary
```

### Example Response

```json
{
  "success": true,
  "train_number": "AGHNIBINA_EXPRESS_735",
  "summary": {
    "train_name": "AGHNIBINA EXPRESS (735)",
    "operating_days": ["Fri","Sat","Sun","Mon","Tue","Wed","Thu"],
    "total_stations": 9,
    "route_summary": {
      "origin": "Dhaka",
      "destination": "Tarakandi",
      "total_distance": 196.32
    },
    "schedule_info": {
      "departure_time": "11:30 am BST",
      "arrival_time": "05:00 pm BST"
    },
    "crowd_data": {
      "train_number": "AGHNIBINA_EXPRESS_735",
      "total_confirmations": 1,
      "active_confirmations": 0,
      "crowd_level": "low"
    }
  },
  "timestamp": "2025-09-02T13:04:52"
}
```

## 👥 Crowd Validation

### Confirm User Onboard

```
POST /trains/<train_number>/confirm
```

### Body Example

```json
{
  "user_id": "user123",
  "station_name": "Tangail",
  "coordinates": [23.9, 90.2]
}
```

### Get Crowd Data

```
GET /trains/<train_number>/crowd-data
```

## 🚉 Trains at Station

### Endpoint

```
GET /stations/<station_name>/trains
```

### Example

```
GET /stations/Dhaka/trains
```

## 📊 Analytics: Delays

### Endpoint

```
GET /analytics/delays
```

### Optional Parameters

- `train=<train_number>`
- `station=<station_name>`

## 🔧 Admin Endpoints

⚠️ *To be protected later with API key or JWT.*

### Refresh data

```
POST /admin/refresh-data
```

### System status

```
GET /admin/system-status
```

## ❌ Error Handling

### 404 Not Found

```json
{
  "success": false,
  "error": "Endpoint not found",
  "timestamp": "2025-09-02T13:10:00"
}
```

### 500 Internal Server Error

```json
{
  "success": false,
  "error": "Internal server error",
  "timestamp": "2025-09-02T13:10:00"
}
```