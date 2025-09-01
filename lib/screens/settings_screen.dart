import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:train_jatri/providers/auth_provider.dart';
import 'package:train_jatri/providers/theme_provider.dart';
import 'package:train_jatri/utils/theme.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Settings'),
        elevation: 0,
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // Account Section
          _buildSectionHeader('Account'),
          _buildAccountSection(context),
          const SizedBox(height: 24),

          // App Preferences Section
          _buildSectionHeader('App Preferences'),
          _buildThemeSection(context),
          _buildNotificationSection(context),
          const SizedBox(height: 24),

          // About Section
          _buildSectionHeader('About'),
          _buildAboutSection(context),
        ],
      ),
    );
  }

  Widget _buildSectionHeader(String title) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 12),
      child: Text(
        title,
        style: TextStyle(
          fontSize: 18,
          fontWeight: FontWeight.bold,
          color: AppTheme.primaryColor,
        ),
      ),
    );
  }

  Widget _buildAccountSection(BuildContext context) {
    return Consumer<AuthProvider>(
      builder: (context, authProvider, child) {
        final user = authProvider.user;
        return Card(
          child: Column(
            children: [
              ListTile(
                leading: CircleAvatar(
                  backgroundImage: user?.photoURL != null
                      ? NetworkImage(user!.photoURL!)
                      : null,
                  child: user?.photoURL == null
                      ? Text(user?.displayName?.substring(0, 1).toUpperCase() ?? 'U')
                      : null,
                ),
                title: Text(user?.displayName ?? 'User'),
                subtitle: Text(user?.email ?? ''),
                trailing: IconButton(
                  icon: const Icon(Icons.edit),
                  onPressed: () {
                    // TODO: Navigate to profile edit screen
                  },
                ),
              ),
              const Divider(height: 1),
              ListTile(
                leading: const Icon(Icons.logout),
                title: const Text('Sign Out'),
                onTap: () async {
                  final confirmed = await _showSignOutDialog(context);
                  if (confirmed) {
                    await authProvider.signOut();
                  }
                },
              ),
            ],
          ),
        );
      },
    );
  }

  Widget _buildThemeSection(BuildContext context) {
    return Consumer<ThemeProvider>(
      builder: (context, themeProvider, child) {
        return Card(
          child: Column(
            children: [
              ListTile(
                leading: const Icon(Icons.palette),
                title: const Text('Theme'),
                subtitle: Text(_getThemeModeText(themeProvider.themeMode)),
                trailing: PopupMenuButton<ThemeMode>(
                  onSelected: themeProvider.setThemeMode,
                  itemBuilder: (context) => [
                    const PopupMenuItem(
                      value: ThemeMode.system,
                      child: Text('System'),
                    ),
                    const PopupMenuItem(
                      value: ThemeMode.light,
                      child: Text('Light'),
                    ),
                    const PopupMenuItem(
                      value: ThemeMode.dark,
                      child: Text('Dark'),
                    ),
                  ],
                  child: const Icon(Icons.arrow_drop_down),
                ),
              ),
              ListTile(
                leading: const Icon(Icons.brightness_6),
                title: const Text('Dark Mode'),
                trailing: Switch(
                  value: themeProvider.isDarkMode,
                  onChanged: (value) {
                    if (value) {
                      themeProvider.setThemeMode(ThemeMode.dark);
                    } else {
                      themeProvider.setThemeMode(ThemeMode.light);
                    }
                  },
                ),
              ),
            ],
          ),
        );
      },
    );
  }

  Widget _buildNotificationSection(BuildContext context) {
    return Card(
      child: Column(
        children: [
          ListTile(
            leading: const Icon(Icons.notifications),
            title: const Text('Push Notifications'),
            subtitle: const Text('Get updates about train delays and status'),
            trailing: Switch(
              value: true, // TODO: Implement notification preferences
              onChanged: (value) {
                // TODO: Update notification preferences
              },
            ),
          ),
          ListTile(
            leading: const Icon(Icons.schedule),
            title: const Text('Delay Alerts'),
            subtitle: const Text('Notify when trains are delayed'),
            trailing: Switch(
              value: true, // TODO: Implement delay alert preferences
              onChanged: (value) {
                // TODO: Update delay alert preferences
              },
            ),
          ),
          ListTile(
            leading: const Icon(Icons.location_on),
            title: const Text('Location Services'),
            subtitle: const Text('Use location for better tracking'),
            trailing: Switch(
              value: true, // TODO: Implement location service preferences
              onChanged: (value) {
                // TODO: Update location service preferences
              },
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildAboutSection(BuildContext context) {
    return Card(
      child: Column(
        children: [
          ListTile(
            leading: const Icon(Icons.info),
            title: const Text('App Version'),
            subtitle: const Text('1.0.0'),
            trailing: const Icon(Icons.arrow_forward_ios, size: 16),
            onTap: () {
              _showAboutDialog(context);
            },
          ),
          ListTile(
            leading: const Icon(Icons.privacy_tip),
            title: const Text('Privacy Policy'),
            trailing: const Icon(Icons.arrow_forward_ios, size: 16),
            onTap: () {
              // TODO: Navigate to privacy policy
            },
          ),
          ListTile(
            leading: const Icon(Icons.description),
            title: const Text('Terms of Service'),
            trailing: const Icon(Icons.arrow_forward_ios, size: 16),
            onTap: () {
              // TODO: Navigate to terms of service
            },
          ),
          ListTile(
            leading: const Icon(Icons.help),
            title: const Text('Help & Support'),
            trailing: const Icon(Icons.arrow_forward_ios, size: 16),
            onTap: () {
              // TODO: Navigate to help & support
            },
          ),
        ],
      ),
    );
  }

  String _getThemeModeText(ThemeMode mode) {
    switch (mode) {
      case ThemeMode.system:
        return 'System Default';
      case ThemeMode.light:
        return 'Light';
      case ThemeMode.dark:
        return 'Dark';
    }
  }

  Future<bool> _showSignOutDialog(BuildContext context) async {
    return await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Sign Out'),
        content: const Text('Are you sure you want to sign out?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(false),
            child: const Text('Cancel'),
          ),
          ElevatedButton(
            onPressed: () => Navigator.of(context).pop(true),
            style: ElevatedButton.styleFrom(
              backgroundColor: AppTheme.errorColor,
            ),
            child: const Text('Sign Out'),
          ),
        ],
      ),
    ) ?? false;
  }

  void _showAboutDialog(BuildContext context) {
    showAboutDialog(
      context: context,
      applicationName: 'TrainJatri',
      applicationVersion: '1.0.0',
      applicationIcon: Container(
        width: 60,
        height: 60,
        decoration: BoxDecoration(
          color: AppTheme.primaryColor,
          borderRadius: BorderRadius.circular(12),
        ),
        child: const Icon(
          Icons.train,
          color: Colors.white,
          size: 30,
        ),
      ),
      children: [
        const Text(
          'TrainJatri is a comprehensive Bangladesh Railway live train tracking and schedule app.',
        ),
        const SizedBox(height: 16),
        const Text(
          'Features include:\n'
          '• Real-time train tracking\n'
          '• Station-to-station search\n'
          '• Live delay information\n'
          '• Crowd-sourced validation\n'
          '• Beautiful timeline interface',
        ),
        const SizedBox(height: 16),
        Text(
          '© 2024 TrainJatri. All rights reserved.',
          style: TextStyle(
            color: Colors.grey[600],
            fontSize: 12,
          ),
        ),
      ],
    );
  }
}
