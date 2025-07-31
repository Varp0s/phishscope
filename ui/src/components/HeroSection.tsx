import React, { useState, useEffect } from 'react';
import { Activity, Shield, Globe, Clock, Database } from 'lucide-react';
import { apiClient } from '../services/api';
import { Statistics } from '../types/api';

interface HeroSectionProps {
  onNavigate: (page: string) => void;
}

const HeroSection: React.FC<HeroSectionProps> = ({ onNavigate }) => {
  const [stats, setStats] = useState<Statistics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        setLoading(true);
        const data = await apiClient.getStatistics();
        setStats(data);
        setError(null);
      } catch (err) {
        console.error('Failed to fetch statistics:', err);
        setError('Failed to load statistics');
        // Fallback to default values
        setStats({
          total_certificates: 0,
          recent_certificates_24h: 0,
          recent_certificates_7d: 0,
          updated_certificates: 0,
          certificates_with_domains: 0,
          unique_subject_cns: 0,
          total_domains: 0,
          avg_certificates_per_day: 0,
          latest_certificate_date: null,
          oldest_certificate_date: null,
          grand_total_intelligence: 0,
          phishing_data: {
            total_phishing_urls: 0,
            recent_phishing_24h: 0,
            sources: {
              phishtank: 0,
              openphish: 0,
              phishing_army: 0,
              black_mirror: 0,
              phishunt: 0,
              phishstats: 0,
              ut1_blacklists: {
                total_ut1_urls: 0,
                categories_count: 0,
                categories: {}
              }
            }
          },
          database_status: 'disconnected'
        });
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  return (
    <section className="bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 dark:from-slate-950 dark:via-blue-950 dark:to-slate-950 text-white py-20 lg:py-32">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <div className="flex justify-center mb-6">
            <div className="bg-blue-500/20 p-4 rounded-full animate-pulse">
              <Activity className="h-12 w-12 text-blue-400" />
            </div>
          </div>
          
          <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold mb-6 bg-gradient-to-r from-blue-400 via-cyan-400 to-blue-400 bg-clip-text text-transparent leading-tight">
            PhishScope
          </h1>
          
          <h2 className="text-2xl md:text-3xl lg:text-4xl font-semibold mb-6 text-gray-200">
            Real-time Phishing Domain Detection
          </h2>
          
          <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-4xl mx-auto leading-relaxed">
            Advanced threat intelligence platform that detects phishing domains within minutes. 
            Protect your organization with comprehensive monitoring and instant alerts.
          </p>

          {/* Grand Total Intelligence Highlight */}
          {stats && !loading && (
            <div className="max-w-2xl mx-auto mb-12">
              <div className="bg-gradient-to-r from-blue-600/20 via-purple-600/20 to-blue-600/20 backdrop-blur-sm rounded-2xl p-8 border border-white/20 shadow-2xl">
                <div className="text-center">
                  <h3 className="text-lg text-gray-300 mb-2">Total Intelligence Gathered</h3>
                  <div className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-blue-400 bg-clip-text text-transparent mb-2">
                    {stats.grand_total_intelligence.toLocaleString()}
                  </div>
                  <p className="text-gray-400 text-sm">
                    {stats.total_certificates.toLocaleString()} SSL Certificates + {stats.phishing_data.total_phishing_urls.toLocaleString()} Phishing URLs
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 text-center card-hover">
            <div className="flex justify-center mb-3">
              <Globe className="h-8 w-8 text-blue-400" />
            </div>
            <div className="text-3xl font-bold text-white mb-1">
              {loading ? (
                <div className="animate-pulse bg-gray-400 h-8 w-16 mx-auto rounded"></div>
              ) : (
                stats?.certificates_with_domains.toLocaleString() || '0'
              )}
            </div>
            <div className="text-gray-300 text-sm">Domains Monitored</div>
          </div>

          <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 text-center card-hover">
            <div className="flex justify-center mb-3">
              <Shield className="h-8 w-8 text-green-400" />
            </div>
            <div className="text-3xl font-bold text-white mb-1">
              {loading ? (
                <div className="animate-pulse bg-gray-400 h-8 w-16 mx-auto rounded"></div>
              ) : (
                stats?.total_certificates.toLocaleString() || '0'
              )}
            </div>
            <div className="text-gray-300 text-sm">Total Certificates</div>
          </div>

          <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 text-center card-hover">
            <div className="flex justify-center mb-3">
              <Clock className="h-8 w-8 text-yellow-400" />
            </div>
            <div className="text-3xl font-bold text-white mb-1">
              {loading ? (
                <div className="animate-pulse bg-gray-400 h-8 w-16 mx-auto rounded"></div>
              ) : (
                stats?.recent_certificates_24h.toLocaleString() || '0'
              )}
            </div>
            <div className="text-gray-300 text-sm">New in 24h</div>
          </div>

          <div className="bg-white/10 backdrop-blur-sm rounded-xl p-6 text-center card-hover">
            <div className="flex justify-center mb-3">
              <Database className={`h-8 w-8 ${stats?.database_status === 'connected' ? 'text-green-400' : 'text-red-400'}`} />
            </div>
            <div className="text-3xl font-bold text-white mb-1">
              {loading ? (
                <div className="animate-pulse bg-gray-400 h-8 w-16 mx-auto rounded"></div>
              ) : (
                stats?.unique_subject_cns.toLocaleString() || '0'
              )}
            </div>
            <div className="text-gray-300 text-sm">Unique Subjects</div>
          </div>
        </div>

        {/* Additional Stats Row */}
        {stats && !loading && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-4 text-center">
              <div className="text-2xl font-bold text-white mb-1">
                {stats.recent_certificates_7d.toLocaleString()}
              </div>
              <div className="text-gray-400 text-sm">New in 7 days</div>
            </div>
            
            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-4 text-center">
              <div className="text-2xl font-bold text-white mb-1">
                {stats.avg_certificates_per_day.toFixed(1)}
              </div>
              <div className="text-gray-400 text-sm">Avg per day (30d)</div>
            </div>
            
            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-4 text-center">
              <div className="text-2xl font-bold text-white mb-1">
                {stats.updated_certificates.toLocaleString()}
              </div>
              <div className="text-gray-400 text-sm">Updated Records</div>
            </div>
          </div>
        )}

        {/* Phishing Intelligence Summary */}
        {stats && !loading && (
          <div className="bg-gradient-to-r from-red-600/10 via-orange-600/10 to-red-600/10 backdrop-blur-sm rounded-2xl p-6 mb-8 border border-red-500/20">
            <h3 className="text-xl font-bold text-red-400 mb-4 text-center">🎣 Phishing Intelligence Network</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-white">
                  {stats.phishing_data.total_phishing_urls.toLocaleString()}
                </div>
                <div className="text-red-300 text-sm">Total Threats</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-white">
                  {stats.phishing_data.recent_phishing_24h.toLocaleString()}
                </div>
                <div className="text-red-300 text-sm">New (24h)</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-white">
                  {Object.keys(stats.phishing_data.sources).length - 1}
                </div>
                <div className="text-red-300 text-sm">Active Sources</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-white">
                  {stats.phishing_data.sources.ut1_blacklists.categories_count}
                </div>
                <div className="text-red-300 text-sm">UT1 Categories</div>
              </div>
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="mt-12 flex flex-col sm:flex-row justify-center items-center space-y-4 sm:space-y-0 sm:space-x-6">
          <button
            onClick={() => onNavigate('dashboard')}
            className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-xl font-semibold transition-all duration-300 transform hover:scale-105 shadow-xl hover:shadow-2xl"
          >
            📊 View Dashboard
          </button>
          <button
            onClick={() => onNavigate('search')}
            className="bg-purple-600 hover:bg-purple-700 text-white px-8 py-4 rounded-xl font-semibold transition-all duration-300 transform hover:scale-105 shadow-xl hover:shadow-2xl"
          >
            🔍 Universal Search
          </button>
          <button
            onClick={() => onNavigate('api-docs')}
            className="bg-transparent border-2 border-white/30 hover:border-white/60 text-white px-8 py-4 rounded-xl font-semibold transition-all duration-300 hover:bg-white/10"
          >
            📚 API Docs
          </button>
        </div>

        {/* Database Status Indicator */}
        {stats && (
          <div className="mt-8 text-center">
            <div className={`inline-flex items-center px-4 py-2 rounded-full text-sm ${
              stats.database_status === 'connected' 
                ? 'bg-green-500/20 text-green-400 border border-green-500/30' 
                : 'bg-red-500/20 text-red-400 border border-red-500/30'
            }`}>
              <div className={`w-2 h-2 rounded-full mr-2 ${
                stats.database_status === 'connected' ? 'bg-green-400' : 'bg-red-400'
              }`}></div>
              Database: {stats.database_status}
            </div>
          </div>
        )}

        {error && (
          <div className="mt-4 text-center">
            <div className="inline-flex items-center px-4 py-2 rounded-full text-sm bg-red-500/20 text-red-400 border border-red-500/30">
              ⚠️ {error}
            </div>
          </div>
        )}
      </div>
    </section>
  );
};

export default HeroSection;