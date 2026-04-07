import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { interviewAPI } from '../services/api';

const Interview = () => {
  const [step, setStep] = useState(1);
  const [config, setConfig] = useState({
    interview_type: 'mixed',
    has_resume: false,
    resume_file: null
  });
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(false);
  const [interviewId, setInterviewId] = useState(null);
  const [voiceActive, setVoiceActive] = useState(false);
  const navigate = useNavigate();

  const handleStartInterview = async () => {
    setLoading(true);
    try {
      const response = await interviewAPI.startInterview(config);
      setInterviewId(response.data.interview_id);
      setQuestions(response.data.questions);
      setStep(2);
    } catch (error) {
      alert('Failed to start interview: ' + (error.response?.data?.error || error.message));
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerChange = (questionId, answer) => {
    setAnswers({ ...answers, [questionId]: answer });
  };

  const handleNextQuestion = async () => {
    const question = questions[currentQuestion];
    
    try {
      await interviewAPI.submitAnswer({
        interview_id: interviewId,
        question_id: question.id,
        answer: answers[question.id] || '',
        question_type: question.category || 'technical'
      });
    } catch (error) {
      console.error('Failed to submit answer:', error);
    }

    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    }
  };

  const handlePrevQuestion = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const handleCompleteInterview = async () => {
    setLoading(true);
    try {
      await interviewAPI.completeInterview(interviewId);
      await interviewAPI.evaluateInterview(interviewId);
      navigate(`/results/${interviewId}`);
    } catch (error) {
      alert('Failed to complete interview: ' + (error.response?.data?.error || error.message));
      navigate(`/results/${interviewId}`);
    } finally {
      setLoading(false);
    }
  };

  const toggleVoice = () => {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
      alert('Voice input not supported in your browser. Please type your answer.');
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    
    if (voiceActive) {
      recognition.stop();
      setVoiceActive(false);
    } else {
      recognition.continuous = true;
      recognition.interimResults = true;
      
      recognition.onresult = (event) => {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          transcript += event.results[i][0].transcript;
        }
        const currentAnswer = answers[questions[currentQuestion]?.id] || '';
        setAnswers({
          ...answers,
          [questions[currentQuestion].id]: currentAnswer + transcript
        });
      };

      recognition.onerror = () => {
        setVoiceActive(false);
      };

      recognition.onend = () => {
        setVoiceActive(false);
      };

      recognition.start();
      setVoiceActive(true);
    }
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setConfig({ ...config, resume_file: reader.result });
      };
      reader.readAsDataURL(file);
    }
  };

  if (step === 1) {
    return (
      <div className="interview-container">
        <div className="dashboard-card">
          <h2 style={{ marginBottom: '30px' }}>Start Your Mock Interview</h2>
          
          <div className="mb-4">
            <label className="form-label fw-bold">Interview Type</label>
            <div className="d-flex gap-3">
              {['technical', 'hr', 'mixed'].map((type) => (
                <div 
                  key={type}
                  className={`form-check p-3 border rounded ${config.interview_type === type ? 'border-primary bg-light' : ''}`}
                  style={{ cursor: 'pointer', minWidth: '120px' }}
                  onClick={() => setConfig({ ...config, interview_type: type })}
                >
                  <input
                    type="radio"
                    className="form-check-input"
                    name="interview_type"
                    value={type}
                    checked={config.interview_type === type}
                    onChange={() => setConfig({ ...config, interview_type: type })}
                  />
                  <label className="form-check-label text-capitalize">
                    {type === 'hr' ? 'HR Round' : type === 'mixed' ? 'Mixed (Both)' : 'Technical'}
                  </label>
                </div>
              ))}
            </div>
          </div>

          <div className="mb-4">
            <label className="form-label fw-bold">Upload Resume (Optional)</label>
            <div className="form-check mb-3">
              <input
                type="checkbox"
                className="form-check-input"
                id="hasResume"
                checked={config.has_resume}
                onChange={(e) => setConfig({ ...config, has_resume: e.target.checked })}
              />
              <label className="form-check-label" htmlFor="hasResume">
                I want to upload my resume for skill-based questions
              </label>
            </div>
            
            {config.has_resume && (
              <input
                type="file"
                className="form-control"
                accept=".pdf"
                onChange={handleFileUpload}
              />
            )}
          </div>

          <div className="alert alert-info">
            <strong>Note:</strong> You'll answer {questions.length || 10} questions. Take your time and be honest in your responses.
          </div>

          <button 
            className="btn btn-primary btn-lg w-100"
            onClick={handleStartInterview}
            disabled={loading}
          >
            {loading ? 'Starting Interview...' : 'Start Interview'}
          </button>
        </div>
      </div>
    );
  }

  if (step === 2 && questions.length > 0) {
    const question = questions[currentQuestion];
    
    return (
      <div className="interview-container">
        <div className="mb-3">
          <div className="d-flex justify-content-between align-items-center">
            <span style={{ color: 'white' }}>
              Question {currentQuestion + 1} of {questions.length}
            </span>
            <span className="badge bg-light text-dark">
              {question.category?.toUpperCase() || 'GENERAL'}
            </span>
          </div>
          <div className="progress mt-2" style={{ height: '5px' }}>
            <div 
              className="progress-bar bg-primary" 
              style={{ width: `${((currentQuestion + 1) / questions.length) * 100}%` }}
            />
          </div>
        </div>

        <div className="question-card">
          <span className="question-number">Question {currentQuestion + 1}</span>
          <h4 className="mb-4">{question.question_text}</h4>
          
          <div className="mb-3">
            <label className="form-label fw-bold">Your Answer:</label>
            <textarea
              className="answer-textarea"
              value={answers[question.id] || ''}
              onChange={(e) => handleAnswerChange(question.id, e.target.value)}
              placeholder="Type your answer here..."
            />
            <button 
              className={`voice-btn ${voiceActive ? 'btn-danger' : ''}`}
              onClick={toggleVoice}
            >
              {voiceActive ? 'Stop Recording' : 'Start Voice Input'}
            </button>
          </div>

          {question.ideal_answer && (
            <details className="mt-3">
              <summary style={{ cursor: 'pointer', color: '#667eea' }}>
                Show Ideal Answer (After you answer)
              </summary>
              <div className="alert alert-secondary mt-2">
                {question.ideal_answer}
              </div>
            </details>
          )}

          <div className="d-flex justify-content-between mt-4">
            <button 
              className="btn btn-outline-secondary"
              onClick={handlePrevQuestion}
              disabled={currentQuestion === 0}
            >
              Previous
            </button>
            
            {currentQuestion < questions.length - 1 ? (
              <button 
                className="btn btn-primary"
                onClick={handleNextQuestion}
              >
                Next Question
              </button>
            ) : (
              <button 
                className="btn btn-success"
                onClick={handleCompleteInterview}
                disabled={loading}
              >
                {loading ? 'Submitting...' : 'Complete Interview'}
              </button>
            )}
          </div>
        </div>

        <div className="d-flex justify-content-center gap-2 mt-3">
          {questions.map((_, idx) => (
            <div
              key={idx}
              className={`rounded-circle ${idx === currentQuestion ? 'bg-primary' : answers[questions[idx].id] ? 'bg-success' : 'bg-secondary'}`}
              style={{ width: '12px', height: '12px', cursor: 'pointer' }}
              onClick={() => setCurrentQuestion(idx)}
            />
          ))}
        </div>
      </div>
    );
  }

  return null;
};

export default Interview;
