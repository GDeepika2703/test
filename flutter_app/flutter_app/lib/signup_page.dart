import 'package:flutter/material.dart';
import 'package:intl_phone_field/intl_phone_field.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class SignUpPage extends StatefulWidget {
  const SignUpPage({super.key}); // ✅ Added key

  @override
  State<SignUpPage> createState() => _SignUpPageState();
}

class _SignUpPageState extends State<SignUpPage> {
  final _nameController = TextEditingController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  String _completePhone = '';
  String? _selectedSector;
  String? _selectedCompany;
  List<String> _sectors = [];
  List<String> _companies = [];
  bool _isPasswordVisible = false;

  @override
  void initState() {
    super.initState();
    fetchSectors();
  }

  Future<void> fetchSectors() async {
    try {
      final response = await http.get(Uri.parse('http://10.5.48.48:5001/sectors'));
      if (response.statusCode == 200) {
        final data = json.decode(response.body) as List;
        setState(() {
          _sectors = data
              .map((e) => (e['sector_name'] as String?) ?? '')
              .map((name) => name[0].toUpperCase() + name.substring(1))
              .toList();
        });
      } else {
        _showAlert('Failed to load sectors.');
      }
    } catch (_) {
      _showAlert('Unexpected error fetching sectors.');
    }
  }

  Future<void> fetchCompaniesBySector(String sector) async {
    try {
      final response = await http.get(Uri.parse('http://10.5.48.48:5001/getcompanies?sector=$sector'));
      if (response.statusCode == 200) {
        final data = json.decode(response.body) as List;
        setState(() {
          _companies = data.map((e) => e['company_name'].toString()).toList();
          _selectedCompany = null;
        });
      } else {
        _showAlert('Failed to load companies.');
      }
    } catch (_) {
      _showAlert('Unexpected error fetching companies.');
    }
  }

  Future<void> signUp() async {
    final name = _nameController.text.trim();
    final phone = _completePhone;
    final email = _emailController.text.trim();
    final password = _passwordController.text.trim();
    final sector = _selectedSector ?? '';
    final company = _selectedCompany ?? '';

    if ([name, phone, email, password, sector, company].any((e) => e.isEmpty)) {
      _showAlert('Please fill in all fields.');
      return;
    }

    final url = Uri.parse('http://10.5.48.48:5001/register');
    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'name': name,
          'phone_no': phone,
          'email': email,
          'password': password,
          'sector_name': sector,
          'company_name': company,
        }),
      );

      final data = json.decode(response.body);
      if (response.statusCode == 201 && data['status'] == 'success') {
        _showAlert('User successfully registered.', onOk: () {
          Navigator.pushReplacementNamed(context, '/home');
        });
      } else {
        _showAlert(data['message'] ?? 'An error occurred.');
      }
    } catch (_) {
      _showAlert('Something went wrong. Try again later.');
    }
  }

  void _showAlert(String msg, {VoidCallback? onOk}) {
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        content: Text(msg),
        actions: [
          TextButton(
            onPressed: () {
              Navigator.pop(ctx);
              if (onOk != null) onOk();
            },
            child: const Text('OK'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(colors: [Colors.pink, Colors.blue]),
        ),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: ListView(
            children: [
              const SizedBox(height: 80),
              _buildTextField(_nameController, 'Name'),
              const SizedBox(height: 10),
              _buildPhoneField(),
              const SizedBox(height: 10),
              _buildTextField(_emailController, 'Email'),
              const SizedBox(height: 10),
              _buildPasswordField(),
              const SizedBox(height: 10),
              _buildDropdown(
                hint: 'Select Sector',
                value: _selectedSector,
                items: _sectors,
                onChanged: (value) {
                  setState(() {
                    _selectedSector = value;
                    _selectedCompany = null;
                    _companies.clear();
                  });
                  if (value != null) fetchCompaniesBySector(value);
                },
              ),
              if (_sectors.isEmpty)
                const Padding(
                  padding: EdgeInsets.only(top: 8.0),
                  child: Text(
                    '⚠️ Failed to load sectors. Please check your network.',
                    style: TextStyle(color: Colors.white),
                  ),
                ),
              if (_companies.isNotEmpty)
                _buildDropdown(
                  hint: 'Select Company',
                  value: _selectedCompany,
                  items: _companies,
                  onChanged: (value) {
                    setState(() {
                      _selectedCompany = value;
                    });
                  },
                ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: signUp,
                style: ElevatedButton.styleFrom(backgroundColor: Colors.white),
                child: const Text('Sign Up', style: TextStyle(color: Colors.black)),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildTextField(TextEditingController controller, String label) {
    return TextField(
      controller: controller,
      style: const TextStyle(color: Colors.white),
      decoration: InputDecoration(
        labelText: label,
        labelStyle: const TextStyle(color: Colors.white),
        enabledBorder: const UnderlineInputBorder(borderSide: BorderSide(color: Colors.white)),
        focusedBorder: const UnderlineInputBorder(borderSide: BorderSide(color: Colors.white)),
      ),
    );
  }

  Widget _buildPasswordField() {
    return TextField(
      controller: _passwordController,
      obscureText: !_isPasswordVisible,
      style: const TextStyle(color: Colors.white),
      decoration: InputDecoration(
        labelText: 'Password',
        labelStyle: const TextStyle(color: Colors.white),
        enabledBorder: const UnderlineInputBorder(borderSide: BorderSide(color: Colors.white)),
        focusedBorder: const UnderlineInputBorder(borderSide: BorderSide(color: Colors.white)),
        suffixIcon: IconButton(
          icon: Icon(
            _isPasswordVisible ? Icons.visibility : Icons.visibility_off,
            color: Colors.white,
          ),
          onPressed: () => setState(() => _isPasswordVisible = !_isPasswordVisible),
        ),
      ),
    );
  }

  Widget _buildPhoneField() {
    return Theme(
      data: Theme.of(context).copyWith(
        primaryColor: Colors.white,
        hintColor: Colors.white,
        inputDecorationTheme: const InputDecorationTheme(
          enabledBorder: UnderlineInputBorder(borderSide: BorderSide(color: Colors.white)),
          focusedBorder: UnderlineInputBorder(borderSide: BorderSide(color: Colors.white)),
        ),
      ),
      child: IntlPhoneField(
        decoration: const InputDecoration(
          labelText: 'Phone Number',
          labelStyle: TextStyle(color: Colors.white),
        ),
        initialCountryCode: 'IN',
        style: const TextStyle(color: Colors.white),
        onChanged: (phone) => _completePhone = phone.completeNumber,
      ),
    );
  }

  Widget _buildDropdown({
    required String hint,
    required String? value,
    required List<String> items,
    required ValueChanged<String?> onChanged,
  }) {
    return DropdownButton<String>(
      value: value,
      hint: Text(hint, style: const TextStyle(color: Colors.white)),
      dropdownColor: Colors.white,
      isExpanded: true,
      onChanged: onChanged,
      items: items.map((item) {
        return DropdownMenuItem<String>(
          value: item,
          child: Text(item, style: const TextStyle(color: Colors.black)),
        );
      }).toList(),
    );
  }
}
