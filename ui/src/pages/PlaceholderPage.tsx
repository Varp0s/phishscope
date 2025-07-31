import React from 'react';
import { ArrowLeft, Construction, Clock, Mail } from 'lucide-react';

interface PlaceholderPageProps {
  title: string;
  description: string;
  onNavigate: (page: string) => void;
}

const PlaceholderPage: React.FC<PlaceholderPageProps> = ({ title, description, onNavigate }) => {
  return (
    <div className="min-h-screen bg-white dark:bg-slate-900 flex items-center justify-center">
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <div className="bg-blue-100 dark:bg-blue-900/20 p-6 rounded-full w-fit mx-auto mb-8">
          <Construction className="h-16 w-16 text-blue-600" />
        </div>
        
        <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
          {title}
        </h1>
        
        <p className="text-xl text-gray-600 dark:text-gray-400 mb-8 leading-relaxed">
          {description}
        </p>
        
        <div className="bg-gray-50 dark:bg-slate-800 rounded-xl p-8 mb-8">
          <div className="flex items-center justify-center space-x-2 text-gray-500 dark:text-gray-400 mb-4">
            <Clock className="h-5 w-5" />
            <span>Coming Soon</span>
          </div>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            We're working hard to bring you comprehensive content for this section. 
            In the meantime, feel free to explore our other pages or contact us with any questions.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={() => onNavigate('home')}
              className="btn-primary flex items-center justify-center space-x-2"
            >
              <ArrowLeft className="h-4 w-4" />
              <span>Back to Home</span>
            </button>
            <button
              onClick={() => onNavigate('contact')}
              className="btn-secondary flex items-center justify-center space-x-2"
            >
              <Mail className="h-4 w-4" />
              <span>Contact Us</span>
            </button>
          </div>
        </div>
        
        <div className="text-sm text-gray-500 dark:text-gray-400">
          <p>
            Want to be notified when this page is ready? 
            <button 
              onClick={() => onNavigate('contact')}
              className="text-blue-600 dark:text-blue-400 hover:underline ml-1"
            >
              Get in touch
            </button>
          </p>
        </div>
      </div>
    </div>
  );
};

export default PlaceholderPage;