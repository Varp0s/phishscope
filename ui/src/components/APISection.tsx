import React, { useState } from 'react';
import { Code, Copy, CheckCircle, Terminal, Book } from 'lucide-react';

const APISection: React.FC = () => {
  const [copiedCode, setCopiedCode] = useState<string | null>(null);

  const copyToClipboard = (code: string, id: string) => {
    navigator.clipboard.writeText(code);
    setCopiedCode(id);
    setTimeout(() => setCopiedCode(null), 2000);
  };

  const curlExample = `curl -X GET "https://api.phishguard.com/v1/phishing/latest" \\
  -H "Authorization: Bearer YOUR_API_KEY" \\
  -H "Content-Type: application/json"`;

  const pythonExample = `import requests

def get_phishing_domains():
    url = "https://api.phishguard.com/v1/phishing/latest"
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    return response.json()

domains = get_phishing_domains()
print(f"Found {len(domains['data'])} phishing domains")`;

  const javascriptExample = `const getPhishingDomains = async () => {
  const response = await fetch('https://api.phishguard.com/v1/phishing/latest', {
    method: 'GET',
    headers: {
      'Authorization': 'Bearer YOUR_API_KEY',
      'Content-Type': 'application/json'
    }
  });
  
  const data = await response.json();
  return data;
};

// Kullanım
getPhishingDomains()
  .then(data => console.log(\`\${data.data.length} phishing domain bulundu\`))
  .catch(error => console.error('Hata:', error));`;

  const jsonResponse = `{
  "status": "success",
  "data": [
    {
      "id": "ph_123456",
      "domain": "payp4l-secure-login.com",
      "first_seen": "2024-01-20T14:30:00Z",
      "source": "PhishTank",
      "threat_type": "phishing",
      "confidence_score": 95,
      "target_brand": "PayPal",
      "ip_address": "192.168.1.100",
      "country": "RU",
      "status": "active"
    }
  ],
  "meta": {
    "total": 1,
    "page": 1,
    "per_page": 50,
    "last_updated": "2024-01-20T14:35:00Z"
  }
}`;

  const CodeBlock: React.FC<{ code: string; language: string; id: string }> = ({ code, language, id }) => (
    <div className="relative">
      <div className="flex items-center justify-between bg-gray-800 px-4 py-2 rounded-t-lg">
        <span className="text-gray-300 text-sm font-medium">{language}</span>
        <button
          onClick={() => copyToClipboard(code, id)}
          className="flex items-center space-x-2 text-gray-400 hover:text-white transition-colors duration-200"
        >
          {copiedCode === id ? (
            <CheckCircle className="h-4 w-4 text-green-400" />
          ) : (
            <Copy className="h-4 w-4" />
          )}
          <span className="text-sm">{copiedCode === id ? 'Kopyalandı!' : 'Kopyala'}</span>
        </button>
      </div>
      <pre className="bg-gray-900 text-gray-300 p-4 rounded-b-lg overflow-x-auto">
        <code>{code}</code>
      </pre>
    </div>
  );

  return (
    <section className="py-16 bg-gray-50 dark:bg-slate-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <div className="flex justify-center mb-6">
            <div className="bg-blue-500 p-4 rounded-full">
              <Code className="h-8 w-8 text-white" />
            </div>
          </div>
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
            API Dokümantasyonu
          </h2>
          <p className="text-lg text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
            RESTful API ile phishing domain verilerine programatik erişim sağlayın
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
          {/* Code Examples */}
          <div className="lg:col-span-2 space-y-8">
            <div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">
                Entegrasyon Örnekleri
              </h3>
              
              <div className="space-y-6">
                <div>
                  <h4 className="text-lg font-medium text-gray-900 dark:text-white mb-3">cURL</h4>
                  <CodeBlock code={curlExample} language="bash" id="curl" />
                </div>

                <div>
                  <h4 className="text-lg font-medium text-gray-900 dark:text-white mb-3">Python</h4>
                  <CodeBlock code={pythonExample} language="python" id="python" />
                </div>

                <div>
                  <h4 className="text-lg font-medium text-gray-900 dark:text-white mb-3">JavaScript</h4>
                  <CodeBlock code={javascriptExample} language="javascript" id="javascript" />
                </div>

                <div>
                  <h4 className="text-lg font-medium text-gray-900 dark:text-white mb-3">JSON Response</h4>
                  <CodeBlock code={jsonResponse} language="json" id="json" />
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* API Endpoints */}
        <div className="bg-white dark:bg-slate-800 rounded-xl shadow-lg p-8">
          <h3 className="text-2xl font-semibold text-gray-900 dark:text-white mb-6">
            Mevcut Endpoint'ler
          </h3>
          
          <div className="space-y-6">
            <div className="border dark:border-slate-700 rounded-lg p-4">
              <div className="flex items-center space-x-3 mb-2">
                <span className="bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400 px-2 py-1 rounded text-sm font-medium">
                  GET
                </span>
                <code className="text-gray-900 dark:text-white font-mono">/v1/phishing/latest</code>
              </div>
              <p className="text-gray-600 dark:text-gray-400">En son tespit edilen phishing domainleri getirir</p>
            </div>

            <div className="border dark:border-slate-700 rounded-lg p-4">
              <div className="flex items-center space-x-3 mb-2">
                <span className="bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400 px-2 py-1 rounded text-sm font-medium">
                  GET
                </span>
                <code className="text-gray-900 dark:text-white font-mono">/v1/phishing/search</code>
              </div>
              <p className="text-gray-600 dark:text-gray-400">Belirli kriterlere göre domain arama</p>
            </div>

            <div className="border dark:border-slate-700 rounded-lg p-4">
              <div className="flex items-center space-x-3 mb-2">
                <span className="bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400 px-2 py-1 rounded text-sm font-medium">
                  GET
                </span>
                <code className="text-gray-900 dark:text-white font-mono">/v1/stats</code>
              </div>
              <p className="text-gray-600 dark:text-gray-400">Genel istatistik ve metrikler</p>
            </div>

            <div className="border dark:border-slate-700 rounded-lg p-4">
              <div className="flex items-center space-x-3 mb-2">
                <span className="bg-blue-100 text-blue-800 dark:bg-blue-900/20 dark:text-blue-400 px-2 py-1 rounded text-sm font-medium">
                  POST
                </span>
                <code className="text-gray-900 dark:text-white font-mono">/v1/phishing/report</code>
              </div>
              <p className="text-gray-600 dark:text-gray-400">Yeni phishing domain rapor etme</p>
            </div>
          </div>
        </div>        
      </div>
    </section>
  );
};

export default APISection;