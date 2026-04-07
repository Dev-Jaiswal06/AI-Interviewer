import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { interviewAPI, evaluationAPI } from '../services/api';

const InterviewResults = () => {
  const { id } = useParams();
  const [data, setData] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    loadResults();
  }, [id]);

  const loadResults = async () => {
    try {
      const [intRes, anaRes] = await Promise.all([
        interviewAPI.getInterview(id),
        evaluationAPI.getAnalysis(id)
      ]);
      
      setData(intRes.data);
      setAnalysis(anaRes.data.analysis);
    } catch (error) {
      console.error('Failed to load results:', error);
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

  const getScoreColor = (score) => {
    if (score >= 80) return '#667eea';
    if (score >= 60) return '#28a745';
    if (score >= 40) return '#ffc107';
    return '#dc3545';
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

  if (!data) {
    return (
      <div className="interview-container">
        <div className="alert alert-danger">Failed to load results</div>
      </div>
    );
  }

  return (
    <div className="interview-container">
      <div className="dashboard-card mb-4">
        <div className="text-center">
          <h2>Interview Results</h2>
          <p className="text-muted">
            {data.interview?.interview_type?.toUpperCase()} Interview - 
            {new Date(data.interview?.started_at).toLocaleDateString()}
          </p>
        </div>
        
        <div className="row mt-4">
          <div className="col-md-4">
            <div className={`score-circle ${getScoreClass(data.interview?.overall_score || 0)}`}>
              {data.interview?.overall_score || 0}%
            </div>
            <h4 className="mt-3">Overall Score</h4>
            <p className="text-muted">{analysis?.readiness_level || 'Assessed'}</p>
          </div>
          <div className="col-md-8">
            <div className="row g-3">
              {analysis?.section_scores && Object.entries(analysis.section_scores).map(([section, info]) => (
                <div className="col-4" key={section}>
                  <div className="p-3 border rounded text-center">
                    <h5>{info.average?.toFixed(1) || 0}%</h5>
                    <small className="text-capitalize">{section.replace('_', ' ')}</small>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      <ul className="nav nav-tabs mb-3">
        <li className="nav-item">
          <button 
            className={`nav-link ${activeTab === 'overview' ? 'active' : ''}`}
            onClick={() => setActiveTab('overview')}
          >
            Overview
          </button>
        </li>
        <li className="nav-item">
          <button 
            className={`nav-link ${activeTab === 'strengths' ? 'active' : ''}`}
            onClick={() => setActiveTab('strengths')}
          >
            Strengths
          </button>
        </li>
        <li className="nav-item">
          <button 
            className={`nav-link ${activeTab === 'weaknesses' ? 'active' : ''}`}
            onClick={() => setActiveTab('weaknesses')}
          >
            Weak Areas
          </button>
        </li>
        <li className="nav-item">
          <button 
            className={`nav-link ${activeTab === 'answers' ? 'active' : ''}`}
            onClick={() => setActiveTab('answers')}
          >
            Your Answers
          </button>
        </li>
      </ul>

      <div className="dashboard-card">
        {activeTab === 'overview' && (
          <div>
            <h4>Performance Summary</h4>
            <div className="alert alert-info mt-3">
              <p><strong>Interview Type:</strong> {data.interview?.interview_type?.toUpperCase()}</p>
              <p><strong>Questions Attempted:</strong> {Object.keys(data.answers || {}).length}</p>
              <p><strong>Overall Readiness:</strong> {analysis?.readiness_level || 'Assessed'}</p>
            </div>
            
            <h5 className="mt-4">Section-wise Performance</h5>
            {analysis?.section_scores && Object.entries(analysis.section_scores).map(([section, info]) => (
              <div key={section} className="mb-3">
                <div className="d-flex justify-content-between mb-1">
                  <span className="text-capitalize">{section.replace('_', ' ')}</span>
                  <span>{info.average?.toFixed(1) || 0}%</span>
                </div>
                <div className="progress" style={{ height: '10px' }}>
                  <div 
                    className="progress-bar" 
                    style={{ 
                      width: `${info.average || 0}%`,
                      backgroundColor: getScoreColor(info.average || 0)
                    }}
                  />
                </div>
              </div>
            ))}
          </div>
        )}

        {activeTab === 'strengths' && (
          <div>
            <h4>Your Strengths</h4>
            {analysis?.strengths?.length > 0 ? (
              <div className="list-group mt-3">
                {analysis.strengths.map((s, i) => (
                  <div key={i} className="list-group-item list-group-item-success">
                    <div className="d-flex justify-content-between">
                      <span>Question {i + 1}</span>
                      <strong>{s.score}%</strong>
                    </div>
                    <small>Similarity: {s.similarity}%</small>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-muted mt-3">Complete more interviews to identify strengths</p>
            )}
          </div>
        )}

        {activeTab === 'weaknesses' && (
          <div>
            <h4>Areas to Improve</h4>
            {analysis?.weak_areas?.length > 0 ? (
              <div className="list-group mt-3">
                {analysis.weak_areas.map((w, i) => (
                  <div key={i} className="list-group-item list-group-item-danger">
                    <div className="d-flex justify-content-between">
                      <span>Question {i + 1}</span>
                      <strong>{w.score}%</strong>
                    </div>
                    <small>{w.feedback}</small>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-muted mt-3">Great job! No major weak areas detected.</p>
            )}
            
            {analysis?.weak_areas?.length > 0 && (
              <div className="alert alert-warning mt-3">
                <h6>Recommendations:</h6>
                <ul className="mb-0">
                  <li>Review the questions where you scored below 50%</li>
                  <li>Practice similar questions in our question bank</li>
                  <li>Focus on technical fundamentals</li>
                </ul>
              </div>
            )}
          </div>
        )}

        {activeTab === 'answers' && (
          <div>
            <h4>Your Answers & Feedback</h4>
            {analysis?.detailed_analysis?.map((item, i) => (
              <div key={i} className="card mb-3">
                <div className="card-body">
                  <h6>Q{ i + 1}: {item.question}</h6>
                  <div className="alert alert-secondary mt-2">
                    <strong>Your Answer:</strong>
                    <p className="mb-0">{item.your_answer || 'Not answered'}</p>
                  </div>
                  {item.ideal_answer && (
                    <div className="alert alert-info mt-2">
                      <strong>Ideal Answer:</strong>
                      <p className="mb-0">{item.ideal_answer}</p>
                    </div>
                  )}
                  <div className="mt-2">
                    <span className={`badge ${item.score >= 70 ? 'bg-success' : item.score >= 50 ? 'bg-warning' : 'bg-danger'}`}>
                      Score: {item.score}%
                    </span>
                  </div>
                  {item.feedback && (
                    <p className="mt-2 mb-0"><em>{item.feedback}</em></p>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="text-center mt-4">
        <Link to="/interview" className="btn btn-primary me-2">
          Take Another Interview
        </Link>
        <Link to="/coding" className="btn btn-outline-primary me-2">
          Practice Coding
        </Link>
        <Link to="/" className="btn btn-outline-secondary">
          Back to Dashboard
        </Link>
      </div>
    </div>
  );
};

export default InterviewResults;
