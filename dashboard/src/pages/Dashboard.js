import React, { useState, useEffect } from 'react';
import api from '../api/client';

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [autoRefreshEnabled, setAutoRefreshEnabled] = useState(true);

  // IMPROVEMENT #1: Auto-refresh every 10 seconds
  useEffect(() => {
    fetchData();

    if (!autoRefreshEnabled) return;

    const interval = setInterval(() => {
      fetchData();
    }, 10000); // Refresh every 10 seconds

    return () => clearInterval(interval);
  }, [autoRefreshEnabled]);

  const fetchData = async () => {
    try {
      const response = await api.get('/api/monitoring/summary');
      setData(response.data);
      setError(null);
      setLastUpdated(new Date().toLocaleTimeString());
      setLoading(false);
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error(err);
      setLoading(false);
    }
  };

  if (loading && !data) return <div className="container"><div className="loading">Loading...</div></div>;
  if (error && !data) return <div className="container"><div className="error">{error}</div></div>;
  if (!data) return <div className="container"><div className="loading">No data</div></div>;

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h2>Dashboard</h2>
        <div style={{ fontSize: '12px', color: '#999' }}>
          {lastUpdated && <span>Last updated: {lastUpdated} | </span>}
          <button
            onClick={() => setAutoRefreshEnabled(!autoRefreshEnabled)}
            style={{
              padding: '5px 10px',
              border: '1px solid #ddd',
              borderRadius: '4px',
              cursor: 'pointer',
              background: autoRefreshEnabled ? '#4CAF50' : '#f44336',
              color: 'white',
              fontSize: '12px'
            }}
          >
            {autoRefreshEnabled ? '🔄 Auto-refresh ON' : '⏸️ Auto-refresh OFF'}
          </button>
        </div>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-label">Total Prospects</div>
          <div className="stat-value">{data.prospects?.total || 0}</div>
          <div style={{ fontSize: '12px', color: '#999', marginTop: '10px' }}>
            {data.prospects?.artists || 0} Artists, {data.prospects?.clients || 0} Clients
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Outreach Messages</div>
          <div className="stat-value">{data.messages?.total || 0}</div>
          <div style={{ fontSize: '12px', color: '#999', marginTop: '10px' }}>
            {data.messages?.draft || 0} Draft, {data.messages?.sent || 0} Sent
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Intent Signals (7d)</div>
          <div className="stat-value" style={{ color: '#4CAF50' }}>{data.signals?.recent || 0}</div>
          <div style={{ fontSize: '12px', color: '#999', marginTop: '10px' }}>
            Recent opportunities detected
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Jobs</div>
          <div className="stat-value">{data.jobs?.total || 0}</div>
          <div style={{ fontSize: '12px', color: '#999', marginTop: '10px' }}>
            {data.jobs?.failed || 0} Failed
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Uptime</div>
          <div className="stat-value">
            {Math.floor((data.uptime_seconds || 0) / 3600)}h
          </div>
        </div>
      </div>

      <div className="card">
        <div className="card-title">Quick Actions</div>
        <div style={{ display: 'flex', gap: '10px' }}>
          <button className="btn btn-sm">Run Discovery</button>
          <button className="btn btn-sm">Run Scoring</button>
          <button className="btn btn-sm">Generate Outreach</button>
        </div>
      </div>
    </div>
  );
}
