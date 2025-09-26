import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://asj234.pythonanywhere.com/api';

function App() {
  const [activeTab, setActiveTab] = useState('process');
  const [report, setReport] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [history, setHistory] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [translation, setTranslation] = useState(null);
  const [translationLoading, setTranslationLoading] = useState(false);

  // Sample data for demonstration
  const sampleReport = "Patient experienced severe nausea and headache after taking Drug X. Patient recovered.";

  useEffect(() => {
    fetchHistory();
    fetchAnalytics();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/reports/`);
      setHistory(response.data.reports || []);
    } catch (err) {
      console.error('Error fetching history:', err);
    }
  };

  const fetchAnalytics = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/analytics/`);
      setAnalytics(response.data);
    } catch (err) {
      console.error('Error fetching analytics:', err);
    }
  };

  const processReport = async () => {
    if (!report.trim()) {
      setError('Please enter a medical report');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post(`${API_BASE_URL}/process-report/`, {
        report: report
      });
      setResult(response.data);
      fetchHistory(); // Refresh history
      fetchAnalytics(); // Refresh analytics
    } catch (err) {
      setError(err.response?.data?.error || err.response?.data?.detail || 'Error processing report');
    } finally {
      setLoading(false);
    }
  };

  const translateText = async (text, language) => {
    setTranslationLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/translate/`, {
        text: text,
        target_language: language
      });
      setTranslation(response.data);
    } catch (err) {
      setError(err.response?.data?.error || err.response?.data?.detail || 'Error translating text');
    } finally {
      setTranslationLoading(false);
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'severe': return '#dc2626';
      case 'moderate': return '#d97706';
      case 'mild': return '#059669';
      default: return '#6b7280';
    }
  };

  const getOutcomeColor = (outcome) => {
    switch (outcome) {
      case 'recovered': return '#059669';
      case 'ongoing': return '#d97706';
      case 'fatal': return '#dc2626';
      default: return '#6b7280';
    }
  };

  // Prepare chart data
  const severityData = analytics?.severity_distribution ? 
    Object.entries(analytics.severity_distribution).map(([key, value]) => ({
      name: key.charAt(0).toUpperCase() + key.slice(1),
      value: value,
      color: getSeverityColor(key)
    })) : [];

  const outcomeData = analytics?.outcome_distribution ? 
    Object.entries(analytics.outcome_distribution).map(([key, value]) => ({
      name: key.charAt(0).toUpperCase() + key.slice(1),
      value: value,
      color: getOutcomeColor(key)
    })) : [];

  return (
    <div className="App">
      <header className="header">
        <div className="container">
          <h1>Regulatory Report Assistant</h1>
          <p>AI-powered adverse event report processing for Feyti Medical Group</p>
        </div>
      </header>

      <div className="container">
        <div className="tabs">
          <button 
            className={`tab ${activeTab === 'process' ? 'active' : ''}`}
            onClick={() => setActiveTab('process')}
          >
            Process Report
          </button>
          <button 
            className={`tab ${activeTab === 'history' ? 'active' : ''}`}
            onClick={() => setActiveTab('history')}
          >
            History
          </button>
          <button 
            className={`tab ${activeTab === 'analytics' ? 'active' : ''}`}
            onClick={() => setActiveTab('analytics')}
          >
            Analytics
          </button>
        </div>

        {activeTab === 'process' && (
          <div className="card">
            <h2>Process Medical Report</h2>
            <div className="form-group">
              <label htmlFor="report">Medical Report:</label>
              <textarea
                id="report"
                value={report}
                onChange={(e) => setReport(e.target.value)}
                placeholder="Enter the medical report here... (e.g., Patient experienced severe nausea and headache after taking Drug X. Patient recovered.)"
              />
            </div>
            
            <div style={{ marginBottom: '16px' }}>
              <button 
                className="btn btn-secondary"
                onClick={() => setReport(sampleReport)}
              >
                Load Sample Report
              </button>
            </div>

            <button 
              className="btn"
              onClick={processReport}
              disabled={loading}
            >
              {loading ? 'Processing...' : 'Process Report'}
            </button>

            {error && <div className="error">{error}</div>}

            {result && (
              <div>
                <div className="success">
                  Report processed successfully!
                </div>
                
                <div className="results-grid">
                  <div className="result-card">
                    <h3>Drug</h3>
                    <p>{result.drug}</p>
                  </div>
                  
                  <div className="result-card">
                    <h3>Adverse Events</h3>
                    <div className="adverse-events">
                      {result.adverse_events.map((event, index) => (
                        <span key={index} className="adverse-event-tag">
                          {event}
                        </span>
                      ))}
                    </div>
                  </div>
                  
                  <div className="result-card">
                    <h3>Severity</h3>
                    <p className={`severity-${result.severity}`}>
                      {result.severity}
                    </p>
                  </div>
                  
                  <div className="result-card">
                    <h3>Outcome</h3>
                    <p className={`outcome-${result.outcome}`}>
                      {result.outcome}
                    </p>
                  </div>
                </div>

                <div style={{ marginTop: '24px' }}>
                  <h3>Translation</h3>
                  <button 
                    className="btn btn-success"
                    onClick={() => translateText(result.outcome, 'french')}
                    disabled={translationLoading}
                  >
                    Translate to French
                  </button>
                  <button 
                    className="btn btn-success"
                    onClick={() => translateText(result.outcome, 'swahili')}
                    disabled={translationLoading}
                  >
                    Translate to Swahili
                  </button>
                  
                  {translation && (
                    <div style={{ marginTop: '16px', padding: '12px', backgroundColor: '#f0fdf4', borderRadius: '8px' }}>
                      <strong>Translation:</strong> {translation.translated_text}
                      <br />
                      <small>Language: {translation.target_language}</small>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'history' && (
          <div className="card">
            <h2>Report History</h2>
            {history.length === 0 ? (
              <p>No reports processed yet.</p>
            ) : (
              <div>
                {history.map((item) => (
                  <div key={item.id} className="history-item">
                    <h4>Report #{item.id}</h4>
                    <p><strong>Drug:</strong> {item.drug}</p>
                    <p><strong>Adverse Events:</strong> {item.adverse_events.join(', ')}</p>
                    <p><strong>Severity:</strong> <span className={`severity-${item.severity}`}>{item.severity}</span></p>
                    <p><strong>Outcome:</strong> <span className={`outcome-${item.outcome}`}>{item.outcome}</span></p>
                    <div className="history-meta">
                      Processed: {new Date(item.created_at).toLocaleString()}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'analytics' && (
          <div>
            {analytics && (
              <div className="analytics-grid">
                <div className="analytics-card">
                  <h4>Total Reports</h4>
                  <p style={{ fontSize: '24px', fontWeight: 'bold', color: '#3b82f6' }}>
                    {analytics.total_reports}
                  </p>
                </div>
                
                <div className="analytics-card">
                  <h4>Most Common Drugs</h4>
                  {Object.entries(analytics.common_drugs || {}).slice(0, 5).map(([drug, count]) => (
                    <p key={drug}>{drug}: {count}</p>
                  ))}
                </div>
                
                <div className="analytics-card">
                  <h4>Most Common Adverse Events</h4>
                  {Object.entries(analytics.common_adverse_events || {}).slice(0, 5).map(([event, count]) => (
                    <p key={event}>{event}: {count}</p>
                  ))}
                </div>
              </div>
            )}

            {severityData.length > 0 && (
              <div className="chart-container">
                <h3 className="chart-title">Severity Distribution</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={severityData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {severityData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            )}

            {outcomeData.length > 0 && (
              <div className="chart-container">
                <h3 className="chart-title">Outcome Distribution</h3>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={outcomeData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="value" fill="#3b82f6" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;