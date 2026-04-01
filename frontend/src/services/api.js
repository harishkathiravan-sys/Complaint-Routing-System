/**
 * API Service
 * Handles all communication with the backend
 */

import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const axiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Handle responses
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear token and redirect to login
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

// ============ STUDENT ROUTES ============

export const studentApi = {
  login: (email, password) =>
    axiosInstance.post('/student/login', { email, password }),
  
  register: (email, password, full_name) =>
    axiosInstance.post('/student/register', { email, password, full_name }),
  
  getProfile: () =>
    axiosInstance.get('/student/profile'),
  
  getDashboard: () =>
    axiosInstance.get('/student/dashboard'),
  
  submitComplaint: (complaint_text) =>
    axiosInstance.post('/student/complaint/submit', { complaint_text }),
  
  getComplaints: (status = null, limit = 50) =>
    axiosInstance.get('/student/complaints', {
      params: { status, limit }
    }),
  
  getComplaintDetails: (complaint_id) =>
    axiosInstance.get(`/student/complaint/${complaint_id}`),
  
  getComplaintStatus: (complaint_id) =>
    axiosInstance.get(`/student/complaint/${complaint_id}/status`),
};

// ============ FACULTY ROUTES ============

export const facultyApi = {
  login: (email, password) =>
    axiosInstance.post('/faculty/login', { email, password }),
  
  getProfile: () =>
    axiosInstance.get('/faculty/profile'),
  
  getDashboard: () =>
    axiosInstance.get('/faculty/dashboard'),
  
  getComplaints: (status = null, limit = 50) =>
    axiosInstance.get('/faculty/complaints', {
      params: { status, limit }
    }),
  
  getComplaintDetails: (complaint_id) =>
    axiosInstance.get(`/faculty/complaint/${complaint_id}`),
  
  markAsRead: (complaint_id) =>
    axiosInstance.put(`/faculty/complaint/${complaint_id}/read`),
  
  addReply: (complaint_id, reply_text) =>
    axiosInstance.put(`/faculty/complaint/${complaint_id}/reply`, {
      reply_text
    }),
  
  resolveComplaint: (complaint_id) =>
    axiosInstance.put(`/faculty/complaint/${complaint_id}/resolve`),
};

// ============ SHARED ROUTES ============

export const complaintApi = {
  getDepartments: () =>
    axiosInstance.get('/complaint/departments'),
  
  getDepartmentByCode: (dept_code) =>
    axiosInstance.get(`/complaint/department/${dept_code}`),
  
  getStatistics: () =>
    axiosInstance.get('/complaint/statistics'),
};

export const healthApi = {
  check: () =>
    axiosInstance.get('/health'),
};

export default axiosInstance;
