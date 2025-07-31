import { PhishingDomain, ThreatSource, Feature, Testimonial, PricingPlan, FAQ } from '../types';

export const mockPhishingDomains: PhishingDomain[] = [
  {
    id: '1',
    domain: 'payp4l-secure-login.com',
    firstSeen: '2024-01-20T14:30:00Z',
    source: 'PhishTank',
    threatType: 'phishing',
    confidenceScore: 95,
    targetBrand: 'PayPal',
    ipAddress: '192.168.1.100',
    country: 'RU',
    status: 'active'
  },
  {
    id: '2',
    domain: 'microsoft-security-update.net',
    firstSeen: '2024-01-20T13:15:00Z',
    source: 'URLhaus',
    threatType: 'malware',
    confidenceScore: 88,
    targetBrand: 'Microsoft',
    ipAddress: '203.0.113.5',
    country: 'CN',
    status: 'active'
  },
  {
    id: '3',
    domain: 'amaz0n-prime-renewal.org',
    firstSeen: '2024-01-20T12:45:00Z',
    source: 'OpenPhish',
    threatType: 'phishing',
    confidenceScore: 92,
    targetBrand: 'Amazon',
    ipAddress: '198.51.100.25',
    country: 'US',
    status: 'investigating'
  },
  {
    id: '4',
    domain: 'g00gle-verify-account.com',
    firstSeen: '2024-01-20T11:20:00Z',
    source: 'PhishStats',
    threatType: 'typosquat',
    confidenceScore: 85,
    targetBrand: 'Google',
    ipAddress: '203.0.113.15',
    country: 'BR',
    status: 'active'
  },
  {
    id: '5',
    domain: 'xvbnmklpoiuytrewq.tk',
    firstSeen: '2024-01-20T10:00:00Z',
    source: 'DGArchive',
    threatType: 'dga',
    confidenceScore: 76,
    ipAddress: '192.0.2.50',
    country: 'Unknown',
    status: 'inactive'
  }
];

export const threatSources: ThreatSource[] = [
  {
    id: '1',
    name: 'PhishTank',
    description: 'Community-driven anti-phishing service',
    category: 'api',
    url: 'https://phishtank.org/',
    icon: 'shield',
    isActive: true,
    lastUpdate: '2024-01-20T14:35:00Z'
  },
  {
    id: '2',
    name: 'URLhaus',
    description: 'Malware URL exchange by abuse.ch',
    category: 'api',
    url: 'https://urlhaus.abuse.ch/',
    icon: 'bug',
    isActive: true,
    lastUpdate: '2024-01-20T14:32:00Z'
  },
  {
    id: '3',
    name: 'OpenPhish',
    description: 'Phishing intelligence feed',
    category: 'api',
    url: 'https://openphish.com/',
    icon: 'fish',
    isActive: true,
    lastUpdate: '2024-01-20T14:30:00Z'
  },
  {
    id: '4',
    name: 'PhishStats',
    description: 'Real-time phishing statistics',
    category: 'api',
    url: 'https://phishstats.info/',
    icon: 'bar-chart',
    isActive: true,
    lastUpdate: '2024-01-20T14:28:00Z'
  },
  {
    id: '5',
    name: 'DGArchive',
    description: 'Domain generation algorithm tracking',
    category: 'github',
    url: 'https://dgarchive.caad.fkie.fraunhofer.de/',
    icon: 'github',
    isActive: true,
    lastUpdate: '2024-01-20T14:25:00Z'
  },
  {
    id: '6',
    name: 'Certificate Transparency',
    description: 'CT logs for suspicious certificates',
    category: 'registry',
    url: 'https://crt.sh/',
    icon: 'certificate',
    isActive: true,
    lastUpdate: '2024-01-20T14:20:00Z'
  }
];

export const features: Feature[] = [
  {
    id: '1',
    title: 'Real-time Detection',
    description: 'Advanced algorithms detect phishing domains within minutes of registration or activation.',
    icon: 'zap',
    category: 'detection',
    benefits: [
      'Sub-minute detection speed',
      'Machine learning powered analysis',
      'Continuous monitoring 24/7',
      'Automated threat classification'
    ]
  },
  {
    id: '2',
    title: 'Comprehensive Intelligence',
    description: 'Access detailed threat intelligence including IP addresses, hosting providers, and attack patterns.',
    icon: 'brain',
    category: 'intelligence',
    benefits: [
      'Detailed domain metadata',
      'Threat actor attribution',
      'Campaign tracking',
      'Historical analysis'
    ]
  },
  {
    id: '3',
    title: 'API Integration',
    description: 'Seamlessly integrate our threat feeds into your existing security infrastructure.',
    icon: 'plug',
    category: 'integration',
    benefits: [
      'RESTful API endpoints',
      'Real-time webhooks',
      'Multiple data formats',
      'Enterprise-grade reliability'
    ]
  },
  {
    id: '4',
    title: 'Global Monitoring',
    description: 'Monitor phishing activities across all major TLDs and geographic regions.',
    icon: 'globe',
    category: 'monitoring',
    benefits: [
      'Worldwide coverage',
      'Multi-language support',
      'Regional threat insights',
      'Cross-border tracking'
    ]
  },
  {
    id: '5',
    title: 'Brand Protection',
    description: 'Specialized monitoring for brand impersonation and typosquatting attacks.',
    icon: 'shield-check',
    category: 'detection',
    benefits: [
      'Brand keyword monitoring',
      'Typosquatting detection',
      'Logo similarity analysis',
      'Automated takedown assistance'
    ]
  },
  {
    id: '6',
    title: 'Threat Analytics',
    description: 'Advanced analytics and reporting to understand threat landscapes and trends.',
    icon: 'bar-chart-3',
    category: 'intelligence',
    benefits: [
      'Interactive dashboards',
      'Custom reporting',
      'Trend analysis',
      'Executive summaries'
    ]
  }
];

