class Station {
  final String name;
  final double longitude;
  final double latitude;

  Station({
    required this.name,
    required this.longitude,
    required this.latitude,
  });

  factory Station.fromJson(MapEntry<String, dynamic> entry) {
    final coordinates = entry.value as List;
    return Station(
      name: entry.key,
      longitude: coordinates[0].toDouble(),
      latitude: coordinates[1].toDouble(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'name': name,
      'longitude': longitude,
      'latitude': latitude,
    };
  }

  double distanceTo(Station other) {
    const double earthRadius = 6371; // Earth's radius in kilometers
    final double lat1Rad = latitude * (3.14159265359 / 180);
    final double lat2Rad = other.latitude * (3.14159265359 / 180);
    final double deltaLat = (other.latitude - latitude) * (3.14159265359 / 180);
    final double deltaLon = (other.longitude - longitude) * (3.14159265359 / 180);

    final double a = (deltaLat / 2).sin() * (deltaLat / 2).sin() +
        lat1Rad.cos() * lat2Rad.cos() * (deltaLon / 2).sin() * (deltaLon / 2).sin();
    final double c = 2 * (a.sqrt().asin());

    return earthRadius * c;
  }
}
