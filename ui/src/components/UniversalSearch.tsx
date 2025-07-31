import React, { useState, useEffect } from 'react';
import { Search, Filter, AlertTriangle, Shield, Clock, ExternalLink, X, ChevronDown, ChevronUp } from 'lucide-react';
import { SearchResponse, SearchSources, SearchResult } from '../types/api';
import { apiClient } from '../services/api';

const UniversalSearch: React.FC = () => {
  const [query, setQuery] = useState('');
  const [searchResults, setSearchResults] = useState<SearchResponse | null>(null);
  const [availableSources, setAvailableSources] = useState<SearchSources | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedSources, setSelectedSources] = useState<string[]>([]);
  const [showFilters, setShowFilters] = useState(false);
  const [expandedCategories, setExpandedCategories] = useState<{ [key: string]: boolean }>({});
  const [resultsPerPage, setResultsPerPage] = useState(20);
  const [currentPage, setCurrentPage] = useState(1);

  useEffect(() => {
    const fetchSources = async () => {
      try {
        const data = await apiClient.getSearchSources();
        setAvailableSources(data);
      } catch (err) {
        console.error('Error fetching sources:', err);
      }
    };
    fetchSources();
  }, []);

  const handleSearch = async () => {
    if (!query.trim()) return;

    try {
      setLoading(true);
      setError(null);
      setCurrentPage(1);
      const results = await apiClient.universalSearch(
        query,
        selectedSources.length > 0 ? selectedSources : undefined
      );
      setSearchResults(results);
    } catch (err) {
      setError('Search failed. Please try again.');
      console.error('Search error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const toggleSource = (source: string) => {
    setSelectedSources(prev => 
      prev.includes(source) 
        ? prev.filter(s => s !== source)
        : [...prev, source]
    );
  };

  const toggleCategoryExpansion = (category: string) => {
    setExpandedCategories(prev => ({
      ...prev,
      [category]: !prev[category]
    }));
  };

  const getResultIcon = (result: SearchResult): React.ReactNode => {
    if (result.result_type === 'ssl_certificate') return <Shield className="h-4 w-4 text-green-600" />;
    if (result.source === 'phishtank') return <AlertTriangle className="h-4 w-4 text-red-600" />;
    if (result.source.startsWith('ut1_')) return <Filter className="h-4 w-4 text-purple-600" />;
    return <AlertTriangle className="h-4 w-4 text-orange-600" />;
  };

  const getResultTypeDisplay = (type: string): { label: string; color: string } => {
    const typeMap: { [key: string]: { label: string; color: string } } = {
      'phishing_url': { label: 'Phishing URL', color: 'bg-red-100 text-red-800 border-red-200' },
      'blacklist_url': { label: 'Blacklist URL', color: 'bg-orange-100 text-orange-800 border-orange-200' },
      'ssl_certificate': { label: 'SSL Certificate', color: 'bg-green-100 text-green-800 border-green-200' }
    };
    return typeMap[type] || { label: type, color: 'bg-gray-100 text-gray-800 border-gray-200' };
  };

  const getThreatLevel = (result: SearchResult): { level: string; color: string } => {
    if (result.verified === 'yes' || result.source === 'phishtank') {
      return { level: 'High Risk', color: 'bg-red-100 text-red-800' };
    }
    if (result.source.startsWith('ut1_')) {
      return { level: 'Medium Risk', color: 'bg-orange-100 text-orange-800' };
    }
    return { level: 'Low Risk', color: 'bg-yellow-100 text-yellow-800' };
  };

  const paginateResults = (results: SearchResult[]) => {
    const startIndex = (currentPage - 1) * resultsPerPage;
    const endIndex = startIndex + resultsPerPage;
    return results.slice(startIndex, endIndex);
  };

  const getTotalPages = (totalResults: number) => {
    return Math.ceil(totalResults / resultsPerPage);
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-slate-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full mb-4">
            <Search className="h-8 w-8 text-white" />
          </div>
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
            Universal Intelligence Search
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
            Search across all phishing intelligence sources, blacklists, and SSL certificates in real-time
          </p>
        </div>

        {/* Search Interface */}
        <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg border border-gray-200 dark:border-slate-700 mb-8">
          <div className="p-6">
            {/* Main Search Bar */}
            <div className="relative mb-6">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search className="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Search for URLs, domains, keywords, certificates..."
                className="block w-full pl-10 pr-12 py-4 text-lg border border-gray-300 dark:border-slate-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-gray-50 dark:bg-slate-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
              />
              <div className="absolute inset-y-0 right-0 flex items-center">
                <button
                  onClick={handleSearch}
                  disabled={loading || !query.trim()}
                  className="mx-2 px-6 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed font-semibold transition-all duration-200 flex items-center space-x-2"
                >
                  {loading ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                      <span>Searching...</span>
                    </>
                  ) : (
                    <>
                      <Search className="h-4 w-4" />
                      <span>Search</span>
                    </>
                  )}
                </button>
              </div>
            </div>

            {/* Advanced Filters Toggle */}
            <div className="flex items-center justify-between mb-4">
              <button
                onClick={() => setShowFilters(!showFilters)}
                className="flex items-center space-x-2 text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
              >
                <Filter className="h-4 w-4" />
                <span className="font-medium">Advanced Filters</span>
                {showFilters ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
              </button>
              {selectedSources.length > 0 && (
                <div className="flex items-center space-x-2">
                  <span className="text-sm text-gray-500 dark:text-gray-400">
                    {selectedSources.length} sources selected
                  </span>
                  <button
                    onClick={() => setSelectedSources([])}
                    className="text-red-600 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300"
                  >
                    <X className="h-4 w-4" />
                  </button>
                </div>
              )}
            </div>

            {/* Advanced Filters Panel */}
            {showFilters && availableSources && (
              <div className="border-t border-gray-200 dark:border-slate-600 pt-6 space-y-6">
                {/* Primary Sources */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Primary Sources</h3>
                  <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-3">
                    {availableSources.main_sources.map(source => (
                      <button
                        key={source}
                        onClick={() => toggleSource(source)}
                        className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 border ${
                          selectedSources.includes(source)
                            ? 'bg-blue-600 text-white border-blue-600 shadow-md'
                            : 'bg-gray-50 dark:bg-slate-700 text-gray-700 dark:text-gray-300 border-gray-200 dark:border-slate-600 hover:bg-gray-100 dark:hover:bg-slate-600'
                        }`}
                      >
                        {source.charAt(0).toUpperCase() + source.slice(1)}
                      </button>
                    ))}
                  </div>
                </div>

                {/* UT1 Categories */}
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white">UT1 Categories</h3>
                    <button
                      onClick={() => toggleCategoryExpansion('ut1')}
                      className="text-sm text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300"
                    >
                      {expandedCategories.ut1 ? 'Show Less' : 'Show All'}
                    </button>
                  </div>
                  <div className="space-y-3">
                    <button
                      onClick={() => toggleSource('ut1')}
                      className={`px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200 border ${
                        selectedSources.includes('ut1')
                          ? 'bg-purple-600 text-white border-purple-600 shadow-md'
                          : 'bg-purple-50 dark:bg-purple-900/20 text-purple-700 dark:text-purple-300 border-purple-200 dark:border-purple-800 hover:bg-purple-100 dark:hover:bg-purple-900/30'
                      }`}
                    >
                      All UT1 Categories
                    </button>
                    <div className={`grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-2 ${
                      !expandedCategories.ut1 ? 'max-h-24 overflow-hidden' : ''
                    }`}>
                      {availableSources.ut1_categories.map(category => (
                        <button
                          key={category}
                          onClick={() => toggleSource(`ut1_${category}`)}
                          className={`px-3 py-1.5 rounded-md text-xs font-medium transition-all duration-200 border ${
                            selectedSources.includes(`ut1_${category}`)
                              ? 'bg-purple-600 text-white border-purple-600'
                              : 'bg-purple-50 dark:bg-purple-900/20 text-purple-700 dark:text-purple-300 border-purple-200 dark:border-purple-800 hover:bg-purple-100 dark:hover:bg-purple-900/30'
                          }`}
                        >
                          {category}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl p-4 mb-8">
            <div className="flex items-center space-x-3">
              <AlertTriangle className="h-5 w-5 text-red-600 dark:text-red-400" />
              <p className="text-red-800 dark:text-red-200 font-medium">{error}</p>
            </div>
          </div>
        )}

        {/* Search Results */}
        {searchResults && (
          <div className="space-y-6">
            {/* Results Summary */}
            <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg border border-gray-200 dark:border-slate-700 p-6">
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-4">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Search Results</h2>
                  <p className="text-gray-600 dark:text-gray-300">
                    Found <span className="font-semibold text-blue-600 dark:text-blue-400">{searchResults.total_found}</span> results for 
                    "<span className="font-semibold">{searchResults.query}</span>" 
                    in {searchResults.sources_searched.length} sources
                  </p>
                </div>
                <div className="flex items-center space-x-4 mt-4 sm:mt-0">
                  <select
                    value={resultsPerPage}
                    onChange={(e) => setResultsPerPage(Number(e.target.value))}
                    className="px-3 py-2 border border-gray-300 dark:border-slate-600 rounded-lg bg-white dark:bg-slate-700 text-gray-900 dark:text-white"
                  >
                    <option value={10}>10 per page</option>
                    <option value={20}>20 per page</option>
                    <option value={50}>50 per page</option>
                    <option value={100}>100 per page</option>
                  </select>
                </div>
              </div>
              
              {/* Quick Stats */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                {Object.entries(searchResults.results_by_type).map(([type, results]) => {
                  const typeDisplay = getResultTypeDisplay(type);
                  return (
                    <div key={type} className={`p-4 rounded-lg border ${typeDisplay.color}`}>
                      <div className="flex items-center space-x-2">
                        {getResultIcon({ result_type: type } as SearchResult)}
                        <span className="font-semibold">{typeDisplay.label}</span>
                      </div>
                      <p className="text-2xl font-bold mt-1">{results.length}</p>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Results by Type */}
            {Object.entries(searchResults.results_by_type).map(([type, results]) => {
              const typeDisplay = getResultTypeDisplay(type);
              const paginatedResults = paginateResults(results);
              const totalPages = getTotalPages(results.length);
              
              return (
                <div key={type} className="bg-white dark:bg-slate-800 rounded-xl shadow-lg border border-gray-200 dark:border-slate-700">
                  <div className="p-6 border-b border-gray-200 dark:border-slate-700">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        {getResultIcon({ result_type: type } as SearchResult)}
                        <h3 className="text-xl font-bold text-gray-900 dark:text-white">{typeDisplay.label}</h3>
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${typeDisplay.color}`}>
                          {results.length} results
                        </span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="p-6">
                    {paginatedResults.length > 0 ? (
                      <div className="space-y-4">
                        {paginatedResults.map((result, index) => {
                          const threatLevel = getThreatLevel(result);
                          return (
                            <div key={index} className="border border-gray-200 dark:border-slate-600 rounded-lg p-4 hover:bg-gray-50 dark:hover:bg-slate-700/50 transition-colors">
                              <div className="flex items-start justify-between">
                                <div className="flex-1 min-w-0">
                                  <div className="flex items-center space-x-3 mb-3">
                                    {getResultIcon(result)}
                                    <div className="flex-1 min-w-0">
                                      <p className="text-lg font-semibold text-gray-900 dark:text-white truncate">
                                        {result.url || result.subject_cn || result.title || 'N/A'}
                                      </p>
                                      <div className="flex items-center space-x-2 mt-1">
                                        <span className="px-2 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-300 rounded text-xs font-medium">
                                          {result.source}
                                        </span>
                                        <span className={`px-2 py-1 rounded text-xs font-medium ${threatLevel.color}`}>
                                          {threatLevel.level}
                                        </span>
                                      </div>
                                    </div>
                                  </div>
                                  
                                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                                    {result.target && (
                                      <div>
                                        <span className="font-medium text-gray-900 dark:text-white">Target:</span>
                                        <p className="text-gray-600 dark:text-gray-300 break-words">{result.target}</p>
                                      </div>
                                    )}
                                    {result.domains && (
                                      <div>
                                        <span className="font-medium text-gray-900 dark:text-white">Domains:</span>
                                        <p className="text-gray-600 dark:text-gray-300 break-words">{result.domains}</p>
                                      </div>
                                    )}
                                    {result.verified && (
                                      <div>
                                        <span className="font-medium text-gray-900 dark:text-white">Verified:</span>
                                        <span className={`ml-2 ${result.verified === 'yes' ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}`}>
                                          {result.verified}
                                        </span>
                                      </div>
                                    )}
                                  </div>
                                </div>
                                <div className="flex flex-col items-end space-y-2 ml-4">
                                  <div className="text-sm text-gray-500 dark:text-gray-400 text-right">
                                    <Clock className="h-4 w-4 inline mr-1" />
                                    {new Date(result.created_at).toLocaleDateString('en-US', {
                                      month: 'short',
                                      day: 'numeric',
                                      hour: '2-digit',
                                      minute: '2-digit'
                                    })}
                                  </div>
                                  {result.url && (
                                    <a
                                      href={result.url}
                                      target="_blank"
                                      rel="noopener noreferrer"
                                      className="flex items-center space-x-1 text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 text-sm"
                                    >
                                      <ExternalLink className="h-4 w-4" />
                                      <span>View</span>
                                    </a>
                                  )}
                                </div>
                              </div>
                            </div>
                          );
                        })}
                        
                        {/* Pagination */}
                        {totalPages > 1 && (
                          <div className="flex items-center justify-between pt-6 border-t border-gray-200 dark:border-slate-600">
                            <div className="text-sm text-gray-500 dark:text-gray-400">
                              Showing {((currentPage - 1) * resultsPerPage) + 1} to {Math.min(currentPage * resultsPerPage, results.length)} of {results.length} results
                            </div>
                            <div className="flex items-center space-x-2">
                              <button
                                onClick={() => setCurrentPage(currentPage - 1)}
                                disabled={currentPage === 1}
                                className="px-3 py-2 border border-gray-300 dark:border-slate-600 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-slate-700 disabled:opacity-50 disabled:cursor-not-allowed"
                              >
                                Previous
                              </button>
                              <span className="px-3 py-2 text-sm font-medium text-gray-700 dark:text-gray-300">
                                Page {currentPage} of {totalPages}
                              </span>
                              <button
                                onClick={() => setCurrentPage(currentPage + 1)}
                                disabled={currentPage === totalPages}
                                className="px-3 py-2 border border-gray-300 dark:border-slate-600 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-slate-700 disabled:opacity-50 disabled:cursor-not-allowed"
                              >
                                Next
                              </button>
                            </div>
                          </div>
                        )}
                      </div>
                    ) : (
                      <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                        <AlertTriangle className="h-12 w-12 mx-auto mb-4 opacity-50" />
                        <p className="text-lg">No {typeDisplay.label.toLowerCase()} found</p>
                      </div>
                    )}
                  </div>
                </div>
              );
            })}

            {searchResults.total_found === 0 && (
              <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg border border-gray-200 dark:border-slate-700 p-12 text-center">
                <Search className="h-16 w-16 mx-auto mb-4 text-gray-400" />
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">No results found</h3>
                <p className="text-gray-600 dark:text-gray-300 mb-6">
                  Try different keywords or adjust your search criteria
                </p>
                <button
                  onClick={() => setShowFilters(true)}
                  className="inline-flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  <Filter className="h-4 w-4" />
                  <span>Adjust Filters</span>
                </button>
              </div>
            )}
          </div>
        )}

        {/* Usage Examples */}
        {availableSources && !searchResults && !loading && (
          <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg border border-gray-200 dark:border-slate-700 p-6">
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4 flex items-center">
              <AlertTriangle className="h-5 w-5 mr-2 text-blue-600" />
              Search Examples
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {Object.entries(availableSources.usage_examples).map(([type, example]) => (
                <div key={type} className="bg-gray-50 dark:bg-slate-700 rounded-lg p-4 hover:bg-gray-100 dark:hover:bg-slate-600 transition-colors">
                  <h4 className="font-medium text-gray-900 dark:text-white capitalize mb-2">
                    {type.replace('_', ' ')}
                  </h4>
                  <code className="text-sm text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/20 px-3 py-2 rounded-md block break-all">
                    {example.split('?')[1] || example}
                  </code>
                  <button
                    onClick={() => setQuery(example.split('?')[1] || example)}
                    className="mt-2 text-xs text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400"
                  >
                    Use this example
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default UniversalSearch;
