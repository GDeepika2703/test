import 'package:flutter/material.dart';
import 'package:intl_phone_field/intl_phone_field.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class ForgotPasswordPage extends StatefulWidget {
  const ForgotPasswordPage({super.key}); // added key

  @override
  State<ForgotPasswordPage> createState() => _ForgotPasswordPageState();
}

class _ForgotPasswordPageState extends State<ForgotPasswordPage> {
  String completePhone = '';
  final TextEditingController _newPasswordController = TextEditingController();
  final TextEditingController _confirmPasswordController = TextEditingController();
  bool isNewPasswordVisible = false;
  bool isConfirmPasswordVisible = false;

  Future<void> resetPassword() async {
    final newPassword = _newPasswordController.text.trim();
    final confirmPassword = _confirmPasswordController.text.trim();

    if (completePhone.isEmpty || newPassword.isEmpty || confirmPassword.isEmpty) {
      _showDialog('Error', 'All fields are required.');
      return;
    }
    if (newPassword != confirmPassword) {
      _showDialog('Error', 'Passwords do not match.');
      return;
    }

    final url = Uri.parse('http://104.154.141.198:5002/forgot-password');
    try {
      final response = await http.post(
        url,
        headers: const {'Content-Type': 'application/json'},
        body: json.encode({
          'phone_no': completePhone,
          'password': newPassword,
        }),
      );
      if (response.statusCode == 200) {
        _showDialog('Success', 'Password updated successfully.');
      } else {
        final data = json.decode(response.body);
        _showDialog('Error', data['message'] ?? 'User not found.');
      }
    } catch (e) {
      _showDialog('Error', 'Something went wrong. Please try again.');
    }
  }

  void _showDialog(String title, String message) {
    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        title: Text(title),
        content: Text(message),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(context); // Close the dialog
              if (title == 'Success') {
                Navigator.pushReplacementNamed(context, '/signin');
              }
            },
            child: const Text('OK'),
          ),
        ],
      ),
    );
  }

  InputDecoration _buildInputDecoration({
    required String label,
    required bool visible,
    required VoidCallback toggle,
  }) {
    return InputDecoration(
      labelText: label,
      labelStyle: const TextStyle(color: Colors.white),
      suffixIcon: IconButton(
        icon: Icon(
          visible ? Icons.visibility : Icons.visibility_off,
          color: Colors.white,
        ),
        onPressed: toggle,
      ),
      enabledBorder: const UnderlineInputBorder(
        borderSide: BorderSide(color: Colors.white),
      ),
      focusedBorder: const UnderlineInputBorder(
        borderSide: BorderSide(color: Colors.white),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        padding: const EdgeInsets.all(16),
        decoration: const BoxDecoration(
          gradient: LinearGradient(colors: [Colors.pink, Colors.blue]),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            IntlPhoneField(
              decoration: const InputDecoration(
                labelText: 'Phone Number',
                labelStyle: TextStyle(color: Colors.white),
                enabledBorder: UnderlineInputBorder(
                  borderSide: BorderSide(color: Colors.white),
                ),
                focusedBorder: UnderlineInputBorder(
                  borderSide: BorderSide(color: Colors.white),
                ),
              ),
              initialCountryCode: 'IN',
              style: const TextStyle(color: Colors.white),
              onChanged: (phone) {
                completePhone = phone.completeNumber;
              },
            ),
            const SizedBox(height: 10),
            TextField(
              controller: _newPasswordController,
              style: const TextStyle(color: Colors.white),
              obscureText: !isNewPasswordVisible,
              decoration: _buildInputDecoration(
                label: 'New Password',
                visible: isNewPasswordVisible,
                toggle: () {
                  setState(() {
                    isNewPasswordVisible = !isNewPasswordVisible;
                  });
                },
              ),
            ),
            const SizedBox(height: 10),
            TextField(
              controller: _confirmPasswordController,
              style: const TextStyle(color: Colors.white),
              obscureText: !isConfirmPasswordVisible,
              decoration: _buildInputDecoration(
                label: 'Confirm Password',
                visible: isConfirmPasswordVisible,
                toggle: () {
                  setState(() {
                    isConfirmPasswordVisible = !isConfirmPasswordVisible;
                  });
                },
              ),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              style: ElevatedButton.styleFrom(backgroundColor: Colors.white),
              onPressed: resetPassword,
              child: const Text('Reset Password', style: TextStyle(color: Colors.black)),
            ),
          ],
        ),
      ),
    );
  }
}
