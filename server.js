// server.js
const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));

// Connect to MongoDB
const uri = 'YOUR_MONGODB_CONNECTION_STRING'; // Replace with your MongoDB connection string
mongoose.connect(uri, { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log('MongoDB connected'))
    .catch(err => console.error(err));

// Define User schema
const userSchema = new mongoose.Schema({
    name: String,
    email: String,
    phone: String,
    address: String,
    message: String
});

// Create User model
const User = mongoose.model('User', userSchema);

// Handle form submission
app.post('/submit', (req, res) => {
    const newUser = new User(req.body);
    newUser.save()
        .then(() => res.send('User details saved successfully!'))
        .catch(err => res.status(400).send('Error saving user details: ' + err));
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
