# 🚂 TrainJatri - Bangladesh Railway Live Tracking App

A comprehensive Flutter application for real-time train tracking and schedule management in Bangladesh Railway system.

## ✨ Features

### 🔍 Search & Discovery
- **Station-to-Station Search**: Find trains between any two stations
- **Train-wise Search**: Search by train number or name
- **Smart Suggestions**: Auto-complete with station names and coordinates

### 📱 Live Tracking
- **Real-time Status**: Live train position and movement
- **Vertical Timeline**: Beautiful journey progress visualization
- **Delay Information**: Real-time delay updates and ETA
- **Distance Metrics**: Distance covered and remaining to next station

### 👥 Crowd Validation
- **User Confirmation**: "Are you inside this train?" popup
- **Crowd-sourced Accuracy**: Multiple users improve tracking precision
- **Location Services**: GPS integration for better accuracy

### 🎨 User Experience
- **Modern UI/UX**: Material Design 3 with beautiful animations
- **Dark/Light Themes**: Theme switching with system preference support
- **Responsive Design**: Works on all screen sizes
- **Offline Support**: Cached data when network unavailable

### 🔐 Authentication
- **Firebase Auth**: Email/password and Google Sign-in
- **User Profiles**: Personalized experience and favorites
- **Secure Data**: Encrypted user preferences and history

## 🏗️ Architecture

### Frontend (Flutter)
- **State Management**: Provider pattern for app-wide state
- **Navigation**: Bottom navigation with tab-based structure
- **Theming**: Custom theme system with Material 3 support
- **Models**: Strongly-typed data models for type safety

### Backend Integration
- **REST API**: Flask/FastAPI backend for live data
- **JSON Data**: Pre-processed railway datasets
- **Real-time Updates**: WebSocket support for live tracking

### Data Sources
- **Stations**: 200+ railway stations with coordinates
- **Schedules**: 132 train schedules with detailed routes
- **Segments**: 500m resolution railway line geometry
- **Route Mapping**: Train-specific route segment connections

## 📁 Project Structure

```
lib/
├── main.dart                 # App entry point
├── models/                   # Data models
│   ├── train_schedule.dart   # Train schedule data
│   ├── train_status.dart     # Live tracking data
│   └── station.dart         # Station information
├── providers/                # State management
│   ├── auth_provider.dart    # Authentication state
│   └── theme_provider.dart   # Theme preferences
├── screens/                  # UI screens
│   ├── splash_screen.dart    # App launch screen
│   ├── home_screen.dart      # Main dashboard
│   ├── search/               # Search functionality
│   ├── train_status_screen.dart # Live tracking view
│   └── settings_screen.dart  # App preferences
├── services/                 # Business logic
│   └── train_service.dart    # API and data services
└── utils/                    # Utilities
    └── theme.dart           # App theming
```

## 🚀 Getting Started

### Prerequisites
- Flutter SDK 3.0.0 or higher
- Dart SDK 3.0.0 or higher
- Android Studio / VS Code
- Firebase project setup

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/train-jatri.git
   cd train-jatri
   ```

2. **Install dependencies**
   ```bash
   flutter pub get
   ```

3. **Firebase Setup**
   - Create a Firebase project
   - Enable Authentication (Email/Password, Google)
   - Download `google-services.json` (Android) and `GoogleService-Info.plist` (iOS)
   - Place them in the appropriate platform folders

4. **Run the app**
   ```bash
   flutter run
   ```

### Configuration

1. **Update API endpoints** in `lib/services/train_service.dart`
2. **Configure Firebase** in your project
3. **Set up backend services** for live data
4. **Update station data** if needed

## 🔧 Backend Integration

### API Endpoints
- `GET /api/trains/search?from={station}&to={station}` - Station search
- `GET /api/trains/search?number={train_number}` - Train search
- `GET /api/trains/{train_number}/status` - Live status
- `POST /api/trains/{train_number}/confirm` - User confirmation

### Data Flow
1. **Schedule Data**: Loaded from JSON files
2. **Live Updates**: Real-time GPS and crowd data
3. **Position Calculation**: Matches GPS to railway segments
4. **Delay Simulation**: Fallback when live data unavailable

## 📊 Data Models

### Train Schedule
```dart
class TrainSchedule {
  final String trainName;
  final String trainModel;
  final List<String> days;
  final List<StationRoute> routes;
  final String totalDuration;
}
```

### Live Status
```dart
class TrainStatus {
  final String trainNumber;
  final List<StationStatusInfo> stationStatuses;
  final double currentSpeed;
  final double distanceCovered;
  final int delayMinutes;
}
```

## 🎨 UI Components

### Timeline Visualization
- **Vertical Progress Line**: Journey representation
- **Status Indicators**: Color-coded station states
- **Train Icon**: Current position marker
- **Delay Badges**: Real-time delay information

### Search Interface
- **Auto-complete**: Smart station suggestions
- **Filter Options**: Multiple search criteria
- **Results Display**: Rich train information cards

## 🔒 Security Features

- **Firebase Authentication**: Secure user management
- **Data Encryption**: Sensitive information protection
- **API Security**: Backend authentication and validation
- **Privacy Controls**: User data management options

## 📱 Platform Support

- **Android**: API level 21+ (Android 5.0+)
- **iOS**: iOS 11.0+
- **Web**: Responsive web application
- **Desktop**: Windows, macOS, Linux support

## 🚧 Development Roadmap

### Phase 1 (Current)
- ✅ Basic app structure
- ✅ Authentication system
- ✅ Search functionality
- ✅ Basic UI components

### Phase 2 (Next)
- 🔄 Real-time tracking
- 🔄 Push notifications
- 🔄 Offline support
- 🔄 Performance optimization

### Phase 3 (Future)
- 📋 Advanced analytics
- 📋 Social features
- 📋 Multi-language support
- 📋 AR navigation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Bangladesh Railway for route data
- Flutter team for the amazing framework
- Firebase for authentication services
- Open source community for inspiration

## 📞 Support

- **Email**: support@trainjatri.com
- **Documentation**: [docs.trainjatri.com](https://docs.trainjatri.com)
- **Issues**: [GitHub Issues](https://github.com/yourusername/train-jatri/issues)

---

Made with ❤️ for Bangladesh Railway passengers
