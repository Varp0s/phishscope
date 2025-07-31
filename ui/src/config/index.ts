// API configuration
export const API_CONFIG = {
  BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/v1',
  TIMEOUT: parseInt(import.meta.env.VITE_API_TIMEOUT || '10000'),
  RETRY_ATTEMPTS: 3,
  RETRY_DELAY: 1000,
};

// Environment variables
export const ENV = {
  API_BASE_URL: import.meta.env.VITE_API_BASE_URL,
  API_TIMEOUT: import.meta.env.VITE_API_TIMEOUT,
  APP_NAME: import.meta.env.VITE_APP_NAME,
  APP_VERSION: import.meta.env.VITE_APP_VERSION,
  NODE_ENV: import.meta.env.NODE_ENV,
  DEV: import.meta.env.DEV,
  PROD: import.meta.env.PROD,
};

// API endpoints
export const ENDPOINTS = {
  HEALTH: '/health',
  DB_HEALTH: '/health/db',
  CERTIFICATES: '/certificates',
  CERTIFICATE_BY_ID: (id: number) => `/certificates/${id}`,
  SEARCH_DOMAINS: '/certificates/search/domains',
  STATISTICS: '/stats',
  RECENT_ACTIVITY: '/stats/recent',
};

// Default pagination settings
export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 20,
  MAX_PAGE_SIZE: 100,
  DEFAULT_PAGE: 1,
};

// Theme configuration
export const THEME = {
  colors: {
    primary: 'indigo',
    secondary: 'gray',
    success: 'green',
    warning: 'yellow',
    danger: 'red',
  },
};
