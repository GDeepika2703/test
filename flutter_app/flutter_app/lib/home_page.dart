import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';
import 'package:shared_preferences/shared_preferences.dart';
//import 'package:flutter/services.dart' show rootBundle;
class HomePage extends StatefulWidget {
const HomePage({super.key}); // :white_check_mark: Fix: added key parameter
@override
HomePageState createState() => HomePageState(); // :white_check_mark: Fix: public state class
}
class HomePageState extends State<HomePage> {
String name = '';
String userId = '';
String companyName = '';
String sectorName = '';
bool isLoading = false;
bool isWebViewLoaded = false;
late final WebViewController _webViewController;
@override
void initState() {
super.initState();
_loadUserData();
_webViewController = WebViewController()
..setJavaScriptMode(JavaScriptMode.unrestricted)
..setNavigationDelegate(
NavigationDelegate(
onPageStarted: (url) {
setState(() {
isLoading = true;
isWebViewLoaded = false;
});
},
onPageFinished: (url) {
setState(() {
isLoading = false;
isWebViewLoaded = true;
});
},
onWebResourceError: (error) {
_showErrorDialog('Error loading web resource: ${error.description}');
},
),
);
}
Future<void> _loadUserData() async {
final prefs = await SharedPreferences.getInstance();
setState(() {
name = prefs.getString('name') ?? 'No Name';
userId = prefs.getString('user_id') ?? 'No User ID';
companyName = prefs.getString('company_name') ?? 'No Company Name';
sectorName = prefs.getString('sector_name')?.toLowerCase() ?? '';
});
}
void _showErrorDialog(String message) {
showDialog(
context: context,
builder: (BuildContext context) => AlertDialog(
title: const Text('Error'),
content: Text(message),
actions: <Widget>[
TextButton(
onPressed: () => Navigator.of(context).pop(),
child: const Text('OK'),
),
],
),
);
}
Future<void> _logout() async {
final prefs = await SharedPreferences.getInstance();
await prefs.clear();
if (!mounted) return; // :white_check_mark: Fix: prevent context use after unmounted
Navigator.pushReplacementNamed(context, '/');
}
Future<void> _loadDashboard() async {
    if (companyName.isEmpty || sectorName.isEmpty) {
      _showErrorDialog('Company or Sector data missing.');
      return;
    }

    final url = 'http://10.5.48.48:5001/dashboards/$sectorName.html'
        '?company=${Uri.encodeComponent(companyName)}'
        '&sector=${Uri.encodeComponent(sectorName)}';

    try {
      await _webViewController.loadRequest(Uri.parse(url));
    } catch (e) {
      _showErrorDialog('Failed to load dashboard: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Dashboard'),
        actions: [
          IconButton(
            icon: const Icon(Icons.exit_to_app),
            onPressed: _logout,
          ),
        ],
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Text('Hello, $name from $companyName'),
          ),
          ElevatedButton(
            onPressed: _loadDashboard,
            child: const Text('Load Dashboard'),
          ),
          Expanded(
            child: WebViewWidget(controller: _webViewController),
          ),
          if (isWebViewLoaded && !isLoading) const Text('WebView Loaded!'),
          const SizedBox(height: 20),
          ElevatedButton(
            onPressed: _logout,
            child: const Text('Logout'),
          ),
        ],
      ),
    );
  }
}