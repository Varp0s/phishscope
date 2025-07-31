import React from 'react';
import { Zap, Brain, Plug, Globe, ShieldCheck, BarChart3, ArrowRight, CheckCircle } from 'lucide-react';
import { features } from '../data/mockData';

interface FeaturesPageProps {
  onNavigate: (page: string) => void;
}

const FeaturesPage: React.FC<FeaturesPageProps> = ({ onNavigate }) => {
  const getFeatureIcon = (iconName: string) => {
    const icons = {
      'zap': Zap,
      'brain': Brain,
      'plug': Plug,
      'globe': Globe,
      'shield-check': ShieldCheck,
      'bar-chart-3': BarChart3
    };
    const IconComponent = icons[iconName as keyof typeof icons] || Zap;
    return <IconComponent className="h-12 w-12" />;
  };

  const getCategoryColor = (category: string) => {
    const colors = {
      'detection': 'from-red-500 to-pink-500',
      'intelligence': 'from-blue-500 to-cyan-500',
      'integration': 'from-green-500 to-emerald-500',
      'monitoring': 'from-purple-500 to-violet-500'
    };
    return colors[category as keyof typeof colors] || 'from-blue-500 to-cyan-500';
  };

  return (
    <div className="min-h-screen bg-white dark:bg-slate-900">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
            Advanced Features
          </h1>
          <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-4xl mx-auto">
            Comprehensive phishing detection powered by cutting-edge technology, 
            machine learning algorithms, and real-time threat intelligence.
          </p>
          <button 
            onClick={() => onNavigate('pricing')}
            className="btn-primary text-lg px-8 py-4"
          >
            Start Free Trial
          </button>
        </div>
      </section>

      {/* Detailed Features */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="space-y-20">
            {features.map((feature, index) => (
              <div key={feature.id} className={`flex flex-col ${index % 2 === 0 ? 'lg:flex-row' : 'lg:flex-row-reverse'} items-center gap-12`}>
                <div className="lg:w-1/2">
                  <div className={`bg-gradient-to-r ${getCategoryColor(feature.category)} p-6 rounded-2xl mb-6 w-fit`}>
                    <div className="text-white">
                      {getFeatureIcon(feature.icon)}
                    </div>
                  </div>
                  <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-6">
                    {feature.title}
                  </h2>
                  <p className="text-xl text-gray-600 dark:text-gray-400 mb-8 leading-relaxed">
                    {feature.description}
                  </p>
                  <div className="space-y-4">
                    {feature.benefits.map((benefit, benefitIndex) => (
                      <div key={benefitIndex} className="flex items-center space-x-3">
                        <CheckCircle className="h-6 w-6 text-green-500 flex-shrink-0" />
                        <span className="text-gray-700 dark:text-gray-300 text-lg">{benefit}</span>
                      </div>
                    ))}
                  </div>
                </div>
                <div className="lg:w-1/2">
                  <div className="bg-gray-100 dark:bg-slate-800 rounded-2xl p-8 h-80 flex items-center justify-center">
                    <div className="text-center">
                      <div className={`bg-gradient-to-r ${getCategoryColor(feature.category)} p-8 rounded-full mb-4 mx-auto w-fit`}>
                        <div className="text-white">
                          {getFeatureIcon(feature.icon)}
                        </div>
                      </div>
                      <p className="text-gray-500 dark:text-gray-400">
                        Interactive demo coming soon
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Technical Specifications */}
      <section className="py-20 bg-gray-50 dark:bg-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-6">
              Technical Specifications
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
              Built with enterprise-grade infrastructure and cutting-edge technology stack.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                title: 'Detection Speed',
                specs: ['< 2 minutes average', '99.9% accuracy rate', '24/7 monitoring', 'Real-time alerts']
              },
              {
                title: 'API Performance',
                specs: ['99.9% uptime SLA', '< 100ms response time', 'Rate limiting', 'Global CDN']
              },
              {
                title: 'Data Sources',
                specs: ['15+ threat feeds', 'Certificate transparency', 'DNS monitoring', 'Social media tracking']
              },
              {
                title: 'Security & Compliance',
                specs: ['SOC 2 Type II', 'GDPR compliant', 'End-to-end encryption', 'Regular audits']
              },
              {
                title: 'Integration Options',
                specs: ['RESTful API', 'Webhooks', 'SIEM connectors', 'Custom integrations']
              },
              {
                title: 'Scalability',
                specs: ['Auto-scaling', 'Load balancing', 'Multi-region', 'Enterprise ready']
              }
            ].map((spec, index) => (
              <div key={index} className="bg-white dark:bg-slate-700 rounded-xl p-6 shadow-lg">
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                  {spec.title}
                </h3>
                <ul className="space-y-2">
                  {spec.specs.map((item, itemIndex) => (
                    <li key={itemIndex} className="flex items-center space-x-2">
                      <CheckCircle className="h-4 w-4 text-green-500" />
                      <span className="text-gray-600 dark:text-gray-400">{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-12 text-white">
            <h2 className="text-4xl font-bold mb-6">
              Ready to Experience These Features?
            </h2>
            <p className="text-xl text-blue-100 mb-8 max-w-3xl mx-auto">
              Join thousands of security professionals who trust PhishScope 
              to protect their organizations from advanced phishing threats.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button 
                onClick={() => onNavigate('pricing')}
                className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold hover:bg-gray-100 transition-colors duration-200 flex items-center justify-center space-x-2"
              >
                <span>View Pricing Plans</span>
                <ArrowRight className="h-5 w-5" />
              </button>
              <button 
                onClick={() => onNavigate('contact')}
                className="border border-white text-white px-8 py-4 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors duration-200"
              >
                Schedule Demo
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default FeaturesPage;