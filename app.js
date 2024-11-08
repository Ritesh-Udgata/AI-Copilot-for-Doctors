// app.js
const express = require('express');
const session = require('express-session');
const bcrypt = require('bcrypt');
const passport = require('passport');
const LocalStrategy = require('passport-local').Strategy;
const GoogleStrategy = require('passport-google-oauth20').Strategy;
const fs = require('fs');
const app = express();
const pg = require("pg");
const env = require("dotenv")

// Load credentials from file
let users = require('./credentials.json');
env.config();

const db = new pg.Client({
  user: process.env.PG_USER,
  host: process.env.PG_HOST,
  database: process.env.PG_DATABASE,
  password: process.env.PG_PASSWORD,
  port: process.env.PG_PORT,
});
db.connect();

app.set('view engine', 'ejs');
app.use(express.static('public'));
app.use(express.json({ limit: '100000mb' })); 
app.use(express.urlencoded({ extended: true }));

// Session setup
app.use(
    session({
      secret: 'secret-key', // Your secret key
      resave: false,
      saveUninitialized: true,
      cookie: {
        maxAge: 24 * 60 * 60 * 1000, // 24 hours in milliseconds
      },
    })
  );
  

// Initialize Passport
app.use(passport.initialize());
app.use(passport.session());

// Local Strategy for login
passport.use(
  new LocalStrategy(async (username, password, done) => {
    const user = users.find((u) => u.username === username);
    if (!user) return done(null, false, { message: 'Incorrect username.' });

    const validPassword = await bcrypt.compare(password, user.password);
    if (!validPassword) return done(null, false, { message: 'Incorrect password.' });

    return done(null, user);
  })
);

// Google OAuth Strategy
passport.use(
  new GoogleStrategy(
    {
      clientID: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
      callbackURL: '/auth/google/callback'
    },
    async (accessToken, refreshToken, profile, done) => {
      let user = users.find((u) => u.username === profile.emails[0].value);
      if (!user) {
        // Register new Google user
        const newUser = { username: profile.emails[0].value, password: await bcrypt.hash('google', 10) };
        users.push(newUser);
        fs.writeFileSync('credentials.json', JSON.stringify(users, null, 2));
        user = newUser;
      }
      return done(null, user);
    }
  )
);

// Passport session management
passport.serializeUser((user, done) => done(null, user.username));
passport.deserializeUser((username, done) => {
  const user = users.find((u) => u.username === username);
  done(null, user);
});

// Routes
app.get('/', (req, res) => res.render('login'));
app.get('/signup', (req, res) => res.render('signup'));

app.post('/signup', async (req, res) => {
  const { username, password } = req.body;
  if (users.find((u) => u.username === username)) {
    return res.redirect('/signup');
  }

  const hashedPassword = await bcrypt.hash(password, 10);
  const newUser = { username, password: hashedPassword };
  users.push(newUser);

  // Save new user to file
  fs.writeFileSync('credentials.json', JSON.stringify(users, null, 2));
  res.redirect('/');
});

app.post(
  '/login',
  passport.authenticate('local', {
    successRedirect: '/dashboard',
    failureRedirect: '/'
  })
);

app.get('/auth/google', passport.authenticate('google', { scope: ['profile', 'email'] }));
app.get(
  '/auth/google/callback',
  passport.authenticate('google', {
    successRedirect: '/dashboard',
    failureRedirect: '/'
  })
);

app.get('/dashboard', async(req, res) => {
    if (!req.isAuthenticated()) return res.redirect('/');
    const drug = await db.query("SELECT drugs FROM pDrug");
    const disease = await db.query("SELECT diseases FROM pDisease");
    
    const sideeffect = await db.query("SELECT sideeffects FROM pSideEffect");
  
    // Sample predictions data
    const predictions = {
      diseases:disease.rows.map(row => row.diseases),
      drugs: drug.rows.map(rowdrug => rowdrug.drugs),
      sideEffects: sideeffect.rows.map(rowse => rowse.sideeffects),
      alternatives: ["Alternative A", "Alternative B", "Alternative C"],
      historyInteractions: ["Drug1", "Drug2", "Drug3", "Drug4"]
    };
  console.log(sideeffect.rows.map(row => row.sideeffect))
    res.render('index', { predictions });
  });
  
  app.get('/database-overhaul', async (req, res) => {
    try {
       // PostgreSQL client
      const tables = await db.query(`
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema='public' AND table_type='BASE TABLE';
      `);
      
      const tableData = await Promise.all(
        tables.rows.map(async (table) => {
          const data = await db.query(`SELECT * FROM ${table.table_name} LIMIT 5`);
          return { name: table.table_name, data: data.rows };
        })
      );
  
      
      res.render('database-overhaul', { tables: tableData });
    } catch (err) {
      console.error(err);
      res.redirect('/dashboard');
    }
  });

  app.get('/database-overhaul/:table', async (req, res) => {
    const tableName = req.params.table;
  
    try {
      
      const data = await db.query(`SELECT * FROM ${tableName}`);
      
      res.render('edit-table', { tableName, data: data.rows });
    } catch (err) {
      console.error(err);
      res.redirect('/database-overhaul');
    }
  });

  app.post('/database-overhaul/:table/update', async (req, res) => {
    const tableName = req.params.table;
    const updatedData = req.body.data; // Accessed as a nested object of rows and columns
  
    try {
      
  
      for (const rowIndex in updatedData) {
        const row = updatedData[rowIndex];
        const updates = Object.keys(row).map(key => `${key} = '${row[key]}'`).join(', ');
  
        await db.query(`UPDATE ${tableName} SET ${updates} WHERE id = ${row.id}`);
      }
  
      
      res.redirect(`/database-overhaul/${tableName}`);
    } catch (err) {
      console.error(err);
      res.redirect(`/database-overhaul/${tableName}`);
    }
  });
  
  
  

app.get('/logout', (req, res) => {
  req.logout();
  res.redirect('/');
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`));
