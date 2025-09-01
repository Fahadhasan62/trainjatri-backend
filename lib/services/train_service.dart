import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:train_jatri/models/train_schedule.dart';
import 'package:train_jatri/models/train_status.dart';
import 'package:train_jatri/models/station.dart';

class TrainService {
  // Update this to your local Flask API URL
  static const String baseUrl = 'http://localhost:5000/api';
  
  static Future<List<TrainSchedule>> searchTrainsByStations(String fromStation, String toStation) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/trains/search?from=$fromStation&to=$toStation'),
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((json) => TrainSchedule.fromJson(json)).toList();
      } else {
        throw Exception('Failed to search trains: ${response.statusCode}');
      }
    } catch (e) {
      // Fallback to mock data if API fails
      return _getMockTrainsByStations(fromStation, toStation);
    }
  }

  static Future<List<TrainSchedule>> searchTrainsByNumber(String trainNumber) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/trains/search?number=$trainNumber'),
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((json) => TrainSchedule.fromJson(json)).toList();
      } else {
        throw Exception('Failed to search trains: ${response.statusCode}');
      }
    } catch (e) {
      // Fallback to mock data if API fails
      return _getMockTrainsByNumber(trainNumber);
    }
  }

  static Future<TrainStatus?> getTrainStatus(String trainNumber) async {
    try {
      final response = await http.get(
        Uri.parse('$baseUrl/trains/$trainNumber/status'),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        return TrainStatus.fromJson(data);
      } else {
        throw Exception('Failed to get train status: ${response.statusCode}');
      }
    } catch (e) {
      // Fallback to mock data if API fails
      return _getMockTrainStatus(trainNumber);
    }
  }

  static Future<List<Station>> getAllStations() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/stations'));

      if (response.statusCode == 200) {
        final Map<String, dynamic> data = json.decode(response.body);
        return data.entries.map((entry) => Station.fromJson(entry)).toList();
      } else {
        throw Exception('Failed to get stations: ${response.statusCode}');
      }
    } catch (e) {
      // Fallback to mock data if API fails
      return _getMockStations();
    }
  }

  static Future<void> confirmUserOnTrain(String trainNumber, String userId) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/trains/$trainNumber/confirm'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'user_id': userId}),
      );

      if (response.statusCode != 200) {
        throw Exception('Failed to confirm location: ${response.statusCode}');
      }
    } catch (e) {
      // Handle error silently for now
      print('Error confirming location: $e');
    }
  }

  // Mock data fallbacks
  static List<TrainSchedule> _getMockTrainsByStations(String fromStation, String toStation) {
    return [
      TrainSchedule(
        trainName: 'AGHNIBINA EXPRESS (735)',
        trainModel: '735',
        days: ['Fri', 'Sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu'],
        routes: [
          StationRoute(
            city: fromStation,
            departureTime: '11:30 am BST',
            halt: null,
            duration: null,
          ),
          StationRoute(
            city: toStation,
            arrivalTime: '05:00 pm BST',
            halt: null,
            duration: '05:30',
          ),
        ],
        totalDuration: '05:30',
      ),
    ];
  }

  static List<TrainSchedule> _getMockTrainsByNumber(String trainNumber) {
    return [
      TrainSchedule(
        trainName: 'AGHNIBINA EXPRESS (735)',
        trainModel: '735',
        days: ['Fri', 'Sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu'],
        routes: [
          StationRoute(
            city: 'Dhaka',
            departureTime: '11:30 am BST',
            halt: null,
            duration: null,
          ),
          StationRoute(
            city: 'Biman_Bandar',
            arrivalTime: '11:53 am BST',
            departureTime: '11:58 am BST',
            halt: '05',
            duration: '00:23',
          ),
          StationRoute(
            city: 'Gafargaon',
            arrivalTime: '01:45 pm BST',
            departureTime: '01:47 pm BST',
            halt: '02',
            duration: '01:47',
          ),
          StationRoute(
            city: 'Mymensingh',
            arrivalTime: '02:35 pm BST',
            departureTime: '02:38 pm BST',
            halt: '03',
            duration: '00:48',
          ),
          StationRoute(
            city: 'Narundi',
            arrivalTime: '03:16 pm BST',
            departureTime: '03:18 pm BST',
            halt: '02',
            duration: '00:38',
          ),
          StationRoute(
            city: 'Jamalpur_Town',
            arrivalTime: '03:38 pm BST',
            departureTime: '03:42 pm BST',
            halt: '04',
            duration: '00:20',
          ),
          StationRoute(
            city: 'Kendua_Bazar',
            arrivalTime: '04:00 pm BST',
            departureTime: '04:02 pm BST',
            halt: '02',
            duration: '00:18',
          ),
          StationRoute(
            city: 'Sarishabari',
            arrivalTime: '04:33 pm BST',
            departureTime: '04:35 pm BST',
            halt: '02',
            duration: '00:31',
          ),
          StationRoute(
            city: 'Tarakandi',
            arrivalTime: '05:00 pm BST',
            halt: null,
            duration: '00:25',
          ),
        ],
        totalDuration: '05:30',
      ),
    ];
  }

  static TrainStatus _getMockTrainStatus(String trainNumber) {
    final now = DateTime.now();
    return TrainStatus(
      trainNumber: trainNumber,
      trainName: 'AGHNIBINA EXPRESS (735)',
      stationStatuses: [
        StationStatusInfo(
          stationName: 'Dhaka',
          status: StationStatus.completed,
          scheduledTime: now.subtract(const Duration(hours: 2)),
          actualTime: now.subtract(const Duration(hours: 2, minutes: 5)),
          delayMinutes: 5,
          haltDuration: '',
          distanceFromStart: 0,
        ),
        StationStatusInfo(
          stationName: 'Biman_Bandar',
          status: StationStatus.completed,
          scheduledTime: now.subtract(const Duration(hours: 1, minutes: 37)),
          actualTime: now.subtract(const Duration(hours: 1, minutes: 42)),
          delayMinutes: 5,
          haltDuration: '05',
          distanceFromStart: 15.2,
        ),
        StationStatusInfo(
          stationName: 'Gafargaon',
          status: StationStatus.current,
          scheduledTime: now.add(const Duration(minutes: 15)),
          actualTime: null,
          delayMinutes: 5,
          haltDuration: '02',
          distanceFromStart: 45.8,
        ),
        StationStatusInfo(
          stationName: 'Mymensingh',
          status: StationStatus.next,
          scheduledTime: now.add(const Duration(minutes: 45)),
          actualTime: null,
          delayMinutes: 5,
          haltDuration: '03',
          distanceFromStart: 65.3,
        ),
        StationStatusInfo(
          stationName: 'Narundi',
          status: StationStatus.upcoming,
          scheduledTime: now.add(const Duration(hours: 1, minutes: 16)),
          actualTime: null,
          delayMinutes: 5,
          haltDuration: '02',
          distanceFromStart: 78.9,
        ),
        StationStatusInfo(
          stationName: 'Jamalpur_Town',
          status: StationStatus.upcoming,
          scheduledTime: now.add(const Duration(hours: 1, minutes: 38)),
          actualTime: null,
          delayMinutes: 5,
          haltDuration: '04',
          distanceFromStart: 92.1,
        ),
        StationStatusInfo(
          stationName: 'Kendua_Bazar',
          status: StationStatus.upcoming,
          scheduledTime: now.add(const Duration(hours: 2, minutes: 0)),
          actualTime: null,
          delayMinutes: 5,
          haltDuration: '02',
          distanceFromStart: 105.7,
        ),
        StationStatusInfo(
          stationName: 'Sarishabari',
          status: StationStatus.upcoming,
          scheduledTime: now.add(const Duration(hours: 2, minutes: 33)),
          actualTime: null,
          delayMinutes: 5,
          haltDuration: '02',
          distanceFromStart: 118.4,
        ),
        StationStatusInfo(
          stationName: 'Tarakandi',
          status: StationStatus.upcoming,
          scheduledTime: now.add(const Duration(hours: 3, minutes: 0)),
          actualTime: null,
          delayMinutes: 5,
          haltDuration: '',
          distanceFromStart: 130.2,
        ),
      ],
      currentSpeed: 65.0,
      distanceCovered: 45.8,
      distanceToNext: 19.5,
      delayMinutes: 5,
      estimatedArrival: now.add(const Duration(minutes: 45)),
    );
  }

  static List<Station> _getMockStations() {
    return [
      Station(name: 'Dhaka', longitude: 90.42605671358024, latitude: 23.73463380302861),
      Station(name: 'Biman_Bandar', longitude: 90.4080793, latitude: 23.8518522),
      Station(name: 'Gafargaon', longitude: 90.5478, latitude: 24.4537),
      Station(name: 'Mymensingh', longitude: 90.41012074414064, latitude: 24.75330502644484),
      Station(name: 'Narundi', longitude: 90.12, latitude: 24.865),
      Station(name: 'Jamalpur_Town', longitude: 89.9546, latitude: 24.9148),
      Station(name: 'Kendua_Bazar', longitude: 89.9067, latitude: 24.8568),
      Station(name: 'Sarishabari', longitude: 89.8398, latitude: 24.7611),
      Station(name: 'Tarakandi', longitude: 89.824246, latitude: 24.685172),
    ];
  }
}
