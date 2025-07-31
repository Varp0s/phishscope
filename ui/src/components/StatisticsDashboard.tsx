import React, { useState, useEffect } from 'react';
import { Shield, Activity, Globe, Clock, Database } from 'lucide-react';
import { Statistics } from '../types/api';
import { apiClient } from '../services/api';

const StatisticsDashboard: React.FC = () => {
  const [stats, setStats] = useState<Statistics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        setLoading(true);
        const data = await apiClient.getStatistics();
        setStats(data);
      } catch (err) {
        setError('Failed to load statistics');
        console.error('Error fetching statistics:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchStats, 30000);
    return () => clearInterval(interval);
  }, []);

  const formatNumber = (num: number): string => {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toLocaleString();
  };

  const formatDate = (dateStr: string | null): string => {
    if (!dateStr) return 'N/A';
    return new Date(dateStr).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getTopUT1Categories = (categories: { [key: string]: number }, limit: number = 10) => {
    return Object.entries(categories)
      .sort(([, a], [, b]) => b - a)
      .slice(0, limit);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 dark:from-slate-900 dark:to-slate-800 p-4 lg:p-8">
        <div className="max-w-7xl mx-auto space-y-8">
          <div className="text-center mb-12">
            <h1 className="text-4xl lg:text-6xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-blue-800 bg-clip-text text-transparent mb-4">
              PhishScope Intelligence
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto mb-8">
              Loading comprehensive threat intelligence dashboard...
            </p>
            <div className="flex flex-col items-center space-y-4">
              <div className="animate-spin rounded-full h-16 w-16 border-4 border-blue-600 border-t-transparent"></div>
              <p className="text-gray-500 dark:text-gray-400 animate-pulse">
                Fetching statistics from database... This may take up to 30 seconds.
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error || !stats) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
        <h3 className="text-lg font-semibold text-red-800 mb-2">Error Loading Statistics</h3>
        <p className="text-red-600">{error || 'No data available'}</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 dark:from-slate-900 dark:to-slate-800 p-4 lg:p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl lg:text-6xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-blue-800 bg-clip-text text-transparent mb-4">
            PhishScope Intelligence
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            Real-time threat intelligence dashboard providing comprehensive insights into SSL certificates and phishing activities
          </p>
          <div className="mt-6 flex items-center justify-center space-x-6 text-sm">
            <span className={`inline-flex items-center px-4 py-2 rounded-full font-medium ${
              stats?.database_status === 'connected' 
                ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300' 
                : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
            }`}>
              <div className={`w-3 h-3 rounded-full mr-2 ${
                stats?.database_status === 'connected' ? 'bg-green-500' : 'bg-red-500'
              }`}></div>
              Database {stats?.database_status || 'Unknown'}
            </span>
            <span className="text-gray-500 dark:text-gray-400">
              🕒 Last updated: {new Date().toLocaleTimeString()}
            </span>
          </div>
        </div>

        {/* Certificate Intelligence */}
        <div className="bg-white dark:bg-slate-800 rounded-3xl shadow-xl border border-gray-100 dark:border-slate-700 overflow-hidden">
          <div className="bg-gradient-to-r from-blue-500 to-cyan-500 p-8 text-white">
            <h2 className="text-3xl font-bold mb-2 flex items-center">
              🔒 SSL Certificate Intelligence
            </h2>
            <p className="text-blue-100">Monitor SSL certificate landscape and domain registrations</p>
          </div>
          
          <div className="p-8">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              <div className="group">
                <div className="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-900 dark:to-blue-800 rounded-2xl p-6 h-full transform group-hover:scale-105 transition-all duration-300 shadow-lg">
                  <div className="flex items-center justify-between mb-4">
                    <div className="bg-blue-500 rounded-xl p-3">
                      <Shield className="h-8 w-8 text-white" />
                    </div>
                    <div className="text-right">
                      <h3 className="text-sm font-semibold text-blue-800 dark:text-blue-200 uppercase tracking-wide">Total Certificates</h3>
                    </div>
                  </div>
                  <p className="text-3xl font-bold text-blue-900 dark:text-blue-100">{formatNumber(stats?.total_certificates || 0)}</p>
                  <p className="text-sm text-blue-600 dark:text-blue-300 mt-2">Active monitoring</p>
                </div>
              </div>

              <div className="group">
                <div className="bg-gradient-to-br from-emerald-50 to-emerald-100 dark:from-emerald-900 dark:to-emerald-800 rounded-2xl p-6 h-full transform group-hover:scale-105 transition-all duration-300 shadow-lg">
                  <div className="flex items-center justify-between mb-4">
                    <div className="bg-emerald-500 rounded-xl p-3">
                      <Activity className="h-8 w-8 text-white" />
                    </div>
                    <div className="text-right">
                      <h3 className="text-sm font-semibold text-emerald-800 dark:text-emerald-200 uppercase tracking-wide">New (24h)</h3>
                    </div>
                  </div>
                  <p className="text-3xl font-bold text-emerald-900 dark:text-emerald-100">{formatNumber(stats?.recent_certificates_24h || 0)}</p>
                  <p className="text-sm text-emerald-600 dark:text-emerald-300 mt-2">Fresh discoveries</p>
                </div>
              </div>

              <div className="group">
                <div className="bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-900 dark:to-purple-800 rounded-2xl p-6 h-full transform group-hover:scale-105 transition-all duration-300 shadow-lg">
                  <div className="flex items-center justify-between mb-4">
                    <div className="bg-purple-500 rounded-xl p-3">
                      <Globe className="h-8 w-8 text-white" />
                    </div>
                    <div className="text-right">
                      <h3 className="text-sm font-semibold text-purple-800 dark:text-purple-200 uppercase tracking-wide">With Domains</h3>
                    </div>
                  </div>
                  <p className="text-3xl font-bold text-purple-900 dark:text-purple-100">{formatNumber(stats?.certificates_with_domains || 0)}</p>
                  <p className="text-sm text-purple-600 dark:text-purple-300 mt-2">Domain coverage</p>
                </div>
              </div>

              <div className="group">
                <div className="bg-gradient-to-br from-orange-50 to-orange-100 dark:from-orange-900 dark:to-orange-800 rounded-2xl p-6 h-full transform group-hover:scale-105 transition-all duration-300 shadow-lg">
                  <div className="flex items-center justify-between mb-4">
                    <div className="bg-orange-500 rounded-xl p-3">
                      <Clock className="h-8 w-8 text-white" />
                    </div>
                    <div className="text-right">
                      <h3 className="text-sm font-semibold text-orange-800 dark:text-orange-200 uppercase tracking-wide">Daily Average</h3>
                    </div>
                  </div>
                  <p className="text-3xl font-bold text-orange-900 dark:text-orange-100">{formatNumber(Math.round(stats?.avg_certificates_per_day || 0))}</p>
                  <p className="text-sm text-orange-600 dark:text-orange-300 mt-2">Processing rate</p>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm text-gray-600 dark:text-gray-400">
              <div className="bg-gray-50 dark:bg-slate-700 rounded-xl p-4">
                <span className="font-semibold text-gray-800 dark:text-gray-200">📅 Latest Certificate:</span> 
                <br className="md:hidden" />
                <span className="md:ml-2">{formatDate(stats?.latest_certificate_date)}</span>
              </div>
              <div className="bg-gray-50 dark:bg-slate-700 rounded-xl p-4">
                <span className="font-semibold text-gray-800 dark:text-gray-200">📅 Oldest Certificate:</span> 
                <br className="md:hidden" />
                <span className="md:ml-2">{formatDate(stats?.oldest_certificate_date)}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Phishing Intelligence */}
        <div className="bg-white dark:bg-slate-800 rounded-3xl shadow-xl border border-gray-100 dark:border-slate-700 overflow-hidden">
          <div className="bg-gradient-to-r from-red-500 to-pink-500 p-8 text-white">
            <h2 className="text-3xl font-bold mb-2 flex items-center">
              🎣 Phishing Intelligence Network
            </h2>
            <p className="text-red-100">Comprehensive threat detection across multiple intelligence sources</p>
          </div>
          
          <div className="p-8">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              
              {/* Main Threat Stats */}
              <div className="lg:col-span-1">
                <div className="space-y-6">
                  <div className="bg-gradient-to-br from-red-50 to-red-100 dark:from-red-900 dark:to-red-800 rounded-2xl p-6 text-center">
                    <div className="bg-red-500 rounded-full p-4 w-16 h-16 mx-auto mb-4">
                      <svg className="w-8 h-8 text-white mx-auto" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <h3 className="text-sm font-semibold text-red-800 dark:text-red-200 uppercase tracking-wide mb-2">Total Phishing URLs</h3>
                    <p className="text-4xl font-bold text-red-900 dark:text-red-100">{formatNumber(stats?.phishing_data.total_phishing_urls || 0)}</p>
                    <p className="text-sm text-red-600 dark:text-red-300 mt-2">Identified threats</p>
                  </div>
                  
                  <div className="bg-gradient-to-br from-yellow-50 to-yellow-100 dark:from-yellow-900 dark:to-yellow-800 rounded-2xl p-6 text-center">
                    <div className="bg-yellow-500 rounded-full p-4 w-16 h-16 mx-auto mb-4">
                      <Clock className="w-8 h-8 text-white" />
                    </div>
                    <h3 className="text-sm font-semibold text-yellow-800 dark:text-yellow-200 uppercase tracking-wide mb-2">New (24h)</h3>
                    <p className="text-3xl font-bold text-yellow-900 dark:text-yellow-100">{formatNumber(stats?.phishing_data.recent_phishing_24h || 0)}</p>
                    <p className="text-sm text-yellow-600 dark:text-yellow-300 mt-2">Recent threats</p>
                  </div>
                </div>
              </div>

              {/* Primary Sources */}
              <div className="lg:col-span-1">
                <h3 className="text-xl font-bold text-gray-800 dark:text-gray-200 mb-6 flex items-center">
                  🔍 Primary Sources
                </h3>
                <div className="space-y-3">
                  {stats && Object.entries(stats.phishing_data.sources)
                    .filter(([key]) => key !== 'ut1_blacklists')
                    .map(([source, count]) => (
                    <div key={source} className="group">
                      <div className="bg-gray-50 dark:bg-slate-700 rounded-xl p-4 hover:bg-gray-100 dark:hover:bg-slate-600 transition-all duration-300">
                        <div className="flex justify-between items-center">
                          <span className="font-medium text-gray-800 dark:text-gray-200 capitalize">
                            {source.replace('_', ' ')}
                          </span>
                          <span className="text-xl font-bold text-gray-900 dark:text-gray-100">
                            {formatNumber(count as number)}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* UT1 Categories */}
              <div className="lg:col-span-1">
                <h3 className="text-xl font-bold text-gray-800 dark:text-gray-200 mb-6 flex items-center">
                  🏷️ UT1 Categories
                  <span className="text-sm font-normal text-gray-500 dark:text-gray-400 ml-2">
                    ({stats?.phishing_data.sources.ut1_blacklists.categories_count} total)
                  </span>
                </h3>
                
                <div className="bg-gradient-to-br from-indigo-50 to-indigo-100 dark:from-indigo-900 dark:to-indigo-800 rounded-2xl p-6 mb-6">
                  <div className="text-center">
                    <p className="text-3xl font-bold text-indigo-900 dark:text-indigo-100">
                      {formatNumber(stats?.phishing_data.sources.ut1_blacklists.total_ut1_urls || 0)}
                    </p>
                    <p className="text-sm text-indigo-600 dark:text-indigo-300">Total UT1 URLs</p>
                  </div>
                </div>
                
                <div className="space-y-2 max-h-80 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-300 dark:scrollbar-thumb-gray-600">
                  {stats && getTopUT1Categories(stats.phishing_data.sources.ut1_blacklists.categories, 15).map(([category, count]) => (
                    <div key={category} className="group">
                      <div className="bg-gray-50 dark:bg-slate-700 rounded-lg p-3 hover:bg-gray-100 dark:hover:bg-slate-600 transition-all duration-300">
                        <div className="flex justify-between items-center">
                          <span className="text-sm text-gray-700 dark:text-gray-300 capitalize truncate">
                            {category.replace(/_/g, ' ')}
                          </span>
                          <span className="font-bold text-gray-900 dark:text-gray-100 text-sm ml-2">
                            {formatNumber(count)}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-gradient-to-r from-slate-100 to-blue-100 dark:from-slate-800 dark:to-slate-700 rounded-3xl p-8 shadow-xl">
          <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-200 mb-6 text-center">
            🚀 Quick Actions
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <button className="group bg-white dark:bg-slate-800 hover:bg-blue-50 dark:hover:bg-slate-700 p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
              <div className="text-center">
                <div className="bg-blue-500 rounded-2xl p-4 w-16 h-16 mx-auto mb-4 group-hover:scale-110 transition-transform duration-300">
                  <svg className="w-8 h-8 text-white mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200">Universal Search</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">Search across all intelligence sources</p>
              </div>
            </button>
            
            <button className="group bg-white dark:bg-slate-800 hover:bg-green-50 dark:hover:bg-slate-700 p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
              <div className="text-center">
                <div className="bg-green-500 rounded-2xl p-4 w-16 h-16 mx-auto mb-4 group-hover:scale-110 transition-transform duration-300">
                  <Shield className="w-8 h-8 text-white mx-auto" />
                </div>
                <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200">View Certificates</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">Browse SSL certificate database</p>
              </div>
            </button>
            
            <button className="group bg-white dark:bg-slate-800 hover:bg-purple-50 dark:hover:bg-slate-700 p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
              <div className="text-center">
                <div className="bg-purple-500 rounded-2xl p-4 w-16 h-16 mx-auto mb-4 group-hover:scale-110 transition-transform duration-300">
                  <Database className="w-8 h-8 text-white mx-auto" />
                </div>
                <h3 className="text-lg font-semibold text-gray-800 dark:text-gray-200">Detailed Analytics</h3>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">Deep dive into threat trends</p>
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StatisticsDashboard;
