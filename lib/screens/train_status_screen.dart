import 'package:flutter/material.dart';
import 'package:train_jatri/models/train_status.dart';
import 'package:train_jatri/services/train_service.dart';
import 'package:train_jatri/utils/theme.dart';
import 'package:intl/intl.dart';

class TrainStatusScreen extends StatefulWidget {
  final String trainNumber;
  final String trainName;

  const TrainStatusScreen({
    super.key,
    required this.trainNumber,
    required this.trainName,
  });

  @override
  State<TrainStatusScreen> createState() => _TrainStatusScreenState();
}

class _TrainStatusScreenState extends State<TrainStatusScreen> {
  TrainStatus? _trainStatus;
  bool _isLoading = true;
  bool _isRefreshing = false;

  @override
  void initState() {
    super.initState();
    _loadTrainStatus();
  }

  Future<void> _loadTrainStatus() async {
    setState(() {
      _isLoading = true;
    });

    try {
      final status = await TrainService.getTrainStatus(widget.trainNumber);
      setState(() {
        _trainStatus = status;
      });
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error loading train status: $e'),
          ),
        );
      }
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  Future<void> _refreshStatus() async {
    setState(() {
      _isRefreshing = true;
    });

    try {
      final status = await TrainService.getTrainStatus(widget.trainNumber);
      setState(() {
        _trainStatus = status;
      });
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error refreshing status: $e'),
          ),
        );
      }
    } finally {
      setState(() {
        _isRefreshing = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.trainName),
        elevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _isRefreshing ? null : _refreshStatus,
          ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _trainStatus == null
              ? _buildErrorState()
              : _buildStatusContent(),
    );
  }

  Widget _buildErrorState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(
            Icons.error_outline,
            size: 80,
            color: Colors.grey[400],
          ),
          const SizedBox(height: 16),
          const Text(
            'Unable to load train status',
            style: TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 8),
          const Text(
            'Please check your connection and try again',
            style: TextStyle(
              fontSize: 16,
              color: Colors.grey,
            ),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 24),
          ElevatedButton(
            onPressed: _loadTrainStatus,
            child: const Text('Retry'),
          ),
        ],
      ),
    );
  }

  Widget _buildStatusContent() {
    final status = _trainStatus!;
    return RefreshIndicator(
      onRefresh: _refreshStatus,
      child: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            // Top Banner - Train Info
            _buildTopBanner(status),
            const SizedBox(height: 24),

            // Timeline
            _buildTimeline(status),
            const SizedBox(height: 24),

            // Bottom Banner - Next Station Info
            _buildBottomBanner(status),
          ],
        ),
      ),
    );
  }

  Widget _buildTopBanner(TrainStatus status) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [
            AppTheme.primaryColor,
            AppTheme.secondaryColor,
          ],
        ),
        borderRadius: BorderRadius.circular(16),
      ),
      child: Column(
        children: [
          Row(
            children: [
              Container(
                width: 60,
                height: 60,
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.2),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: const Icon(
                  Icons.train,
                  color: Colors.white,
                  size: 30,
                ),
              ),
              const SizedBox(width: 20),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      status.trainName,
                      style: const TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                    Text(
                      'Train No: ${status.trainNumber}',
                      style: const TextStyle(
                        fontSize: 16,
                        color: Colors.white70,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 20),
          Row(
            children: [
              Expanded(
                child: _buildMetricCard(
                  'Speed',
                  '${status.currentSpeed.toStringAsFixed(1)} km/h',
                  Icons.speed,
                ),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: _buildMetricCard(
                  'Distance Covered',
                  '${status.distanceCovered.toStringAsFixed(1)} km',
                  Icons.route,
                ),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: _buildMetricCard(
                  'To Next Station',
                  '${status.distanceToNext.toStringAsFixed(1)} km',
                  Icons.location_on,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildMetricCard(String label, String value, IconData icon) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.2),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Column(
        children: [
          Icon(
            icon,
            color: Colors.white,
            size: 20,
          ),
          const SizedBox(height: 4),
          Text(
            value,
            style: const TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
            textAlign: TextAlign.center,
          ),
          Text(
            label,
            style: const TextStyle(
              fontSize: 10,
              color: Colors.white70,
            ),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }

  Widget _buildTimeline(TrainStatus status) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Journey Timeline',
            style: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold,
              color: Colors.grey[800],
            ),
          ),
          const SizedBox(height: 20),
          ...status.stationStatuses.asMap().entries.map((entry) {
            final index = entry.key;
            final station = entry.value;
            final isLast = index == status.stationStatuses.length - 1;
            
            return _buildTimelineItem(station, index, isLast);
          }).toList(),
        ],
      ),
    );
  }

  Widget _buildTimelineItem(StationStatusInfo station, int index, bool isLast) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        // Timeline Line and Dot
        Column(
          children: [
            Container(
              width: 20,
              height: 20,
              decoration: BoxDecoration(
                color: _getStatusColor(station.status),
                shape: BoxShape.circle,
                border: Border.all(
                  color: Colors.white,
                  width: 3,
                ),
                boxShadow: [
                  BoxShadow(
                    color: _getStatusColor(station.status).withOpacity(0.3),
                    blurRadius: 8,
                    spreadRadius: 2,
                  ),
                ],
              ),
              child: station.status == StationStatus.current
                  ? const Icon(
                      Icons.train,
                      color: Colors.white,
                      size: 12,
                    )
                  : null,
            ),
            if (!isLast)
              Container(
                width: 2,
                height: 60,
                color: _getStatusColor(station.status).withOpacity(0.3),
              ),
          ],
        ),
        const SizedBox(width: 16),

        // Station Info
        Expanded(
          child: Container(
            margin: const EdgeInsets.only(bottom: 20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Text(
                      station.stationName,
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                        color: _getStatusColor(station.status),
                      ),
                    ),
                    const Spacer(),
                    if (station.delayMinutes > 0)
                      Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 8,
                          vertical: 4,
                        ),
                        decoration: BoxDecoration(
                          color: AppTheme.errorColor.withOpacity(0.1),
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: Text(
                          '+${station.delayMinutes} min',
                          style: TextStyle(
                            fontSize: 12,
                            fontWeight: FontWeight.w600,
                            color: AppTheme.errorColor,
                          ),
                        ),
                      ),
                  ],
                ),
                const SizedBox(height: 8),
                Row(
                  children: [
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Scheduled: ${DateFormat('HH:mm').format(station.scheduledTime)}',
                            style: TextStyle(
                              fontSize: 14,
                              color: Colors.grey[600],
                            ),
                          ),
                          if (station.actualTime != null)
                            Text(
                              'Actual: ${DateFormat('HH:mm').format(station.actualTime!)}',
                              style: TextStyle(
                                fontSize: 14,
                                color: station.delayMinutes > 0 
                                    ? AppTheme.errorColor 
                                    : AppTheme.successColor,
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                        ],
                      ),
                    ),
                    if (station.haltDuration.isNotEmpty)
                      Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 8,
                          vertical: 4,
                        ),
                        decoration: BoxDecoration(
                          color: AppTheme.warningColor.withOpacity(0.1),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Text(
                          'Halt: ${station.haltDuration}',
                          style: TextStyle(
                            fontSize: 12,
                            color: AppTheme.warningColor,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ),
                  ],
                ),
                if (station.distanceFromStart > 0)
                  Padding(
                    padding: const EdgeInsets.only(top: 8),
                    child: Text(
                      '${station.distanceFromStart.toStringAsFixed(1)} km from start',
                      style: TextStyle(
                        fontSize: 12,
                        color: Colors.grey[500],
                      ),
                    ),
                  ),
              ],
            ),
          ),
        ),
      ],
    );
  }

  Color _getStatusColor(StationStatus status) {
    switch (status) {
      case StationStatus.completed:
        return AppTheme.successColor;
      case StationStatus.current:
        return AppTheme.errorColor;
      case StationStatus.next:
        return AppTheme.infoColor;
      case StationStatus.upcoming:
        return Colors.grey;
    }
  }

  Widget _buildBottomBanner(TrainStatus status) {
    final nextStation = status.stationStatuses.firstWhere(
      (s) => s.status == StationStatus.next,
      orElse: () => status.stationStatuses.first,
    );

    final timeToNext = nextStation.scheduledTime.difference(DateTime.now());
    final minutesToNext = timeToNext.inMinutes;

    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppTheme.infoColor.withOpacity(0.1),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(
          color: AppTheme.infoColor.withOpacity(0.3),
        ),
      ),
      child: Row(
        children: [
          Icon(
            Icons.info_outline,
            color: AppTheme.infoColor,
            size: 24,
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Next Station: ${nextStation.stationName}',
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.bold,
                    color: Colors.grey[800],
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  'Arriving in ${minutesToNext > 0 ? minutesToNext : 0} minutes',
                  style: TextStyle(
                    fontSize: 14,
                    color: Colors.grey[600],
                  ),
                ),
                if (status.delayMinutes > 0)
                  Text(
                    'Delay: +${status.delayMinutes} minutes',
                    style: TextStyle(
                      fontSize: 14,
                      color: AppTheme.errorColor,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
