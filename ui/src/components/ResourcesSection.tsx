import React from 'react';
import { ExternalLink, Shield, Github, Database, Activity } from 'lucide-react';
import { threatSources } from '../data/mockData';

const ResourcesSection: React.FC = () => {
  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'api': return <Database className="h-6 w-6" />;
      case 'github': return <Github className="h-6 w-6" />;
      case 'registry': return <Shield className="h-6 w-6" />;
      case 'social': return <Activity className="h-6 w-6" />;
      default: return <Database className="h-6 w-6" />;
    }
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'api': return 'from-blue-500 to-cyan-500';
      case 'github': return 'from-gray-700 to-gray-900';
      case 'registry': return 'from-green-500 to-emerald-500';
      case 'social': return 'from-purple-500 to-pink-500';
      default: return 'from-blue-500 to-cyan-500';
    }
  };

  const getCategoryName = (category: string) => {
    switch (category) {
      case 'api': return 'API Kaynakları';
      case 'github': return 'GitHub Repoları';
      case 'registry': return 'Domain Kayıtları';
      case 'social': return 'Sosyal Medya';
      default: return 'Diğer';
    }
  };

  const groupedSources = threatSources.reduce((acc, source) => {
    if (!acc[source.category]) {
      acc[source.category] = [];
    }
    acc[source.category].push(source);
    return acc;
  }, {} as Record<string, typeof threatSources>);

  return (
    <section className="py-16 bg-white dark:bg-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
            Tehdit İstihbaratı Kaynakları
          </h2>
          <p className="text-lg text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
            Gerçek zamanlı tehdit verilerini toplayan güvenilir kaynaklar ve API'ler
          </p>
        </div>

        <div className="space-y-12">
          {Object.entries(groupedSources).map(([category, sources]) => (
            <div key={category}>
              <div className="flex items-center mb-6">
                <div className={`bg-gradient-to-r ${getCategoryColor(category)} p-3 rounded-lg mr-4`}>
                  {getCategoryIcon(category)}
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white">
                    {getCategoryName(category)}
                  </h3>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    {sources.length} aktif kaynak
                  </p>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {sources.map((source) => (
                  <div
                    key={source.id}
                    className="bg-gray-50 dark:bg-slate-700 rounded-xl p-6 hover:shadow-lg transition-all duration-200 transform hover:-translate-y-1"
                  >
                    <div className="flex items-start justify-between mb-4">
                      <div className={`bg-gradient-to-r ${getCategoryColor(category)} p-2 rounded-lg`}>
                        {getCategoryIcon(category)}
                      </div>
                      <div className="flex items-center space-x-2">
                        {source.isActive && (
                          <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                        )}
                        <span className="text-xs text-gray-500 dark:text-gray-400">
                          {source.isActive ? 'Aktif' : 'Pasif'}
                        </span>
                      </div>
                    </div>

                    <h4 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                      {source.name}
                    </h4>
                    <p className="text-gray-600 dark:text-gray-400 text-sm mb-4">
                      {source.description}
                    </p>

                    <div className="flex items-center justify-between">
                      <div className="text-xs text-gray-500 dark:text-gray-400">
                        Son güncelleme: {new Date(source.lastUpdate).toLocaleString('tr-TR', {
                          month: 'short',
                          day: 'numeric',
                          hour: '2-digit',
                          minute: '2-digit'
                        })}
                      </div>
                      <a
                        href={source.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center px-3 py-1 bg-blue-500 hover:bg-blue-600 text-white text-xs font-medium rounded-lg transition-colors duration-200"
                      >
                        Ziyaret Et
                        <ExternalLink className="ml-1 h-3 w-3" />
                      </a>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Add New Source CTA */}
        <div className="mt-12 text-center">
          <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl p-8 text-white">
            <h3 className="text-2xl font-bold mb-4">Yeni Kaynak Öner</h3>
            <p className="text-blue-100 mb-6">
              Bildiğiniz güvenilir bir tehdit istihbaratı kaynağı var mı? Topluluğa katkıda bulunun!
            </p>
            <button className="bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors duration-200">
              Kaynak Öner
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ResourcesSection;