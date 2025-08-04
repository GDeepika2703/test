import 'package:flutter/material.dart';
import 'signin_page.dart';
import 'home_page.dart';
import 'signup_page.dart';

void main() {
  runApp(const MyApp()); // ✅ Use const for performance
}

class MyApp extends StatelessWidget {
  const MyApp({super.key}); // ✅ Use super.key in constructor

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter App',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => const SignInPage(),
        '/signin': (context) => const SignInPage(), // ✅ const constructors
        '/home': (context) => const HomePage(),
        '/signup': (context) => const SignUpPage(),
      },
    );
  }
}
