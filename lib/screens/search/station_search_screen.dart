import 'package:flutter/material.dart';
import 'package:train_jatri/models/train_schedule.dart';
import 'package:train_jatri/services/train_service.dart';
import 'package:train_jatri/screens/train_schedule_screen.dart';
import 'package:train_jatri/utils/theme.dart';

class StationSearchScreen extends StatefulWidget {
  const StationSearchScreen({super.key});

  @override
  State<StationSearchScreen> createState() => _StationSearchScreenState();
}

class _StationSearchScreenState extends State<StationSearchScreen> {
  final _fromController = TextEditingController();
  final _toController = TextEditingController();
  List<Station> _stations = [];
  List<Station> _filteredFromStations = [];
  List<Station> _filteredToStations = [];
  bool _isLoading = false;
  bool _showFromSuggestions = false;
  bool _showToSuggestions = false;

  @override
  void initState() {
    super.initState();
    _loadStations();
  }

  @override
  void dispose() {
    _fromController.dispose();
    _toController.dispose();
    super.dispose();
  }

  Future<void> _loadStations() async {
    setState(() {
      _isLoading = true;
    });

    try {
      final stations = await TrainService.getAllStations();
      setState(() {
        _stations = stations;
        _filteredFromStations = stations;
        _filteredToStations = stations;
      });
    } catch (e) {
      // Handle error
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  void _filterFromStations(String query) {
    if (query.isEmpty) {
      setState(() {
        _filteredFromStations = _stations;
        _showFromSuggestions = false;
      });
    } else {
      final filtered = _stations.where((station) {
        return station.name.toLowerCase().contains(query.toLowerCase());
      }).toList();
      setState(() {
        _filteredFromStations = filtered;
        _showFromSuggestions = true;
      });
    }
  }

  void _filterToStations(String query) {
    if (query.isEmpty) {
      setState(() {
        _filteredToStations = _stations;
        _showToSuggestions = false;
      });
    } else {
      final filtered = _stations.where((station) {
        return station.name.toLowerCase().contains(query.toLowerCase());
      }).toList();
      setState(() {
        _filteredToStations = filtered;
        _showToSuggestions = true;
      });
    }
  }

  void _selectFromStation(Station station) {
    setState(() {
      _fromController.text = station.name;
      _showFromSuggestions = false;
    });
  }

  void _selectToStation(Station station) {
    setState(() {
      _toController.text = station.name;
      _showToSuggestions = false;
    });
  }

  Future<void> _searchTrains() async {
    if (_fromController.text.isEmpty || _toController.text.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Please select both from and to stations'),
        ),
      );
      return;
    }

    setState(() {
      _isLoading = true;
    });

    try {
      final trains = await TrainService.searchTrainsByStations(
        _fromController.text,
        _toController.text,
      );

      if (mounted) {
        Navigator.of(context).push(
          MaterialPageRoute(
            builder: (_) => TrainScheduleScreen(
              trains: trains,
              fromStation: _fromController.text,
              toStation: _toController.text,
            ),
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error searching trains: $e'),
          ),
        );
      }
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Station to Station'),
        elevation: 0,
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : Padding(
              padding: const EdgeInsets.all(24.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  // From Station
                  Text(
                    'From Station',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w600,
                      color: Colors.grey[700],
                    ),
                  ),
                  const SizedBox(height: 8),
                  TextFormField(
                    controller: _fromController,
                    decoration: InputDecoration(
                      hintText: 'Select departure station',
                      prefixIcon: const Icon(Icons.location_on_outlined),
                      suffixIcon: _fromController.text.isNotEmpty
                          ? IconButton(
                              icon: const Icon(Icons.clear),
                              onPressed: () {
                                _fromController.clear();
                                _filterFromStations('');
                              },
                            )
                          : null,
                    ),
                    onChanged: _filterFromStations,
                    onTap: () {
                      if (_fromController.text.isNotEmpty) {
                        _showFromSuggestions = true;
                      }
                    },
                  ),
                  if (_showFromSuggestions && _filteredFromStations.isNotEmpty)
                    Container(
                      constraints: const BoxConstraints(maxHeight: 200),
                      child: Card(
                        elevation: 4,
                        child: ListView.builder(
                          shrinkWrap: true,
                          itemCount: _filteredFromStations.length,
                          itemBuilder: (context, index) {
                            final station = _filteredFromStations[index];
                            return ListTile(
                              title: Text(station.name),
                              subtitle: Text(
                                '${station.latitude.toStringAsFixed(4)}, ${station.longitude.toStringAsFixed(4)}',
                              ),
                              onTap: () => _selectFromStation(station),
                            );
                          },
                        ),
                      ),
                    ),
                  const SizedBox(height: 24),

                  // To Station
                  Text(
                    'To Station',
                    style: TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w600,
                      color: Colors.grey[700],
                    ),
                  ),
                  const SizedBox(height: 8),
                  TextFormField(
                    controller: _toController,
                    decoration: InputDecoration(
                      hintText: 'Select destination station',
                      prefixIcon: const Icon(Icons.location_on),
                      suffixIcon: _toController.text.isNotEmpty
                          ? IconButton(
                              icon: const Icon(Icons.clear),
                              onPressed: () {
                                _toController.clear();
                                _filterToStations('');
                              },
                            )
                          : null,
                    ),
                    onChanged: _filterToStations,
                    onTap: () {
                      if (_toController.text.isNotEmpty) {
                        _showToSuggestions = true;
                      }
                    },
                  ),
                  if (_showToSuggestions && _filteredToStations.isNotEmpty)
                    Container(
                      constraints: const BoxConstraints(maxHeight: 200),
                      child: Card(
                        elevation: 4,
                        child: ListView.builder(
                          shrinkWrap: true,
                          itemCount: _filteredToStations.length,
                          itemBuilder: (context, index) {
                            final station = _filteredToStations[index];
                            return ListTile(
                              title: Text(station.name),
                              subtitle: Text(
                                '${station.latitude.toStringAsFixed(4)}, ${station.longitude.toStringAsFixed(4)}',
                              ),
                              onTap: () => _selectToStation(station),
                            );
                          },
                        ),
                      ),
                    ),
                  const SizedBox(height: 32),

                  // Search Button
                  ElevatedButton(
                    onPressed: _isLoading ? null : _searchTrains,
                    style: ElevatedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 16),
                    ),
                    child: _isLoading
                        ? const SizedBox(
                            height: 20,
                            width: 20,
                            child: CircularProgressIndicator(
                              strokeWidth: 2,
                              valueColor: AlwaysStoppedAnimation<Color>(Colors.white),
                            ),
                          )
                        : const Text(
                            'Search Trains',
                            style: TextStyle(fontSize: 16),
                          ),
                  ),

                  const SizedBox(height: 24),

                  // Info Card
                  Card(
                    child: Padding(
                      padding: const EdgeInsets.all(16),
                      child: Row(
                        children: [
                          Icon(
                            Icons.info_outline,
                            color: AppTheme.infoColor,
                            size: 24,
                          ),
                          const SizedBox(width: 16),
                          Expanded(
                            child: Text(
                              'Find all available trains between the selected stations with schedules and real-time status.',
                              style: TextStyle(
                                color: Colors.grey[600],
                                fontSize: 14,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ],
              ),
            ),
    );
  }
}
