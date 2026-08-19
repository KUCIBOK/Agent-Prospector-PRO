import React, { useState, useEffect } from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';

import Dashboard from './pages/Dashboard';
import ProspectsPage from './pages/Prospects';
import MessagesPage from './pages/Messages';
import MonitoringPage from './pages/Monitoring';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/prospects" element={<ProspectsPage />} />
          <Route path="/messages" element={<MessagesPage />} />
          <Route path="/monitoring" element={<MonitoringPage />} />
        </Routes>
      </div>
    </Router>
  );
}

function Header() {
  const location = useLocation();

  return (
    <div className="header">
      <div className="container">
        <h1>🎨 Kucibok Prospector</h1>
        <nav className="nav">
          <Link to="/" className={location.pathname === '/' ? 'active' : ''}>Dashboard</Link>
          <Link to="/prospects" className={location.pathname === '/prospects' ? 'active' : ''}>Prospects</Link>
          <Link to="/messages" className={location.pathname === '/messages' ? 'active' : ''}>Outreach</Link>
          <Link to="/monitoring" className={location.pathname === '/monitoring' ? 'active' : ''}>Monitoring</Link>
        </nav>
      </div>
    </div>
  );
}

export default App;
