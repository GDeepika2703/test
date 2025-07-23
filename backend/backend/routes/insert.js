
const db = require('../dao/dao');
const mongodb = require('../dao/mongodbdao')
const nodemailer =require('nodemailer');
const { MailerSend, EmailParams, Sender, Recipient } = require('mailersend');

const generateRandomNumber = () => {
    return Math.floor(1000000 + Math.random() * 9000000); 
  }

const sendMailRegistration = async (toEmail, userName) => {
    try {
        let transporter = nodemailer.createTransport({
            service: 'gmail',
            host: "smtp.gmail.com",
            secure: false,
            port: 587,
            auth: {
                user: 'usha@velastra.co',
                pass: 'xzpw ixjm qpax jaim'  // no quotes or spaces in actual password
            },
            tls: {
                rejectUnauthorized: false  // allow self-signed certs
            }
            
        });

        let mailOptions = {
            from: "usha@velastra.co",
            to: toEmail, 
            subject: "Welcome to Velastra!",
            text: `Hello ${userName},\n\nWelcome to Velastra! Your account has been successfully registered.\n\nBest Regards,\nVistaarnksh Team`
        };

        let info = await transporter.sendMail(mailOptions);
        console.log(`Email sent to ${toEmail}: `, info.response);
    } catch (error) {
        console.error("Error sending welcome email:", error);
    }
};

const sendMailToCompany = async (companyMail , userDetails) => { 
    try {
        let transporter = nodemailer.createTransport({
            service: 'gmail',
            host: "smtp.gmail.com",
            secure: false,
            port: 587,
            auth: {
                user: 'usha@velastra.co',
                pass: 'xzpw ixjm qpax jaim'  // no quotes or spaces in actual password
            },
            tls: {
                rejectUnauthorized: false  // allow self-signed certs
            }
        });

        let mailOptions = {
            from: "usha@velastra.co",
            to: companyMail, 
            subject: "New User Registration – Grant Access Required",
            text: `Hello,\n\nA new user has registered for your company. Below are the details:\n
            - Name: ${userDetails.name}
            - Email: ${userDetails.email}
            - Phone: ${userDetails.phone_no}
            - Company: ${userDetails.company_name}

            Please review their details and grant access if necessary.\n\nBest Regards,\nVistaarnksh Team`
        };

        let info = await transporter.sendMail(mailOptions);
        console.log(`Email sent to ${companyMail}: `, info.response);
    } catch (error) {
        console.error("Error sending email:", error);
    }
};



