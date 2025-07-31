// API types
export interface Certificate {
  id: number;
  subject_cn: string;
  domains?: string;
  created_at: string;
  updated_at: string;
}

export interface PaginationInfo {
  page: number;
  limit: number;
  total: number;
  total_pages: number;
  has_next: boolean;
  has_prev: boolean;
}

export interface CertificateListResponse {
  certificates: Certificate[];
  pagination: PaginationInfo;
}

export interface UT1Categories {
  [category: string]: number;
}

export interface UT1Statistics {
  total_ut1_urls: number;
  categories_count: number;
  categories: UT1Categories;
}

export interface PhishingSources {
  phishtank: number;
  openphish: number;
  phishing_army: number;
  black_mirror: number;
  phishunt: number;
  phishstats: number;
  ut1_blacklists: UT1Statistics;
}

export interface PhishingData {
  total_phishing_urls: number;
  recent_phishing_24h: number;
  sources: PhishingSources;
}

export interface Statistics {
  total_certificates: number;
  recent_certificates_24h: number;
  recent_certificates_7d: number;
  updated_certificates: number;
  certificates_with_domains: number;
  unique_subject_cns: number;
  total_domains: number;
  avg_certificates_per_day: number;
  latest_certificate_date: string | null;
  oldest_certificate_date: string | null;
  grand_total_intelligence: number;
  phishing_data: PhishingData;
  database_status: string;
}

export interface RecentActivity {
  subject_cn: string;
  domains?: string;
  created_at: string;
  updated_at: string;
  was_updated: boolean;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}

export interface SearchResult {
  id?: number;
  url?: string;
  title?: string;
  target?: string;
  verified?: string;
  created_at: string;
  source: string;
  result_type: 'phishing_url' | 'blacklist_url' | 'ssl_certificate';
  domains?: string;
  subject_cn?: string;
}

export interface SearchResponse {
  query: string;
  search_type: string;
  sources_searched: string[];
  total_found: number;
  returned: number;
  limit: number;
  offset: number;
  results_by_type: {
    [key: string]: SearchResult[];
  };
  all_results: SearchResult[];
}

export interface SearchSources {
  main_sources: string[];
  ut1_categories: string[];
  search_capabilities: {
    wildcard_search: string;
    url_search: string;
    keyword_search: string;
    certificate_search: string;
    domain_search: string;
  };
  usage_examples: {
    [key: string]: string;
  };
}

// Search parameters
export interface CertificateSearchParams {
  page?: number;
  limit?: number;
  search?: string;
  has_domains?: boolean;
}
