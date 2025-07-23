const db = require('../dao/dao');
const mongodb = require('../dao/mongodbdao');
const axios = require('axios');

// ✨ Prediction function
const getPredictions = async (req, res) => {
  try {
    const response = await axios.get('http://localhost:4000/predict');
    res.json(response.data);
  } catch (err) {
    console.error("Prediction API failed:", err);
    res.status(500).json({ error: "Prediction failed" });
  }
};
module.exports = {
    // ✅ NEW: Get sector names
    getsectors: async (req, res) => {
        console.log("📥 GET /sectors called");

        if (!db || typeof db.query !== "function") {
            console.error("❌ DB is not connected or 'query' is not a function.");
            return res.status(500).send("Database not connected");
        }

        db.query('SELECT DISTINCT sector_name FROM companies', (err, result) => {
            if (err) {
                console.error("❌ Error fetching sectors:", err);
                return res.status(500).send("Error fetching sectors");
            }

            console.log("✅ Sectors fetched successfully:", result);
            res.status(200).json(result);
        });
    },

    // ✅ Existing: Get companies by sector
    getcompanies: async (req, res) => {
        console.log("📥 GET /getcompanies called");

        if (!db || typeof db.query !== "function") {
            console.error("❌ DB is not connected or 'query' is not a function.");
            return res.status(500).send("Database not connected");
        }

        const sector = req.query.sector;
        if (!sector) {
            console.warn("⚠️ No sector provided in query.");
            return res.status(400).send("Sector is required");
        }

        db.query('SELECT company_name FROM companies WHERE sector_name = ?', [sector], (err, result) => {
            if (err) {
                console.error("❌ Error fetching companies from DB:", err);
                return res.status(500).send("Error fetching companies");
            }

            console.log(`✅ Companies for sector "${sector}" fetched successfully:`, result);
            res.status(200).json(result);
        });
    },

    // ✅ Existing: Fetch all MongoDB posts
    fetchall: async (req, res) => {
        try {
            const mongo = await mongodb.connectDB();
            const collection = mongo.db("landslides").collection("posts");
            const data = await collection.find({}).toArray();
            res.json(data);
        } catch (error) {
            console.error("❌ Error fetching MongoDB data:", error);
            res.status(500).send('Error fetching data');
        }
    },
    getPredictions,
    // fetch.js

    getSectorDashboard: async (req, res) => {
    const sector = req.params.sector.toLowerCase();
    const company = req.query.company?.toLowerCase();

    let conn;
    try {
      conn = await req.pool.getConnection();

      let rows;
      if (company) {
        rows = await conn.query(`
          SELECT s.*
          FROM sensor_data s
          JOIN devices d ON s.device_id = d.device_id
          JOIN companies c ON d.company_name = c.company_name
          WHERE LOWER(c.sector_name) = ? AND LOWER(c.company_name) = ?
          ORDER BY s.timestamp DESC
          LIMIT 10
        `, [sector, company]);
      } else {
        rows = await conn.query(`
          SELECT s.*
          FROM sensor_data s
          JOIN devices d ON s.device_id = d.device_id
          JOIN companies c ON d.company_name = c.company_name
          WHERE LOWER(c.sector_name) = ?
          ORDER BY s.timestamp DESC
          LIMIT 10
        `, [sector]);
      }

      if (rows.length === 0) {
        return res.status(404).json({ error: `No data found for sector: ${sector}` });
      }

      const formatted = rows.reverse().map(row => ({
        ...row,
        time: new Date(row.timestamp).toLocaleTimeString([], {
          hour: '2-digit',
          minute: '2-digit',
        }),
      }));

      res.json(formatted);
    } catch (err) {
      console.error("❌ SQL Error in sector dashboard:", err);
      res.status(500).json({ error: "Failed to fetch sector data" });
    } finally {
      if (conn) {
        try {
          conn.release();
        } catch (releaseErr) {
          console.warn("⚠️ Error releasing connection:", releaseErr);
        }
      }
    }
  },

  getEquipmentStatus: async (req, res) => {
    let conn;
    try {
      conn = await req.pool.getConnection();

      const rows = await conn.query(`
        SELECT equipment_name, temperature, pressure, machine_runtime, tyre_pressure
        FROM (
          SELECT *
          FROM sensor_data
          WHERE equipment_name IN ('Excavator', 'Crusher', 'Truck', 'Loader')
          ORDER BY timestamp DESC
        ) AS latest_data
        GROUP BY equipment_name
      `);

      res.json(rows);
    } catch (err) {
      console.error("❌ Equipment Status Error:", err);
      res.status(500).json({ error: "Failed to fetch equipment stats" });
    } finally {
      if (conn) conn.release();
    }
  }
};


