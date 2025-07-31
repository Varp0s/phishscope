import React, { useState, useEffect } from 'react';
import { Search, RefreshCw, Download, AlertTriangle, Shield, Bug, Hash } from 'lucide-react';
import { PhishingDomain } from '../types';
import { mockPhishingDomains } from '../data/mockData';

const DomainTable: React.FC = () => {
  const [domains, setDomains] = useState<PhishingDomain[]>(mockPhishingDomains);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedThreatType] = useState<string>('all');
  const [isRefreshing, setIsRefreshing] = useState(false);

  const getThreatIcon = (type: string) => {
    switch (type) {
      case 'phishing': return <Shield className="h-4 w-4" />;
      case 'malware': return <Bug className="h-4 w-4" />;
      case 'typosquat': return <AlertTriangle className="h-4 w-4" />;
      case 'dga': return <Hash className="h-4 w-4" />;
      default: return <Shield className="h-4 w-4" />;
    }
  };

  const getThreatColor = (type: string) => {
    switch (type) {
      case 'phishing': return 'text-red-500 bg-red-100 dark:bg-red-900/20';
      case 'malware': return 'text-orange-500 bg-orange-100 dark:bg-orange-900/20';
      case 'typosquat': return 'text-yellow-500 bg-yellow-100 dark:bg-yellow-900/20';
      case 'dga': return 'text-purple-500 bg-purple-100 dark:bg-purple-900/20';
      default: return 'text-gray-500 bg-gray-100 dark:bg-gray-900/20';
    }
  };

  const getConfidenceColor = (score: number) => {
    if (score >= 90) return 'text-red-600 bg-red-100 dark:bg-red-900/20';
    if (score >= 75) return 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/20';
    return 'text-green-600 bg-green-100 dark:bg-green-900/20';
  };

  const filteredDomains = domains.filter(domain => {
    const matchesSearch = domain.domain.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         domain.targetBrand?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesType = selectedThreatType === 'all' || domain.threatType === selectedThreatType;
    return matchesSearch && matchesType;
  });

  const handleRefresh = () => {
    setIsRefreshing(true);
    setTimeout(() => {
      setIsRefreshing(false);
    }, 1000);
  };

  // Auto-refresh simulation
  useEffect(() => {
    const interval = setInterval(() => {
      // Simulate new domain detection
      const randomDomain = Math.random().toString(36).substring(7) + '.com';
      const newDomain: PhishingDomain = {
        id: Date.now().toString(),
        domain: randomDomain,
        firstSeen: new Date().toISOString(),
        source: 'PhishTank',
        threatType: 'phishing',
        confidenceScore: Math.floor(Math.random() * 30) + 70,
        status: 'active'
      };
      
      setDomains(prev => [newDomain, ...prev.slice(0, 9)]);
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  return (
    <section className="py-16 bg-gray-50 dark:bg-slate-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
            Phinishing Hole
          </h2>
          <p className="text-gray-600 dark:text-gray-400">
            Searching for crawled phishing domains?
          </p>
        </div>

        {/* Controls */}
        <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-6 mb-8">
          <div className="flex flex-col md:flex-row gap-4 mb-6">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
              <input
                type="text"
                placeholder="Domain ara veya marka ismi gir..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            
            <div className="flex gap-3">              
              <button
                onClick={handleRefresh}
                disabled={isRefreshing}
                className="px-4 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg transition-colors duration-200 disabled:opacity-50"
              >
                <RefreshCw className={`h-5 w-5 ${isRefreshing ? 'animate-spin' : ''}`} />
              </button>
              
              <button className="px-4 py-3 bg-green-500 hover:bg-green-600 text-white rounded-lg transition-colors duration-200">
                <Download className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>

        {/* Table */}
        <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-slate-700">
                <tr>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Alan Adı
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Tehdit Türü
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Güven Skoru
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Kaynak
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    İlk Görülme
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Durum
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-slate-700">
                {filteredDomains.map((domain) => (
                  <tr key={domain.id} className="hover:bg-gray-50 dark:hover:bg-slate-700 transition-colors duration-200">
                    <td className="px-6 py-4">
                      <div>
                        <div className="font-mono text-sm text-gray-900 dark:text-white">
                          {domain.domain}
                        </div>
                        {domain.targetBrand && (
                          <div className="text-xs text-gray-500 dark:text-gray-400">
                            Hedef: {domain.targetBrand}
                          </div>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${getThreatColor(domain.threatType)}`}>
                        {getThreatIcon(domain.threatType)}
                        <span className="ml-2 capitalize">{domain.threatType}</span>
                      </span>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium ${getConfidenceColor(domain.confidenceScore)}`}>
                        {domain.confidenceScore}%
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900 dark:text-white">
                      {domain.source}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-400">
                      {new Date(domain.firstSeen).toLocaleString('tr-TR')}
                    </td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                        domain.status === 'active' ? 'text-red-600 bg-red-100 dark:bg-red-900/20' :
                        domain.status === 'investigating' ? 'text-yellow-600 bg-yellow-100 dark:bg-yellow-900/20' :
                        'text-gray-600 bg-gray-100 dark:bg-gray-900/20'
                      }`}>
                        {domain.status === 'active' ? 'Aktif' : 
                         domain.status === 'investigating' ? 'İnceleniyor' : 'Pasif'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        <div className="mt-6 text-center text-sm text-gray-500 dark:text-gray-400">
          {filteredDomains.length} domain gösteriliyor • Son güncelleme: {new Date().toLocaleTimeString('tr-TR')}
        </div>
      </div>
    </section>
  );
};

export default DomainTable;