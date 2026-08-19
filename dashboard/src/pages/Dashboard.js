import React, { useState, useEffect } from 'react';
import api from '../api/client';

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const response = await api.get('/api/monitoring/summary');
      setData(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="container"><div className="loading">Loading...</div></div>;
  if (error) return <div className="container"><div className="error">{error}</div></div>;
  if (!data) return <div className="container"><div className="loading">No data</div></div>;

  return (
    <div className="container">
      <h2>Dashboard</h2>

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
