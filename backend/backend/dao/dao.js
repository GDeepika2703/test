const mysql = require('mysql');
const config = require('../config/dbconfig'); // Import database config

// Create a single database connection
const db = mysql.createConnection(config);

// Connect to MySQL
db.connect((err) => {
    if (err) {
        console.error("Database connection failed:", err.stack);
        return;
    }
    console.log("Connected to MySQL Database with ID:", db.threadId);
});

module.exports = db; // Export the database connection
