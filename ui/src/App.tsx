import React from 'react';
import { ThemeProvider } from './context/ThemeContext';
import Header from './components/Header';
import HeroSection from './components/HeroSection';
import DomainTable from './components/DomainTable';
import APISection from './components/APISection';
import Footer from './components/Footer';
import PlaceholderPage from './pages/PlaceholderPage';
import StatisticsDashboard from './components/StatisticsDashboard';
import UniversalSearch from './components/UniversalSearch';

function App() {
  const [currentPage, setCurrentPage] = React.useState('home');

  const handleNavigate = (page: string) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const renderPage = () => {
    switch (currentPage) {
      case 'home':
        return (
          <main>
            <HeroSection onNavigate={handleNavigate} />
            <DomainTable />
            <APISection />
          </main>
        );
      
      case 'dashboard':
        return <StatisticsDashboard />;
      
      case 'search':
        return <UniversalSearch />;
      
      // Placeholder pages
      case 'api-docs':
        return (
          <PlaceholderPage
            title="API Documentation"
            description="Comprehensive documentation for integrating with our threat intelligence API, including endpoints, authentication, rate limits, and code examples."
            onNavigate={handleNavigate}
          />
        );
      
      case 'careers':
        return (
          <PlaceholderPage
            title="Careers"
            description="Join our mission to make the internet safer. Explore open positions in engineering, security research, product management, and more."
            onNavigate={handleNavigate}
          />
        );
      
      case 'blog':
        return (
          <PlaceholderPage
            title="Blog"
            description="Stay updated with the latest threat intelligence insights, security research, product updates, and industry analysis from our team of experts."
            onNavigate={handleNavigate}
          />
        );
      
      case 'privacy':
        return (
          <PlaceholderPage
            title="Privacy Policy"
            description="Learn how we collect, use, and protect your personal information. We're committed to transparency and protecting your privacy."
            onNavigate={handleNavigate}
          />
        );
      
      case 'terms':
        return (
          <PlaceholderPage
            title="Terms of Service"
            description="Our terms of service outline the rules and regulations for using our platform and services. Please read them carefully."
            onNavigate={handleNavigate}
          />
        );
      
      case 'gdpr':
        return (
          <PlaceholderPage
            title="GDPR Compliance"
            description="Information about our GDPR compliance measures and how we handle personal data for EU residents."
            onNavigate={handleNavigate}
          />
        );
      
      case 'security-policy':
        return (
          <PlaceholderPage
            title="Security Policy"
            description="Details about our security practices, incident response procedures, and how to report security vulnerabilities."
            onNavigate={handleNavigate}
          />
        );
      
      case 'help':
        return (
          <PlaceholderPage
            title="Help Center"
            description="Find answers to common questions, troubleshooting guides, and step-by-step tutorials for using our platform effectively."
            onNavigate={handleNavigate}
          />
        );
      
      case 'status':
        return (
          <PlaceholderPage
            title="System Status"
            description="Real-time status of our services, including API uptime, scheduled maintenance, and incident reports."
            onNavigate={handleNavigate}
          />
        );
      
      case 'forum':
        return (
          <PlaceholderPage
            title="Community Forum"
            description="Connect with other security professionals, share insights, ask questions, and discuss threat intelligence topics."
            onNavigate={handleNavigate}
          />
        );
      
      case 'press':
        return (
          <PlaceholderPage
            title="Press Kit"
            description="Media resources including company logos, product screenshots, executive bios, and press releases for journalists and partners."
            onNavigate={handleNavigate}
          />
        );
      
      default:
        return (
          <PlaceholderPage
            title="Page Not Found"
            description="The page you're looking for doesn't exist or has been moved. Please check the URL or navigate back to our homepage."
            onNavigate={handleNavigate}
          />
        );
    }
  };

  return (
    <ThemeProvider>
      <div className="min-h-screen bg-white dark:bg-slate-900 transition-colors duration-300">
        <Header currentPage={currentPage} onNavigate={handleNavigate} />
        {renderPage()}
        <Footer onNavigate={handleNavigate} />
      </div>
    </ThemeProvider>
  );
}

export default App;