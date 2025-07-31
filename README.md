# PhishScope 🎣🔍

A comprehensive phishing detection and monitoring platform that combines certificate transparency monitoring, threat intelligence feeds, and URL analysis to identify and track phishing websites in real-time.
<img width="1347" height="1220" alt="image" src="https://github.com/user-attachments/assets/c2be3cd1-8002-4b65-886d-844111c68f8b" />


## 🌟 Features

- **Real-time Certificate Monitoring**: Monitors Certificate Transparency logs for suspicious domain registrations
- **Multi-source Threat Intelligence**: Aggregates data from multiple phishing feeds and blacklists
- **Advanced Analysis**: URL scanning with VirusTotal integration and custom threat assessment
- **Modern Web Interface**: React-based dashboard for monitoring and analysis
- **RESTful API**: FastAPI backend for programmatic access to data
- **Scalable Architecture**: Docker-based microservices architecture.  not ready yet

## 🎣 TO-DO list

- the project is not yet ready to be set up as compatible in docker. ❌ 
- addition of additional resources.❌ 
- Regulations for search performance.❌ 
- adding resources like virustotal etc. and integrating them with the ui to make it more user friendly.❌ 
- script that automatically creates the tables on the db. already existing should be improved.❌ 

## 🏗️ Architecture

PhishScope consists of four main components:

### 1. Certificate Stream Server (`ssl_stream_server/`)
- Monitors Certificate Transparency (CT) logs in real-time
- Identifies suspicious domain patterns and keywords
- Stores certificate data for analysis
- I reorganized the [certstream server](https://github.com/CaliDog/certstream-server) repo and got it working.

### 2. Phishing Crawler (`phish_crawl/`)
- Aggregates data from multiple threat intelligence sources:
  - PhishTank
  - OpenPhish
  - Phishing Army Blocklist
  - Black Mirror Blocklist
  - PhishStats
  - UT1 Blacklists (30+ categories)
  - Phishunt.io
- Scheduled crawling with configurable intervals
- Deduplication and data normalization

### 3. FastAPI Backend (`fast_api/`)
- RESTful API for data access and management
- VirusTotal integration for URL/hash analysis
- Advanced filtering and search capabilities
- Real-time statistics and reporting

### 4. React Frontend (`ui/`)
- Modern, responsive web interface
- Real-time dashboard with threat statistics
- Search and filtering capabilities
- Data visualization and reporting tools

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose.  not ready yet
- (Optional) VirusTotal API key for enhanced analysis

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/phishscope.git
   cd phishscope
   ```

2. **Set up environment variables**
   ```bash
   # Copy example environment files
   cp fast_api/env/.env.example fast_api/env/.env
   cp phish_crawl/env/.env.example phish_crawl/env/.env
   
   # Edit the .env files with your configuration
   ```

3. **Start the platform**
   ```bash
   docker-compose up -d
   ```

4. **Access the services**
   - Web Interface: http://localhost:3000
   - API Documentation: http://localhost:8000/docs
   - pgAdmin: http://localhost:5050 (admin@pentester.dad / H4y4lp3r32t3rb12474m4nl3tm3!)

## 🔧 Configuration

### Environment Variables

#### FastAPI Backend
```env
# Database Configuration
DB_HOST=postgres
DB_PORT=5432
DB_NAME=phishing_crawler
DB_USER=postgres
DB_PASSWORD=postgres

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# VirusTotal Integration (Optional)
VT_API_KEY=your_virustotal_api_key
```

#### Phishing Crawler
```env
# Database Configuration
DB_HOST=postgres
DB_PORT=5432
DB_NAME=phishing_crawler
DB_USER=postgres
DB_PASSWORD=postgres

# Crawler Configuration
CRAWL_INTERVAL=3600  # Seconds between crawl cycles
MAX_WORKERS=10       # Concurrent crawler threads
```

## 📊 Data Sources

PhishScope aggregates data from the following sources:

### Primary Feeds
- **PhishTank**: Community-driven phishing URL database
- **OpenPhish**: Real-time phishing URL feed
- **PhishStats**: Comprehensive phishing statistics and data

### Blocklists
- **Phishing Army**: Regularly updated phishing blocklist
- **Black Mirror**: Advanced threat intelligence feed
- **UT1 Blacklists**: 30+ categories of malicious domains

### Certificate Transparency
- Real-time monitoring of CT logs
- Pattern matching for suspicious domains
- Wildcard certificate detection

## 🔌 API Usage

### Get Recent Phishing URLs
```bash
curl -X GET "http://localhost:8000/v1/phishing-urls?limit=100&hours=24"
```

### Search for Specific Domain
```bash
curl -X GET "http://localhost:8000/v1/search?domain=example.com"
```

### VirusTotal Analysis
```bash
curl -X POST "http://localhost:8000/v1/analyze/url" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://suspicious-domain.com"}'
```

## 🛠️ Development

### Local Development Setup

1. **Set up Python environment**
   ```bash
   # For FastAPI backend
   cd fast_api
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
   # For Phishing Crawler
   cd ../phish_crawl
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Set up React frontend**
   ```bash
   cd ui
   npm install
   npm run dev
   ```

3. **Database setup**
   ```bash
   # Start PostgreSQL with Docker
   docker run -d --name phishscope-db \
     -e POSTGRES_USER=postgres \
     -e POSTGRES_PASSWORD=postgres \
     -e POSTGRES_DB=phishing_crawler \
     -p 5432:5432 postgres:15
   ```

### Project Structure

```
phishscope/
├── certstream_server/     # Certificate transparency monitoring
│   ├── certstream/        # Core CT monitoring logic
│   └── helper/           # Database utilities
├── fast_api/             # FastAPI backend
│   ├── api/              # API routes and endpoints
│   ├── core/             # Configuration and database
│   ├── models/           # Database models
│   ├── plugins/          # Analysis plugins (VirusTotal, etc.)
│   └── schema/           # Pydantic schemas
├── phish_crawl/          # Threat intelligence crawler
│   ├── helper/           # Database and utility functions
│   └── plugins/          # Source-specific crawlers
└── ui/                   # React frontend
    └── src/              # React components and logic
```

## 🚨 Security Considerations

- **API Security**: Implement authentication and rate limiting for production use
- **Database Security**: Use strong passwords and restrict network access
- **Data Privacy**: Ensure compliance with data protection regulations
- **Resource Limits**: Configure appropriate resource limits for Docker containers

## 📈 Monitoring and Logging

- Application logs are stored in `logs/` directories within each service
- PostgreSQL performance can be monitored via pgAdmin
- Health checks are configured for all services in docker-compose

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Certificate Transparency community
- PhishTank and OpenPhish for providing free threat intelligence
- VirusTotal for URL/file analysis capabilities
- All contributors to the open-source security community

## 🐛 Issues and Support

If you encounter any issues or need support:

1. Check the [Issues](https://github.com/yourusername/phishscope/issues) page
2. Review the logs in the respective `logs/` directories
3. Create a new issue with detailed information about the problem

---

**⚠️ Disclaimer**: This tool is for educational and defensive security purposes only. Users are responsible for complying with applicable laws and regulations.
