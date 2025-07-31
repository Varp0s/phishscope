import axios, { AxiosInstance, AxiosResponse } from 'axios';
import { 
  Certificate, 
  CertificateListResponse, 
  Statistics, 
  RecentActivity,
  CertificateSearchParams 
} from '../types/api';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
      timeout: parseInt(import.meta.env.VITE_API_TIMEOUT || '30000'), // Increased from 10s to 30s
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
        return config;
      },
      (error) => {
        console.error('❌ Request Error:', error);
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response: AxiosResponse) => {
        console.log(`✅ API Response: ${response.status} ${response.config.url}`);
        return response;
      },
      (error) => {
        console.error('❌ Response Error:', error.response?.data || error.message);
        return Promise.reject(error);
      }
    );
  }

  // Health endpoints
  async healthCheck() {
    const response = await this.client.get('/health/');
    return response.data;
  }

  async databaseHealth() {
    const response = await this.client.get('/health/db/');
    return response.data;
  }

  // Certificate endpoints
  async getCertificates(params?: CertificateSearchParams): Promise<CertificateListResponse> {
    const response = await this.client.get('/certificates/', { params });
    return response.data;
  }

  async getCertificate(id: number): Promise<Certificate> {
    const response = await this.client.get(`/certificates/${id}`);
    return response.data;
  }

  async searchDomains(query: string, limit: number = 10) {
    const response = await this.client.get('/certificates/search/domains/', {
      params: { query, limit }
    });
    return response.data;
  }

  // Search endpoints
  async universalSearch(query: string, sources?: string[], limit: number = 50, offset: number = 0) {
    const response = await this.client.get('/search/', {
      params: { 
        q: query, 
        sources: sources?.join(','), 
        limit, 
        offset 
      }
    });
    return response.data;
  }

  async getSearchSources() {
    const response = await this.client.get('/search/sources/');
    return response.data;
  }

  // Statistics endpoints
  async getStatistics(): Promise<Statistics> {
    const response = await this.client.get('/stats/');
    return response.data;
  }

  async getRecentActivity(limit: number = 10): Promise<{ recent_activity: RecentActivity[], count: number }> {
    const response = await this.client.get('/stats/recent/', {
      params: { limit }
    });
    return response.data;
  }
}

// Create singleton instance
export const apiClient = new ApiClient();

// Export default
export default apiClient;
