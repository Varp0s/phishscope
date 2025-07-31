export interface PhishingDomain {
  id: string;
  domain: string;
  firstSeen: string;
  source: string;
  threatType: 'phishing' | 'malware' | 'typosquat' | 'dga';
  confidenceScore: number;
  targetBrand?: string;
  ipAddress?: string;
  country?: string;
  status: 'active' | 'inactive' | 'investigating';
}

export interface ThreatSource {
  id: string;
  name: string;
  description: string;
  category: 'api' | 'registry' | 'github' | 'social';
  url: string;
  icon: string;
  isActive: boolean;
  lastUpdate: string;
}

export interface ThreatStats {
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
  database_status: string;
}

export interface Feature {
  id: string;
  title: string;
  description: string;
  icon: string;
  category: 'detection' | 'intelligence' | 'integration' | 'monitoring';
  benefits: string[];
}

export interface Testimonial {
  id: string;
  name: string;
  role: string;
  company: string;
  content: string;
  avatar?: string;
  rating: number;
}

// Re-export API types
export * from './api';

export interface PricingPlan {
  id: string;
  name: string;
  price: {
    monthly: number;
    yearly: number;
  };
  description: string;
  features: string[];
  limitations?: string[];
  popular?: boolean;
  cta: string;
  ctaType: 'primary' | 'secondary' | 'contact';
}

export interface FAQ {
  id: string;
  question: string;
  answer: string;
  category: 'general' | 'pricing' | 'technical' | 'security';
}