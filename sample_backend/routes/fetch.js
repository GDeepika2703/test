const db = require('../dao/dao');

module.exports = {
    // ✅ NEW: Get sector names
    getsectors: async (req, res) => {
        console.log("📥 GET /sectors called");

        if (!db || typeof db.query !== "function") {
            console.error("❌ DB is not connected or 'query' is not a function.");
            return res.status(500).send("Database not connected");
        }

        db.query('SELECT DISTINCT sector_name FROM sector', (err, result) => {
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

    // ✅ Existing: Get regions by company
    getregions: (req, res) => {
    console.log("📥 GET /getregions called");
    console.log("Query params:", req.query);

    const company = req.query.company;
    if (!company) return res.status(400).send("Company is required");

    db.query(
        "SELECT region_name FROM regions WHERE company_name = ?",
        [company],
        (err, results) => {
        if (err) return res.status(500).send("DB error");
        console.log("Regions fetched:", results);
        res.json(results);
        }
    );
    }

}