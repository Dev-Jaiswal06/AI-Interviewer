import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { dashboardAPI, interviewAPI } from '../services/api';

const Dashboard = () => {
  const [data, setData] = useState(null);
  const [interviews, setInterviews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [dashRes, intRes] = await Promise.all([
        dashboardAPI.getDashboardData(),
        interviewAPI.getHistory(1)
      ]);
      
      setData(dashRes.data);
      setInterviews(intRes.data.interviews || []);
    } catch (error) {
      console.error('Failed to load dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const getScoreClass = (score) => {
    if (score >= 80) return 'score-excellent';
    if (score >= 60) return 'score-good';
    if (score >= 40) return 'score-average';
    return 'score-poor';
  };

  const getReadinessClass = (level) => {
    switch (level) {
      case 'Excellent': return 'bg-success';
      case 'Good': return 'bg-primary';
      case 'Average': return 'bg-warning';
      default: return 'bg-danger';
    }
  };

  if (loading) {
    return (
      <div className="loading-spinner">
        <div className="spinner-border text-light" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <div className="mb-4">
        <h2 style={{ color: 'white', fontWeight: '600' }}>Your Dashboard</h2>
        <p style={{ color: 'rgba(255,255,255,0.8)' }}>Track your interview preparation progress</p>
      </div>

      <div className="row g-4">
        <div className="col-md-3">
          <div className="stat-card">
            <h3>{data?.total_interviews || 0}</h3>
            <p style={{ color: '#666' }}>Total Interviews</p>
          </div>
        </div>
        
        <div className="col-md-3">
          <div className="stat-card">
            <h3>{data?.total_coding_sessions || 0}</h3>
            <p style={{ color: '#666' }}>Coding Sessions</p>
          </div>
        </div>
        
        <div className="col-md-3">
          <div className="stat-card">
            <h3>{data?.overall_score || 0}%</h3>
            <p style={{ color: '#666' }}>Average Score</p>
          </div>
        </div>
        
        <div className="col-md-3">
          <div className="stat-card">
            <span className={`badge ${getReadinessClass(data?.readiness_level)} mb-2`} style={{ fontSize: '14px', padding: '8px 16px' }}>
              {data?.readiness_level || 'Not Assessed'}
            </span>
            <p style={{ color: '#666', fontSize: '14px' }}>Readiness Level</p>
          </div>
        </div>
      </div>

      <div className="row mt-4 g-4">
        <div className="col-lg-6">
          <div className="dashboard-card">
            <div className="d-flex justify-content-between align-items-center mb-3">
              <h4 style={{ margin: 0 }}>Recent Interviews</h4>
              <Link to="/interview" className="btn btn-sm btn-primary">
                New Interview
              </Link>
            </div>
            
            {interviews.length === 0 ? (
              <div className="text-center py-4" style={{ color: '#999' }}>
                <p>No interviews yet. Start your first interview!</p>
                <Link to="/interview" className="btn btn-outline-primary">
                  Start Interview
                </Link>
              </div>
            ) : (
              <div className="list-group">
                {interviews.slice(0, 5).map((interview) => (
                  <Link 
                    key={interview.id} 
                    to={`/results/${interview.id}`}
                    className="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
                  >
                    <div>
                      <strong>{interview.interview_type?.toUpperCase()}</strong>
                      <br />
                      <small style={{ color: '#666' }}>
                        {new Date(interview.started_at).toLocaleDateString()}
                      </small>
                    </div>
                    <div className={`score-circle ${getScoreClass(interview.overall_score || 0)}`} style={{ width: '60px', height: '60px', fontSize: '18px' }}>
                      {interview.overall_score || 0}%
                    </div>
                  </Link>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="col-lg-6">
          <div className="dashboard-card">
            <h4 className="mb-3">Strengths & Weak Areas</h4>
            
            {data?.strengths?.length > 0 && (
              <div className="mb-4">
                <h6 style={{ color: '#28a745' }}>Strengths</h6>
                <ul className="list-unstyled">
                  {data.strengths.slice(0, 3).map((s, i) => (
                    <li key={i} className="mb-2">
                      <span style={{ color: '#28a745' }}>✓</span> {s.area} - Score: {s.score}%
                    </li>
                  ))}
                </ul>
              </div>
            )}
            
            {data?.weak_areas?.length > 0 && (
              <div>
                <h6 style={{ color: '#dc3545' }}>Areas to Improve</h6>
                <ul className="list-unstyled">
                  {data.weak_areas.slice(0, 3).map((w, i) => (
                    <li key={i} className="mb-2">
                      <span style={{ color: '#dc3545' }}>⚠</span> {w.area} - Score: {w.score}%
                    </li>
                  ))}
                </ul>
              </div>
            )}
            
            {(!data?.strengths?.length && !data?.weak_areas?.length) && (
              <div className="text-center py-4" style={{ color: '#999' }}>
                <p>Complete interviews to see your analysis</p>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="row mt-4">
        <div className="col-12">
          <div className="dashboard-card">
            <h4 className="mb-3">Quick Actions</h4>
            <div className="row g-3">
              <div className="col-md-4">
                <Link to="/interview" className="btn btn-primary w-100 py-3">
                  Start Mock Interview
                </Link>
              </div>
              <div className="col-md-4">
                <Link to="/coding" className="btn btn-outline-primary w-100 py-3">
                  Practice Coding Problems
                </Link>
              </div>
              <div className="col-md-4">
                <button className="btn btn-outline-secondary w-100 py-3" onClick={loadDashboardData}>
                  Refresh Dashboard
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
