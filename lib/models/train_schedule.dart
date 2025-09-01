class TrainSchedule {
  final String trainName;
  final String trainModel;
  final List<String> days;
  final List<StationRoute> routes;
  final String totalDuration;

  TrainSchedule({
    required this.trainName,
    required this.trainModel,
    required this.days,
    required this.routes,
    required this.totalDuration,
  });

  factory TrainSchedule.fromJson(Map<String, dynamic> json) {
    return TrainSchedule(
      trainName: json['data']['train_name'] ?? '',
      trainModel: json['data']['train_model'] ?? '',
      days: List<String>.from(json['data']['days'] ?? []),
      routes: (json['data']['routes'] as List?)
          ?.map((route) => StationRoute.fromJson(route))
          .toList() ?? [],
      totalDuration: json['data']['total_duration'] ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'data': {
        'train_name': trainName,
        'train_model': trainModel,
        'days': days,
        'routes': routes.map((route) => route.toJson()).toList(),
        'total_duration': totalDuration,
      }
    };
  }
}

class StationRoute {
  final String city;
  final String? arrivalTime;
  final String? departureTime;
  final String? halt;
  final String? duration;

  StationRoute({
    required this.city,
    this.arrivalTime,
    this.departureTime,
    this.halt,
    this.duration,
  });

  factory StationRoute.fromJson(Map<String, dynamic> json) {
    return StationRoute(
      city: json['city'] ?? '',
      arrivalTime: json['arrival_time'],
      departureTime: json['departure_time'],
      halt: json['halt'],
      duration: json['duration'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'city': city,
      'arrival_time': arrivalTime,
      'departure_time': departureTime,
      'halt': halt,
      'duration': duration,
    };
  }
}
