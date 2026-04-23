const express = require('express');
const axios = require('axios');
const path = require('path');
const app = express();

// Bug Fix: Use environment variables for the API URL
const API_URL = process.env.API_URL || "http://api:8000";

app.use(express.json());
app.use(express.static(path.join(__dirname, 'views')));

app.post('/submit', async (req, res) => {
  try {
    const response = await axios.post(`${API_URL}/jobs`);
    res.json(response.data);
  } catch (err) {
    // Bug Fix: Log error for better debugging
    console.error("API Connection Error:", err.message);
    res.status(500).json({ error: "Could not connect to API" });
  }
});

app.get('/status/:id', async (req, res) => {
  try {
    const response = await axios.get(`${API_URL}/jobs/${req.params.id}`);
    res.json(response.data);
  } catch (err) {
    console.error("API Connection Error:", err.message);
    res.status(500).json({ error: "Could not fetch job status" });
  }
});

// Bug Fix: Use environment variable for PORT
const PORT = process.env.PORT || 3000;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Frontend running on port ${PORT}`);
});
