const express = require('express');
const router = express.Router();
const fetch = require('./routes/fetch');
const insert = require('./routes/insert');
const path = require('path');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));


const PORT = 5001;

// Company/region APIs
app.get('/getcompanies', fetch.getcompanies);
app.get('/sectors', fetch.getsectors);
app.get('/getregions', fetch.getregions);



// Dashboard APIs
app.get('/fetch-dashboard-data', insert.fetchDashboardData);
app.get('/api/get_last_10_zaxis', insert.getLast10ZAxis);
app.post('/api/sensor-data', insert.receiveSensorData);
app.post('/insert-realtime-data',insert.insertRealtimeData);
app.post('/api/store_avg_values', async (req, res) => {
  const { device_id, timestamp, avg_fuel, avg_gradient } = req.body;
  const sql = `
    INSERT INTO realtime_sensor_data (device_id, timestamp, fuel_consumption_l_per_100km, avg_gradient)
    VALUES (?, ?, ?, ?)
  `;
  try {
    await db.query(sql, [device_id, timestamp, avg_fuel, avg_gradient]);
    res.send({ success: true });
  } catch (err) {
    console.error(err);
    res.status(500).send({ error: 'Database insert failed' });
  }
});


// Auth / Registration
app.post('/register', insert.register);
app.post('/signin', insert.signin);
app.post('/forgot-password', insert.forgotPassword);

// ✅ New: register FCM token from Flutter
app.post('/register-token', insert.registerToken);

// Test route
app.post('/test', (req, res) => {
  console.log("Test API called with:", req.body);
  res.json({ message: "Test successful", received: req.body });
});

// Dashboard web page
app.get('/dashboard', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'dashboard.html'));
});

// Root
app.get('/', (req, res) => {
  res.send('');
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server is running on http://0.0.0.0:${PORT}`);
});


