import React, { useState, useEffect } from 'react';
import api from '../api/client';

export default function ProspectsPage() {
  const [prospects, setProspects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filters, setFilters] = useState({ type: '', status: '', priority: '' });

  useEffect(() => {
    fetchProspects();
  }, [filters]);

  const fetchProspects = async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (filters.type) params.append('prospect_type', filters.type);
      if (filters.status) params.append('status', filters.status);
      if (filters.priority) params.append('priority', filters.priority);

      const response = await api.get(`/api/prospects?${params}`);
      setProspects(response.data.items || []);
      setError(null);
    } catch (err) {
      setError('Failed to load prospects');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="container"><div className="loading">Loading...</div></div>;

  return (
    <div className="container">
      <h2>Prospects</h2>

      <div className="card">
        <div className="card-title">Filters</div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '10px' }}>
          <select value={filters.type} onChange={(e) => setFilters({ ...filters, type: e.target.value })}>
            <option value="">All Types</option>
            <option value="ARTIST">Artist</option>
            <option value="ART_ADVISOR">Art Advisor</option>
            <option value="CURATOR">Curator</option>
            <option value="GALLERY">Gallery</option>
          </select>
          <select value={filters.status} onChange={(e) => setFilters({ ...filters, status: e.target.value })}>
            <option value="">All Status</option>
            <option value="IDENTIFIED">Identified</option>
            <option value="PREQUALIFIED">Prequalified</option>
            <option value="VERIFIED_KUCIBOK">Verified</option>
          </select>
          <select value={filters.priority} onChange={(e) => setFilters({ ...filters, priority: e.target.value })}>
            <option value="">All Priority</option>
            <option value="P1">P1</option>
            <option value="P2">P2</option>
            <option value="P3">P3</option>
            <option value="P4">P4</option>
          </select>
        </div>
      </div>

      {error && <div className="error">{error}</div>}

      <div className="card">
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Country</th>
                <th>Status</th>
                <th>Score</th>
                <th>Priority</th>
              </tr>
            </thead>
            <tbody>
              {prospects.map((prospect) => (
                <tr key={prospect.id}>
                  <td><strong>{prospect.name}</strong></td>
                  <td><span className="badge badge-info">{prospect.type}</span></td>
                  <td>{prospect.country}</td>
                  <td><span className="badge badge-success">{prospect.status}</span></td>
                  <td>{prospect.score.toFixed(1)}/100</td>
                  <td><span className="badge badge-warning">{prospect.priority || '—'}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
