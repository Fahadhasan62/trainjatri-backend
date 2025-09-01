import 'package:flutter/material.dart';
import 'package:train_jatri/models/train_schedule.dart';
import 'package:train_jatri/screens/train_status_screen.dart';
import 'package:train_jatri/utils/theme.dart';

class TrainScheduleScreen extends StatelessWidget {
  final List<TrainSchedule> trains;
  final String fromStation;
  final String toStation;

  const TrainScheduleScreen({
    super.key,
    required this.trains,
    required this.fromStation,
    required this.toStation,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('$fromStation → $toStation'),
        elevation: 0,
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16),
        itemCount: trains.length,
        itemBuilder: (context, index) {
          final train = trains[index];
          return _buildTrainCard(context, train);
        },
      ),
    );
  }

  Widget _buildTrainCard(BuildContext context, TrainSchedule train) {
    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      elevation: 4,
      child: Column(
        children: [
          // Train Header
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: AppTheme.primaryColor.withOpacity(0.1),
              borderRadius: const BorderRadius.only(
                topLeft: Radius.circular(12),
                topRight: Radius.circular(12),
              ),
            ),
            child: Row(
              children: [
                Container(
                  width: 50,
                  height: 50,
                  decoration: BoxDecoration(
                    color: AppTheme.primaryColor,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: const Icon(
                    Icons.train,
                    color: Colors.white,
                    size: 24,
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        train.trainName,
                        style: const TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      Text(
                        'Train No: ${train.trainModel}',
                        style: TextStyle(
                          fontSize: 14,
                          color: Colors.grey[600],
                        ),
                      ),
                    ],
                  ),
                ),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.end,
                  children: [
                    Text(
                      'Duration',
                      style: TextStyle(
                        fontSize: 12,
                        color: Colors.grey[600],
                      ),
                    ),
                    Text(
                      train.totalDuration,
                      style: const TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                        color: AppTheme.primaryColor,
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),

          // Route Details
          Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
                // From Station
                _buildStationRow(
                  train.routes.first,
                  isFirst: true,
                  isLast: false,
                ),
                
                // Route Line
                Container(
                  margin: const EdgeInsets.symmetric(horizontal: 20),
                  height: 40,
                  child: CustomPaint(
                    painter: RouteLinePainter(),
                  ),
                ),

                // To Station
                _buildStationRow(
                  train.routes.last,
                  isFirst: false,
                  isLast: true,
                ),

                const SizedBox(height: 20),

                // Operating Days
                Row(
                  children: [
                    Icon(
                      Icons.calendar_today,
                      size: 16,
                      color: Colors.grey[600],
                    ),
                    const SizedBox(width: 8),
                    Text(
                      'Operating Days:',
                      style: TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.w600,
                        color: Colors.grey[700],
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                Wrap(
                  spacing: 8,
                  children: train.days.map((day) {
                    return Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 12,
                        vertical: 6,
                      ),
                      decoration: BoxDecoration(
                        color: AppTheme.primaryColor.withOpacity(0.1),
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(
                          color: AppTheme.primaryColor.withOpacity(0.3),
                        ),
                      ),
                      child: Text(
                        day,
                        style: TextStyle(
                          fontSize: 12,
                          fontWeight: FontWeight.w600,
                          color: AppTheme.primaryColor,
                        ),
                      ),
                    );
                  }).toList(),
                ),

                const SizedBox(height: 20),

                // Action Buttons
                Row(
                  children: [
                    Expanded(
                      child: OutlinedButton.icon(
                        onPressed: () {
                          // Add to favorites
                          ScaffoldMessenger.of(context).showSnackBar(
                            const SnackBar(
                              content: Text('Added to favorites'),
                            ),
                          );
                        },
                        icon: const Icon(Icons.favorite_border),
                        label: const Text('Favorite'),
                        style: OutlinedButton.styleFrom(
                          padding: const EdgeInsets.symmetric(vertical: 12),
                        ),
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: ElevatedButton.icon(
                        onPressed: () {
                          _showUserConfirmationDialog(context, train);
                        },
                        icon: const Icon(Icons.timeline),
                        label: const Text('Live Status'),
                        style: ElevatedButton.styleFrom(
                          padding: const EdgeInsets.symmetric(vertical: 12),
                        ),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStationRow(StationRoute route, {required bool isFirst, required bool isLast}) {
    return Row(
      children: [
        Container(
          width: 40,
          height: 40,
          decoration: BoxDecoration(
            color: isFirst || isLast 
                ? AppTheme.primaryColor 
                : Colors.grey[300],
            shape: BoxShape.circle,
          ),
          child: Icon(
            isFirst ? Icons.location_on_outlined : Icons.location_on,
            color: isFirst || isLast ? Colors.white : Colors.grey[600],
            size: 20,
          ),
        ),
        const SizedBox(width: 16),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                route.city,
                style: TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w600,
                  color: isFirst || isLast ? AppTheme.primaryColor : Colors.grey[800],
                ),
              ),
              if (isFirst && route.departureTime != null)
                Text(
                  'Departure: ${route.departureTime}',
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.grey[600],
                  ),
                ),
              if (isLast && route.arrivalTime != null)
                Text(
                  'Arrival: ${route.arrivalTime}',
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.grey[600],
                  ),
                ),
            ],
          ),
        ),
        if (route.halt != null && !isFirst && !isLast)
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
            decoration: BoxDecoration(
              color: AppTheme.warningColor.withOpacity(0.1),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Text(
              'Halt: ${route.halt}min',
              style: TextStyle(
                fontSize: 12,
                color: AppTheme.warningColor,
                fontWeight: FontWeight.w600,
              ),
            ),
          ),
      ],
    );
  }

  void _showUserConfirmationDialog(BuildContext context, TrainSchedule train) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Confirm Location'),
        content: Text(
          'Are you currently inside the ${train.trainName}?',
        ),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
              // User denied - still allow viewing status
              _navigateToStatus(context, train);
            },
            child: const Text('No'),
          ),
          ElevatedButton(
            onPressed: () {
              Navigator.of(context).pop();
              // User confirmed - use for crowd validation
              _navigateToStatus(context, train, userConfirmed: true);
            },
            child: const Text('Yes'),
          ),
        ],
      ),
    );
  }

  void _navigateToStatus(BuildContext context, TrainSchedule train, {bool userConfirmed = false}) {
    if (userConfirmed) {
      // TODO: Send confirmation to backend for crowd validation
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Thank you! Your location will help improve tracking accuracy.'),
        ),
      );
    }

    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => TrainStatusScreen(
          trainNumber: train.trainModel,
          trainName: train.trainName,
        ),
      ),
    );
  }
}

class RouteLinePainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.grey[400]!
      ..strokeWidth = 2
      ..style = PaintingStyle.stroke;

    final path = Path();
    path.moveTo(size.width / 2, 0);
    path.lineTo(size.width / 2, size.height);

    canvas.drawPath(path, paint);

    // Draw dots along the line
    final dotPaint = Paint()
      ..color = Colors.grey[400]!
      ..style = PaintingStyle.fill;

    for (int i = 0; i < 3; i++) {
      final y = (size.height / 4) * (i + 1);
      canvas.drawCircle(Offset(size.width / 2, y), 3, dotPaint);
    }
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => false;
}
