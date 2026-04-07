import React, { useState, useEffect } from 'react';
import { codingAPI } from '../services/api';

const Coding = () => {
  const [problems, setProblems] = useState([]);
  const [selectedProblem, setSelectedProblem] = useState(null);
  const [code, setCode] = useState('');
  const [language, setLanguage] = useState('python');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [difficulty, setDifficulty] = useState('');

  useEffect(() => {
    loadProblems();
  }, [difficulty]);

  const loadProblems = async () => {
    try {
      const response = await codingAPI.getProblems(difficulty);
      setProblems(response.data.problems || []);
    } catch (error) {
      console.error('Failed to load problems:', error);
      setProblems([]);
    }
  };

  const selectProblem = (problem) => {
    setSelectedProblem(problem);
    setCode(problem.starter_code || '');
    setResult(null);
  };

  const handleSubmit = async () => {
    setLoading(true);
    setResult(null);
    
    try {
      const response = await codingAPI.submitCode({
        problem_id: selectedProblem.id,
        code: code,
        language: language
      });
      setResult(response.data.result);
    } catch (error) {
      setResult({
        error: error.response?.data?.error || 'Failed to submit code',
        score: 0
      });
    } finally {
      setLoading(false);
    }
  };

  const handleTest = async () => {
    setLoading(true);
    setResult(null);
    
    try {
      const response = await codingAPI.testCode({
        code: code,
        language: language,
        stdin: ''
      });
      setResult(response.data.result);
    } catch (error) {
      setResult({
        error: error.response?.data?.error || 'Failed to test code'
      });
    } finally {
      setLoading(false);
    }
  };

  const getDifficultyBadge = (diff) => {
    const badges = {
      easy: 'badge-easy',
      medium: 'badge-medium',
      hard: 'badge-hard'
    };
    return badges[diff] || 'badge-medium';
  };

  return (
    <div className="dashboard-container">
      <div className="mb-4">
        <h2 style={{ color: 'white', fontWeight: '600' }}>Coding Practice</h2>
        <p style={{ color: 'rgba(255,255,255,0.8)' }}>Practice coding problems and improve your problem-solving skills</p>
      </div>

      <div className="row">
        <div className="col-lg-4">
          <div className="dashboard-card">
            <div className="d-flex justify-content-between align-items-center mb-3">
              <h4 style={{ margin: 0 }}>Problems</h4>
              <select 
                className="form-select form-select-sm" 
                style={{ width: 'auto' }}
                value={difficulty}
                onChange={(e) => setDifficulty(e.target.value)}
              >
                <option value="">All</option>
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
              </select>
            </div>
            
            <div className="list-group">
              {problems.length === 0 ? (
                <p className="text-muted p-3">No problems available</p>
              ) : (
                problems.map((problem) => (
                  <button
                    key={problem.id}
                    className={`list-group-item list-group-item-action ${selectedProblem?.id === problem.id ? 'active' : ''}`}
                    onClick={() => selectProblem(problem)}
                  >
                    <div className="d-flex justify-content-between align-items-center">
                      <span className="fw-bold">{problem.title}</span>
                      <span className={`badge badge-custom ${getDifficultyBadge(problem.difficulty)}`}>
                        {problem.difficulty}
                      </span>
                    </div>
                    <small className="text-muted">
                      {problem.problem_type} • {problem.points} points
                    </small>
                  </button>
                ))
              )}
            </div>
          </div>
        </div>

        <div className="col-lg-8">
          {selectedProblem ? (
            <div className="dashboard-card">
              <div className="d-flex justify-content-between align-items-start mb-3">
                <div>
                  <h4>{selectedProblem.title}</h4>
                  <span className={`badge badge-custom ${getDifficultyBadge(selectedProblem.difficulty)}`}>
                    {selectedProblem.difficulty}
                  </span>
                </div>
                <select 
                  className="form-select" 
                  style={{ width: 'auto' }}
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                >
                  <option value="python">Python</option>
                  <option value="javascript">JavaScript</option>
                  <option value="java">Java</option>
                  <option value="cpp">C++</option>
                </select>
              </div>

              <div className="mb-4">
                <h6>Problem Description:</h6>
                <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit', background: '#f8f9fa', padding: '15px', borderRadius: '8px' }}>
                  {selectedProblem.description}
                </pre>
              </div>

              {selectedProblem.hints && (
                <details className="mb-4">
                  <summary style={{ cursor: 'pointer', color: '#667eea' }}>
                    Show Hints
                  </summary>
                  <div className="alert alert-warning mt-2">
                    {selectedProblem.hints}
                  </div>
                </details>
              )}

              <div className="mb-3">
                <label className="form-label fw-bold">Your Code:</label>
                <textarea
                  className="code-editor"
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  placeholder="Write your code here..."
                />
              </div>

              <div className="d-flex gap-2 mb-3">
                <button 
                  className="btn btn-outline-primary"
                  onClick={handleTest}
                  disabled={loading}
                >
                  Test Code
                </button>
                <button 
                  className="btn btn-success"
                  onClick={handleSubmit}
                  disabled={loading}
                >
                  {loading ? 'Submitting...' : 'Submit Solution'}
                </button>
              </div>

              {result && (
                <div className={`alert ${result.error ? 'alert-danger' : result.score >= 70 ? 'alert-success' : 'alert-warning'}`}>
                  <h5>Results:</h5>
                  {result.error ? (
                    <p className="mb-0">{result.error}</p>
                  ) : (
                    <>
                      <p className="mb-1">
                        <strong>Score:</strong> {result.score || 0}%
                      </p>
                      <p className="mb-1">
                        <strong>Test Cases Passed:</strong> {result.test_cases_passed || 0} / {result.total_test_cases || 0}
                      </p>
                      {result.stdout && (
                        <div className="mt-2">
                          <strong>Output:</strong>
                          <pre style={{ background: '#f8f9fa', padding: '10px', borderRadius: '5px', marginTop: '5px' }}>
                            {result.stdout}
                          </pre>
                        </div>
                      )}
                      {result.note && (
                        <small className="text-muted">{result.note}</small>
                      )}
                    </>
                  )}
                </div>
              )}
            </div>
          ) : (
            <div className="dashboard-card text-center py-5">
              <h5 className="text-muted">Select a problem to start coding</h5>
              <p className="text-muted">Choose from the list on the left</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Coding;
