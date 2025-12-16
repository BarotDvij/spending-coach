import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Transactions
export const getTransactions = () => api.get('/transactions/');
export const createTransaction = (data) => api.post('/transactions/', data);

// Budgets
export const getBudgets = () => api.get('/budgets/');

// Insights
export const getInsights = () => api.get('/insights/');

// Rewards endpoints (create these in Django later)
export const getUserProfile = (userId) => api.get(`/users/${userId}/profile/`);
export const getUserBadges = (userId) => api.get(`/users/${userId}/badges/`);

export default api;