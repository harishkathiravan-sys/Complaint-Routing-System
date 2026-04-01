/**
 * Authentication Service
 * Manages user authentication and session
 */

export const authService = {
  // Get current user
  getCurrentUser: () => {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
  },

  // Check if user is logged in
  isLoggedIn: () => {
    return !!localStorage.getItem('token');
  },

  // Get user role
  getUserRole: () => {
    const user = authService.getCurrentUser();
    return user?.role || null;
  },

  // Login - called from API response
  login: (token, user) => {
    localStorage.setItem('token', token);
    localStorage.setItem('user', JSON.stringify(user));
  },

  // Logout
  logout: () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },

  // Get token
  getToken: () => {
    return localStorage.getItem('token');
  },

  // Check if student
  isStudent: () => {
    return authService.getUserRole() === 'student';
  },

  // Check if faculty
  isFaculty: () => {
    return authService.getUserRole() === 'faculty';
  },
};

export default authService;
