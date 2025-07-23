import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutterapp/main.dart'; // Adjust the path if needed

void main() {
  testWidgets('Test MyApp Widget', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: MyApp(), // Ensure MyApp is a const constructor
      ),
    );

    // Update this to match actual UI text
    expect(find.text('Hello, World!'), findsOneWidget);
  });
}
