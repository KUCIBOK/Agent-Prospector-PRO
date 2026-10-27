import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const client = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    // Note: a key bundled into a browser app is visible to anyone who opens it.
    // Fine for a private deployment; use real user auth before opening it up.
    ...(process.env.REACT_APP_API_KEY ? { 'X-API-Key': process.env.REACT_APP_API_KEY } : {}),
  },
});

export default client;
