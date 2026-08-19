import React, { useState, useEffect } from 'react';
import api from '../api/client';

export default function MessagesPage() {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchMessages();
  }, []);

  const fetchMessages = async () => {
    try {
      setLoading(true);
      const response = await api.get('/api/messages');
      setMessages(response.data.items || []);
      setError(null);
    } catch (err) {
      setError('Failed to load messages');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="container"><div className="loading">Loading...</div></div>;

  return (
    <div className="container">
      <h2>Outreach Queue</h2>

      <div className="card">
        <div className="card-title">LinkedIn Messages (Ready to Send)</div>
        <div style={{ marginBottom: '20px', fontSize: '14px', color: '#666' }}>
          Total: {messages.length} messages ready for manual send
        </div>
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Prospect</th>
                <th>Persona</th>
                <th>Message</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {messages.map((msg) => (
                <tr key={msg.id}>
                  <td><strong>{msg.prospect_id}</strong></td>
                  <td><span className="badge badge-info">{msg.persona}</span></td>
                  <td style={{ maxWidth: '300px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {msg.content}
                  </td>
                  <td><span className="badge badge-success">{msg.status}</span></td>
                  <td>
                    <button className="btn btn-sm">Copy & Send</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
