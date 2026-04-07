import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  forgotPassword: (email) => api.post('/auth/forgot-password', { email }),
  getProfile: () => api.get('/auth/profile'),
  updateProfile: (data) => api.put('/auth/profile', data)
};

export const interviewAPI = {
  startInterview: (data) => api.post('/interview/start', data),
  submitAnswer: (data) => api.post('/interview/submit-answer', data),
  completeInterview: (interviewId) => api.post('/interview/complete', { interview_id: interviewId }),
  getHistory: (page = 1) => api.get(`/interview/history?page=${page}`),
  getInterview: (id) => api.get(`/interview/${id}`)
};

export const codingAPI = {
  getProblems: (difficulty) => api.get(`/coding/problems${difficulty ? `?difficulty=${difficulty}` : ''}`),
  getProblem: (id) => api.get(`/coding/problems/${id}`),
  submitCode: (data) => api.post('/coding/submit', data),
  getSessions: (problemId) => api.get(`/coding/sessions${problemId ? `?problem_id=${problemId}` : ''}`),
  testCode: (data) => api.post('/coding/test', data)
};

export const evaluationAPI = {
  evaluateAnswer: (data) => api.post('/evaluation/answer', data),
  evaluateInterview: (interviewId) => api.post(`/evaluation/interview/${interviewId}`),
  getAnalysis: (interviewId) => api.get(`/evaluation/analysis/${interviewId}`)
};

export const dashboardAPI = {
  getOverview: () => api.get('/dashboard/overview'),
  getPerformance: () => api.get('/dashboard/performance'),
  getStrengths: () => api.get('/dashboard/strengths'),
  getWeaknesses: () => api.get('/dashboard/weaknesses'),
  getRecommendations: () => api.get('/dashboard/recommendations'),
  getDashboardData: () => api.get('/dashboard/dashboard-data')
};

export default api;