export const testimonials: Testimonial[] = [
  {
    id: '1',
    name: 'Sarah Chen',
    role: 'CISO',
    company: 'TechCorp Industries',
    content: 'PhishScope has revolutionized our threat detection capabilities. We now catch phishing attempts 80% faster than before.',
    rating: 5
  },
  {
    id: '2',
    name: 'Michael Rodriguez',
    role: 'Security Analyst',
    company: 'Financial Services Inc.',
    content: 'The API integration was seamless, and the real-time alerts have prevented multiple successful phishing campaigns targeting our customers.',
    rating: 5
  },
  {
    id: '3',
    name: 'Emily Watson',
    role: 'IT Director',
    company: 'Healthcare Solutions',
    content: 'Outstanding threat intelligence platform. The detailed reporting helps us stay ahead of emerging threats in the healthcare sector.',
    rating: 5
  },
  {
    id: '4',
    name: 'David Kim',
    role: 'Cybersecurity Manager',
    company: 'E-commerce Global',
    content: 'Brand protection features are exceptional. We\'ve significantly reduced successful brand impersonation attacks.',
    rating: 4
  }
];

export const pricingPlans: PricingPlan[] = [
  {
    id: 'free',
    name: 'Free',
    price: {
      monthly: 0,
      yearly: 0
    },
    description: 'Perfect for individuals and small teams getting started with phishing detection.',
    features: [
      '100 API calls per month',
      'Basic threat intelligence',
      'Email alerts',
      'Community support'
    ],
    limitations: [
      'Limited to 100 domains per month',
      'Basic reporting only',
      'No real-time webhooks'
    ],
    cta: 'Start Free',
    ctaType: 'secondary'
  },
  {
    id: 'pro',
    name: 'Pro',
    price: {
      monthly: 99,
      yearly: 990
    },
    description: 'Advanced features for growing businesses and security teams.',
    features: [
      '10,000 API calls per month',
      'Real-time threat intelligence',
      'Advanced analytics dashboard',
      'Webhook notifications',
      'Brand monitoring',
      'Priority support',
      'Custom integrations',
      'Historical data access'
    ],
    popular: true,
    cta: 'Subscribe Now',
    ctaType: 'primary'
  },
  {
    id: 'enterprise',
    name: 'Pro+',
    price: {
      monthly: 299,
      yearly: 2990
    },
    description: 'Enterprise-grade solution with unlimited access and premium support.',
    features: [
      'Unlimited API calls',
      'Premium threat intelligence',
      'Custom threat feeds',
      'Dedicated account manager',
      'SLA guarantees',
      '24/7 phone support',
      'On-premise deployment',
      'Custom reporting',
      'Threat hunting services',
      'Incident response support'
    ],
    cta: 'Contact Sales',
    ctaType: 'contact'
  }
];

export const faqs: FAQ[] = [
  {
    id: '1',
    question: 'How quickly can PhishScope detect new phishing domains?',
    answer: 'Our advanced detection algorithms can identify new phishing domains within minutes of their registration or activation. We continuously monitor certificate transparency logs, DNS changes, and multiple threat intelligence sources to ensure rapid detection.',
    category: 'technical'
  },
  {
    id: '2',
    question: 'What makes your threat intelligence different from free sources?',
    answer: 'Our threat intelligence combines multiple premium data sources with proprietary machine learning algorithms. We provide detailed metadata, confidence scores, threat actor attribution, and real-time updates that free sources cannot match.',
    category: 'general'
  },
  {
    id: '3',
    question: 'Can I integrate PhishScope with my existing security tools?',
    answer: 'Yes! We offer comprehensive API integration, webhooks, and support for popular SIEM platforms like Splunk, QRadar, and Sentinel. Our technical team can assist with custom integrations.',
    category: 'technical'
  },
  {
    id: '4',
    question: 'Is there a free trial available?',
    answer: 'Yes, we offer a free tier with 100 API calls per month. For our Pro and Pro+ plans, we provide a 14-day free trial with full access to all features.',
    category: 'pricing'
  },
  {
    id: '5',
    question: 'How do you ensure data privacy and security?',
    answer: 'We follow industry-standard security practices including SOC 2 compliance, end-to-end encryption, and regular security audits. All data is processed in secure, geographically distributed data centers.',
    category: 'security'
  },
  {
    id: '6',
    question: 'What support options are available?',
    answer: 'We offer multiple support channels: community forums for free users, email support for Pro users, and 24/7 phone support with dedicated account managers for Pro+ customers.',
    category: 'general'
  }
];