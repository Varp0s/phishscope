import React from 'react';
import { Shield, Users, Globe, Award, Target, Zap, Heart, ArrowRight } from 'lucide-react';

interface AboutPageProps {
  onNavigate: (page: string) => void;
}

const AboutPage: React.FC<AboutPageProps> = ({ onNavigate }) => {
  const teamMembers = [
    {
      name: 'Sarah Chen',
      role: 'CEO & Co-founder',
      bio: 'Former CISO with 15+ years in cybersecurity. Led security teams at Fortune 500 companies.',
      expertise: ['Executive Leadership', 'Cybersecurity Strategy', 'Risk Management']
    },
    {
      name: 'Michael Rodriguez',
      role: 'CTO & Co-founder',
      bio: 'Security researcher and engineer. Published 20+ papers on threat detection and machine learning.',
      expertise: ['Machine Learning', 'Threat Detection', 'System Architecture']
    },
    {
      name: 'Emily Watson',
      role: 'Head of Product',
      bio: 'Product leader with expertise in security tools. Former product manager at leading security vendors.',
      expertise: ['Product Strategy', 'User Experience', 'Market Research']
    },
    {
      name: 'David Kim',
      role: 'Lead Security Engineer',
      bio: 'Cybersecurity expert specializing in phishing detection and threat intelligence platforms.',
      expertise: ['Threat Intelligence', 'API Development', 'Security Engineering']
    }
  ];

  const milestones = [
    { year: '2020', event: 'Company founded by cybersecurity veterans' },
    { year: '2021', event: 'First major enterprise client onboarded' },
    { year: '2022', event: 'Reached 1M+ domains monitored daily' },
    { year: '2023', event: 'Launched advanced ML-powered detection' },
    { year: '2024', event: 'Expanded to global threat intelligence network' }
  ];

  return (
    <div className="min-h-screen bg-white dark:bg-slate-900">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h1 className="text-5xl md:text-6xl font-bold mb-6 bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
              About PhishScope
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-4xl mx-auto">
              We're on a mission to make the internet safer by providing the world's most 
              advanced phishing detection and threat intelligence platform.
            </p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="text-4xl font-bold text-blue-400 mb-2">10,000+</div>
              <div className="text-gray-300">Organizations Protected</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-green-400 mb-2">2M+</div>
              <div className="text-gray-300">Threats Detected</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-purple-400 mb-2">50+</div>
              <div className="text-gray-300">Countries Served</div>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-yellow-400 mb-2">99.9%</div>
              <div className="text-gray-300">Uptime SLA</div>
            </div>
          </div>
        </div>
      </section>

      {/* Mission & Vision */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <div>
              <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-6">
                Our Mission
              </h2>
              <p className="text-xl text-gray-600 dark:text-gray-400 mb-8 leading-relaxed">
                To democratize access to advanced threat intelligence and make sophisticated 
                phishing detection capabilities available to organizations of all sizes. We believe 
                that cybersecurity should not be a luxury reserved for large enterprises.
              </p>
              <div className="space-y-4">
                {[
                  'Protect organizations from evolving phishing threats',
                  'Provide real-time, actionable threat intelligence',
                  'Enable proactive security measures through early detection',
                  'Foster a safer digital ecosystem for everyone'
                ].map((item, index) => (
                  <div key={index} className="flex items-center space-x-3">
                    <Target className="h-6 w-6 text-blue-600 flex-shrink-0" />
                    <span className="text-gray-700 dark:text-gray-300">{item}</span>
                  </div>
                ))}
              </div>
            </div>
            <div className="bg-gradient-to-br from-blue-50 to-purple-50 dark:from-slate-800 dark:to-slate-700 rounded-2xl p-8">
              <div className="text-center">
                <Shield className="h-16 w-16 text-blue-600 mx-auto mb-6" />
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                  Our Vision
                </h3>
                <p className="text-gray-600 dark:text-gray-400 leading-relaxed">
                  A world where phishing attacks are detected and neutralized before they can 
                  cause harm, where organizations can focus on their core business knowing 
                  their digital assets are protected by intelligent, automated security systems.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Values */}
      <section className="py-20 bg-gray-50 dark:bg-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-6">
              Our Core Values
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
              These principles guide everything we do, from product development to customer support.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: Shield,
                title: 'Security First',
                description: 'We prioritize security in every decision, from our platform architecture to our business practices.'
              },
              {
                icon: Zap,
                title: 'Innovation',
                description: 'We continuously push the boundaries of threat detection technology to stay ahead of evolving threats.'
              },
              {
                icon: Users,
                title: 'Customer Success',
                description: 'Our customers\' success is our success. We\'re committed to providing exceptional value and support.'
              },
              {
                icon: Globe,
                title: 'Global Impact',
                description: 'We work to make the internet safer for everyone, regardless of geography or organization size.'
              },
              {
                icon: Heart,
                title: 'Transparency',
                description: 'We believe in open communication, honest reporting, and transparent business practices.'
              },
              {
                icon: Award,
                title: 'Excellence',
                description: 'We strive for excellence in everything we do, from code quality to customer experience.'
              }
            ].map((value, index) => (
              <div key={index} className="bg-white dark:bg-slate-700 rounded-xl p-8 text-center card-hover">
                <div className="bg-blue-100 dark:bg-blue-900/20 p-4 rounded-full w-fit mx-auto mb-6">
                  <value.icon className="h-8 w-8 text-blue-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                  {value.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-400 leading-relaxed">
                  {value.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Team */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-6">
              Meet Our Team
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
              Our diverse team of cybersecurity experts, engineers, and researchers is dedicated 
              to building the future of threat detection.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {teamMembers.map((member, index) => (
              <div key={index} className="bg-white dark:bg-slate-800 rounded-xl p-6 text-center shadow-lg card-hover">
                <div className="w-20 h-20 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-white font-bold text-xl">
                    {member.name.split(' ').map(n => n[0]).join('')}
                  </span>
                </div>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                  {member.name}
                </h3>
                <p className="text-blue-600 dark:text-blue-400 font-medium mb-4">
                  {member.role}
                </p>
                <p className="text-gray-600 dark:text-gray-400 text-sm mb-4 leading-relaxed">
                  {member.bio}
                </p>
                <div className="space-y-1">
                  {member.expertise.map((skill, skillIndex) => (
                    <span
                      key={skillIndex}
                      className="inline-block bg-gray-100 dark:bg-slate-700 text-gray-700 dark:text-gray-300 px-2 py-1 rounded text-xs mr-1"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Timeline */}
      <section className="py-20 bg-gray-50 dark:bg-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-6">
              Our Journey
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
              From a small startup to a leading threat intelligence platform, 
              here are the key milestones in our growth.
            </p>
          </div>

          <div className="relative">
            <div className="absolute left-1/2 transform -translate-x-1/2 w-1 h-full bg-blue-200 dark:bg-blue-800"></div>
            <div className="space-y-12">
              {milestones.map((milestone, index) => (
                <div key={index} className={`flex items-center ${index % 2 === 0 ? 'flex-row' : 'flex-row-reverse'}`}>
                  <div className={`w-1/2 ${index % 2 === 0 ? 'pr-8 text-right' : 'pl-8 text-left'}`}>
                    <div className="bg-white dark:bg-slate-700 rounded-lg p-6 shadow-lg">
                      <div className="text-2xl font-bold text-blue-600 dark:text-blue-400 mb-2">
                        {milestone.year}
                      </div>
                      <p className="text-gray-700 dark:text-gray-300">
                        {milestone.event}
                      </p>
                    </div>
                  </div>
                  <div className="relative z-10">
                    <div className="w-4 h-4 bg-blue-600 rounded-full border-4 border-white dark:border-slate-900"></div>
                  </div>
                  <div className="w-1/2"></div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-12 text-white">
            <h2 className="text-4xl font-bold mb-6">
              Join Us in Making the Internet Safer
            </h2>
            <p className="text-xl text-blue-100 mb-8 max-w-3xl mx-auto">
              Whether you're looking to protect your organization or join our mission, 
              we'd love to hear from you.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button 
                onClick={() => onNavigate('contact')}
                className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold hover:bg-gray-100 transition-colors duration-200 flex items-center justify-center space-x-2"
              >
                <span>Get in Touch</span>
                <ArrowRight className="h-5 w-5" />
              </button>
              <button 
                onClick={() => onNavigate('careers')}
                className="border border-white text-white px-8 py-4 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors duration-200"
              >
                View Open Positions
              </button>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default AboutPage;