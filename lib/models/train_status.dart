enum StationStatus { completed, current, next, upcoming }

class TrainStatus {
  final String trainNumber;
  final String trainName;
  final List<StationStatusInfo> stationStatuses;
  final double currentSpeed;
  final double distanceCovered;
  final double distanceToNext;
  final int delayMinutes;
  final DateTime estimatedArrival;

  TrainStatus({
    required this.trainNumber,
    required this.trainName,
    required this.stationStatuses,
    required this.currentSpeed,
    required this.distanceCovered,
    required this.distanceToNext,
    required this.delayMinutes,
    required this.estimatedArrival,
  });

  factory TrainStatus.fromJson(Map<String, dynamic> json) {
    return TrainStatus(
      trainNumber: json['train_number'] ?? '',
      trainName: json['train_name'] ?? '',
      stationStatuses: (json['station_statuses'] as List?)
          ?.map((status) => StationStatusInfo.fromJson(status))
          .toList() ?? [],
      currentSpeed: (json['current_speed'] ?? 0).toDouble(),
      distanceCovered: (json['distance_covered'] ?? 0).toDouble(),
      distanceToNext: (json['distance_to_next'] ?? 0).toDouble(),
      delayMinutes: json['delay_minutes'] ?? 0,
      estimatedArrival: DateTime.parse(json['estimated_arrival'] ?? DateTime.now().toIso8601String()),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'train_number': trainNumber,
      'train_name': trainName,
      'station_statuses': stationStatuses.map((status) => status.toJson()).toList(),
      'current_speed': currentSpeed,
      'distance_covered': distanceCovered,
      'distance_to_next': distanceToNext,
      'delay_minutes': delayMinutes,
      'estimated_arrival': estimatedArrival.toIso8601String(),
    };
  }
}

class StationStatusInfo {
  final String stationName;
  final StationStatus status;
  final DateTime scheduledTime;
  final DateTime? actualTime;
  final int delayMinutes;
  final String haltDuration;
  final double distanceFromStart;

  StationStatusInfo({
    required this.stationName,
    required this.status,
    required this.scheduledTime,
    this.actualTime,
    required this.delayMinutes,
    required this.haltDuration,
    required this.distanceFromStart,
  });

  factory StationStatusInfo.fromJson(Map<String, dynamic> json) {
    return StationStatusInfo(
      stationName: json['station_name'] ?? '',
      status: StationStatus.values.firstWhere(
        (e) => e.toString() == 'StationStatus.${json['status']}',
        orElse: () => StationStatus.upcoming,
      ),
      scheduledTime: DateTime.parse(json['scheduled_time']),
      actualTime: json['actual_time'] != null ? DateTime.parse(json['actual_time']) : null,
      delayMinutes: json['delay_minutes'] ?? 0,
      haltDuration: json['halt_duration'] ?? '',
      distanceFromStart: (json['distance_from_start'] ?? 0).toDouble(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'station_name': stationName,
      'status': status.toString().split('.').last,
      'scheduled_time': scheduledTime.toIso8601String(),
      'actual_time': actualTime?.toIso8601String(),
      'delay_minutes': delayMinutes,
      'halt_duration': haltDuration,
      'distance_from_start': distanceFromStart,
    };
  }
}
