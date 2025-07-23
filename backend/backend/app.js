const express = require('express');
const path = require('path');
const cors = require('cors');
const mariadb = require('mariadb');
const fs = require('fs');

// Modular routes
const fetch = require('./routes/fetch');
const insert = require('./routes/insert');

const app = express();
const PORT = 5001;

// Middleware
app.use(cors());
app.use(express.json());

// Serve static Flutter HTML dashboards
const dashboardsPath = path.join('C:/Users/dell/Desktop/flutter_app/flutter_app/assets/dashboard');
app.use('/dashboards', express.static(dashboardsPath));

// MariaDB connection pool
const pool = mariadb.createPool({
  host: '104.154.141.198',
  user: 'root',
  password: 'vistaarnksh',
  database: 'pro',
  connectionLimit: 5,
  connectTimeout: 10000,
  acquireTimeout: 10000,
  idleTimeout: 60000
});

// Add MariaDB pool to request object
app.use((req, res, next) => {
  req.pool = pool;
  next();
});

// Keep-alive ping every 60s
setInterval(async () => {
  let conn;
  try {
    conn = await pool.getConnection();
    await conn.query('SELECT 1');
  } catch (err) {
    console.warn('⚠️ Keep-alive failed:', err);
  } finally {
    if (conn) conn.release();
  }
}, 60000);

// Routes from fetch.js
app.get('/getcompanies', fetch.getcompanies);
app.get('/sectors', fetch.getsectors);
app.get('/fetchall', fetch.fetchall);
app.get('/api/:sector/dashboard', fetch.getSectorDashboard);
app.get('/api/equipment-status', fetch.getEquipmentStatus);
app.get('/api/predict', fetch.getPredictions);
// Routes from insert.js
app.post('/register', insert.register);
app.post('/registertest', insert.registertest);
app.post('/signin', insert.signin);
app.post('/mailersend', insert.mailersend);
app.post('/getDashboard', insert.getDashboard);
app.post('/getDashboardDetails', insert.getDashboardDetails);
app.post('/forgot-password', insert.forgotPassword);
app.post('/postdata', insert.insertDht);
app.post('/getDashboard', insert.getDashboard);

// Test route
app.post('/test', (req, res) => {
  console.log("Test API called with:", req.body);
  res.json({ message: "Test successful", received: req.body });
});
// Health check
app.get('/', (req, res) => {
  res.send('Backend is running.');
});

// Start the server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`✅ Server running at http://localhost:${PORT}`);
});
