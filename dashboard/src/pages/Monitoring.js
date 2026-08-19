import React, { useState, useEffect } from 'react';
import api from '../api/client';

export default function MonitoringPage() {
  const [jobs, setJobs] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchMonitoring();
  }, []);

  const fetchMonitoring = async () => {
    try {
      setLoading(true);
      const [jobsRes, statsRes] = await Promise.all([
        api.get('/api/monitoring/jobs'),
        api.get('/api/monitoring/prospects/stats'),
      ]);
      setJobs(jobsRes.data.items || []);
      setStats(statsRes.data);
      setError(null);
    } catch (err) {
      setError('Failed to load monitoring data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="container"><div className="loading">Loading...</div></div>;

  return (
    <div className="container">
      <h2>System Monitoring</h2>

      {stats && (
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-label">Total Prospects</div>
            <div className="stat-value">{stats.total}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Artists</div>
            <div className="stat-value">{stats.by_type?.artists || 0}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Advisors</div>
            <div className="stat-value">{stats.by_type?.advisors || 0}</div>
          </div>
          <div className="stat-card">
            <div className="stat-label">Curators</div>
            <div className="stat-value">{stats.by_type?.curators || 0}</div>
          </div>
        </div>
      )}

      <div className="card">
        <div className="card-title">Recent Jobs</div>
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Job ID</th>
                <th>Type</th>
                <th>Status</th>
                <th>Results</th>
                <th>Attempts</th>
                <th>Started</th>
              </tr>
            </thead>
            <tbody>
              {jobs.map((job) => (
                <tr key={job.id}>
                  <td>#{job.id}</td>
                  <td>{job.job_type}</td>
                  <td>
                    <span className={`badge badge-${job.status === 'SUCCESS' ? 'success' : job.status === 'FAILED' ? 'danger' : 'warning'}`}>
                      {job.status}
                    </span>
                  </td>
                  <td>{job.result_count}</td>
                  <td>{job.attempts}/3</td>
                  <td>{new Date(job.started_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