module.exports  = {

    getDashboardDetails: (req, res) => {
        const { user_id } = req.body; // Ensure 'user_id' is used
    
        if ( !user_id) {  // Use the correct variable names
            return res.status(400).json({ message: "Company name and user ID are required" });
        }
    
            const getDashboarddata = `SELECT 
                dd.*,
                d.*
            FROM 
                users u
            JOIN 
                companies c ON u.company_name = c.company_name
            JOIN 
                dashboards d ON c.company_id = d.company_id
            JOIN 
                dashboard_data dd ON d.dashboard_id = dd.dashboard_id
            WHERE 
                u.user_id = ?
                AND u.access = 'verified'`;
    
            db.query(getDashboarddata, [user_id], (err, result) => {
                if (err) {
                    console.error('Error fetching dashboard data:', err);
                    return res.status(500).json({ error: 'Database error' });
                }
    
                if (result.length > 0) {
                    return res.status(200).json({
                        status: 'success',
                        data: result
                    });
                } else {
                    return res.status(404).json({ message: 'No dashboard data found for this company' });
                }
            });
    },
     

    getDashboard : (req, res) => {
        const { company_name } = req.body;
        console.log("called getDashboard");
    
        if (!company_name) {
            return res.status(400).json({ message: 'Company name is required' });
        }
    
        const getCompanyIdQuery = `
            SELECT company_id FROM companies 
            WHERE company_name = ?
        `;
    
        db.query(getCompanyIdQuery, [company_name], (err, companyResult) => {
            if (err) {
                console.error('Error fetching company ID:', err);
                return res.status(500).json({ error: 'Database error' });
            }
    
            if (companyResult.length === 0) {
                return res.status(404).json({ message: 'Company not found' });
            }
    
            const companyId = companyResult[0].company_id;
    
            const getDashboardQuery = `
                SELECT 
                    *
                FROM 
                    dashboards d
                LEFT JOIN 
                    dashboard_data dd ON d.dashboard_id = dd.dashboard_id
                WHERE 
                    d.company_id = ?
            `;
    
            db.query(getDashboardQuery, [companyId], (err, result) => {
                if (err) {
                    console.error('Error fetching dashboard data:', err);
                    return res.status(500).json({ error: 'Database error' });
                }
    
                if (result.length > 0) {
                    return res.status(200).json({
                        status: 'success',
                        data: result
                    });
                } else {
                    return res.status(404).json({ message: 'No dashboard data found for this company' });
                }
            });
        });
    },
    
    mailersend: (req, res) => {
            console.log('Mailersend route hit'); 
            const mailerSend = new MailerSend({
                apiKey: process.env.API_KEY,
            });
        
            const sentFrom = new Sender("usha@velastra.co", "usha");
        
            const recipients = [
                new Recipient("ushadevarapalli43@gmail.com", "usha")
            ];
        
            const emailParams = new EmailParams()
                .setFrom(sentFrom)
                .setTo(recipients)
                .setReplyTo(sentFrom)
                .setSubject("Welcome! Your free trial is ready.")
                .setTemplateId('templateId');
        
            mailerSend.email.send(emailParams)
                .then(response => {
                    console.log("Email sent successfully:", response);
                    res.status(200).json({
                        status: 'success',
                        message: 'Email sent successfully',
                        response
                    });
                })
                .catch(error => {
                    console.error("Error sending email:", error);
                    res.status(500).json({
                        status: 'error',
                        message: 'Failed to send email',
                        error: error.message
                    });
                });
        },
    register: (req, res) => {
  const { name, phone_no, email, password, sector_name, company_name } = req.body;
  const randomNumber = generateRandomNumber();
  const access = "in progress";

  if (!name || !email || !password || !phone_no || !sector_name || !company_name) {
    return res.status(400).json({ message: 'All fields are required including sector' });
  }

  const checkQuery = `SELECT * FROM users WHERE phone_no = ? OR email = ?`;
  db.query(checkQuery, [phone_no, email], (err, existingUsers) => {
    if (err) {
      console.error('Error checking existing user:', err);
      return res.status(500).json({ message: 'Database error during duplicate check' });
    }

    if (existingUsers.length > 0) {
      return res.status(409).json({
        message: 'User already registered with this phone number or email'
      });
    }

    // ✅ Match 8 columns with 8 values
    const insertQuery = `
      INSERT INTO users (user_id, name, phone_no, email, password, access, sector_name, company_name)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `;

    db.query(insertQuery, [
      randomNumber,
      name,
      phone_no,
      email,
      password,
      access,
      sector_name,
      company_name
    ], (err, result) => {
      if (err) {
        console.error('Error inserting user:', err);
        return res.status(500).json({ message: 'Database error during insert' });
      }

      // ✅ Send welcome email
      sendMailRegistration(email, name);

      // ✅ Fetch company mail
      const query1 = `SELECT company_mail FROM companies WHERE sector_name = ? AND company_name = ?`;
      db.query(query1, [sector_name, company_name], (err, results) => {
        if (err) {
          console.error("Error fetching company mail:", err);
          return res.status(500).json({ message: "Database error while fetching company email" });
        }

        if (results.length > 0) {
          const companyMail = results[0].company_mail;
          sendMailToCompany(companyMail, { name, email, phone_no, sector_name, company_name });
        }
      });

      return res.status(201).json({
        status: 'success',
        message: 'User registered successfully',
        user_id: randomNumber,
        name,
        email,
        sector_name,
        company_name
      });
    });
  });
},


    signin: (req, res) => {
  const { phone_no, password } = req.body;
  console.log('📥 Request body:', req.body);

  if (!phone_no || !password) {
    console.warn('⚠️ Missing phone_no or password');
    return res.status(400).json({
      message: "Please provide a valid phone number and password or register if you haven't."
    });
  }

  const query = 'SELECT * FROM users WHERE phone_no = ? AND password = ?';
  console.log('➡️ Executing query with:', phone_no, password);

  db.query(query, [phone_no, password], (err, result) => {
    if (err) {
      console.error('❌ Database error:', err);
      return res.status(500).json({ message: 'Database error' });
    }

    console.log('🔎 Query returned rows:', result.length);

    if (result.length > 0) {
      const user = result[0];
      console.log('✅ User found, ID:', user.user_id);
      return res.status(200).json({
        status: 'success',
        message: 'Login successful',
        user: {
          user_id: user.user_id,
          name: user.name,
          phone_no: user.phone_no,
          email: user.email,
          sector_name: user.sector_name,
          company_name: user.company_name,
          access: user.access
        }
      });
    } else {
      console.warn('⚠️ Invalid credentials for phone:', phone_no);
      return res.status(401).json({ message: 'Invalid phone number or password' });
    }
  });
},


    registertest :  (req ,res ) =>{
        const postdata = req.body;
        console.log(postdata);
        const {name , phone_no ,email ,password ,sector_name, company_name} = req.body;
        const randomNumber = generateRandomNumber();
        //const company_id = 1931885
        const access = "in progress"

        if (!name || !email || !password || !phone_no || !sector_name || !company_name)  {
            return res.status(400).json({ error: 'Name, email, and password are required' });
        }
        
        const query = `
        INSERT INTO users (user_id, name, phone_no, email, password,  access, sector_name, company_name) 
        VALUES (?, ?, ?, ?, ?,? ,?,?)`;

        db.query(query, [randomNumber, name, phone_no, email, password,  access, sector_name, company_name] , (err,result) =>{
            if (err) {
                console.error('Error inserting user:', err);
                return res.status(500).json({ error: 'Database error' });
            }else{
                sendMail(email, name);
                return res.status(201).json({
                    //status: 'success',
                    message: 'User registered successfully',
                    user_id: randomNumber,
                    name: name,
                    email: email,
                    sector_name: sector_name,
                    company_name:company_name
                });
            }
        } )
    },
    // ✅ Company-specific dashboard via MariaDB
    
    insertDht: async (req, res) => {
        try {
            const postData = req.body; // Get data from the request body
            const dbcon = await mongodb.connectDB() // Ensure DB is connected
            const collection = dbcon.db("landslides").collection("posts"); // Access the 'posts' collection
            const result = await collection.insertOne(postData); // Insert data into the collection
            console.log(postData);
            res.status(200).json({
                message: 'Data inserted successfully',
                insertedId: result.insertedId // Return the inserted document's ID
            });
        } catch (e) {
            console.error("Error inserting data:", e); // Log the error
            res.status(500).json({
                error: 'An error occurred while inserting data',
                details: e.message // Return the error message to the client
            });
        }
    },


  getDashboard: async (req, res) => {
  console.log("📥 getDashboard received:", req.body);
  return res.json({ status: "ok", sector: req.body.sector, company: req.body.company_name });
},

  
forgotPassword: (req, res) => {
  const { phone_no, new_password } = req.body;

  if (!phone_no || !new_password) {
    return res.status(400).json({ message: 'Phone number and new password are required' });
  }

  const cleanPhone = phone_no.trim();
  console.log('📞 Phone from frontend (cleaned):', cleanPhone);

  // Log all numbers from the database
  db.query('SELECT phone_no FROM users', (err, results) => {
    if (err) {
      console.error('❌ Error fetching phone numbers:', err);
      return res.status(500).json({ message: 'Database error' });
    }
    console.log('📋 All phone numbers in DB:', results.map(r => r.phone_no));

    const checkQuery = `SELECT * FROM users WHERE phone_no = ?`;
    db.query(checkQuery, [cleanPhone], (err, result) => {
      if (err) {
        console.error('❌ Error checking user:', err);
        return res.status(500).json({ message: 'Database error' });
      }

      console.log('🔍 Matching Result:', result);

      if (result.length === 0) {
        console.log('🚫 User not found for phone:', cleanPhone);
        return res.status(404).json({ message: 'User not found' });
      }

      const updateQuery = `UPDATE users SET password = ? WHERE phone_no = ?`;
      db.query(updateQuery, [new_password, cleanPhone], (err, updateResult) => {
        if (err) {
          console.error('❌ Error updating password:', err);
          return res.status(500).json({ message: 'Error updating password' });
        }

        console.log('✅ Password updated for:', cleanPhone);
        return res.status(200).json({ message: 'Password updated successfully' });
      });
    });
  });
}
}