# 🔬 Research Gap Finder

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Security](https://img.shields.io/badge/Security-Protected-brightgreen.svg)](#security)

An intelligent academic research tool that helps researchers identify gaps in the literature using AI-powered analysis. Built with comprehensive security, rate limiting, and professional export capabilities.

## ✨ **Key Features**

### 🔍 **Smart Academic Search**
- **Multi-Database Search**: Semantic Scholar + Crossref integration
- **Rate-Limited Compliance**: Proper 1 req/sec rate limiting for APIs
- **Intelligent Query Generation**: AI-powered search strategy optimization
- **Real-Time Status Updates**: User-friendly progress feedback

### 🤖 **AI-Powered Analysis**
- **Research Gap Identification**: Methodological, theoretical, and empirical gaps
- **Paper Quality Assessment**: Automated A+ to F grading system
- **Multi-Criteria Evaluation**: Methodology, novelty, impact, clarity, applicability
- **Confidence Scoring**: Statistical confidence in gap analysis

### 📊 **Professional Export System**
- **JSON Export**: Developer-friendly structured data
- **YAML Export**: Human-readable configuration format
- **CSV Bundle**: 3-file spreadsheet package (papers, gaps, summary)
- **Excel Workbook**: Professional multi-sheet reports with formatting

### 🔒 **Enterprise Security**
- **API Key Protection**: Environment variables + .gitignore
- **Secure Configuration**: Professional key management system
- **Interactive Setup**: Guided security configuration
- **No Hardcoded Secrets**: Industry-standard security practices

## 🚀 **Quick Start**

### **1. Clone and Setup**
```bash
git clone https://github.com/calvinliao223/research-gap-finder.git
cd research-gap-finder
pip install -r requirements.txt
```

### **2. Secure Configuration**
```bash
# Interactive setup (recommended)
python setup_security.py

# Or manual setup
cp .env.template .env
# Edit .env with your API keys
```

### **3. Launch Application**
```bash
streamlit run research_gap_finder.py
```

Visit `http://localhost:8501` to start researching!

## Configuration

### API Keys (Optional but Recommended)

The application works without API keys but provides enhanced features with them:

```env
# At least one is recommended for advanced analysis
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here  
GOOGLE_API_KEY=your_google_key_here

# Academic database keys (optional)
SEMANTIC_SCHOLAR_API_KEY=your_s2_key_here
```

### Without API Keys
- Basic paper search functionality
- Simple temporal gap analysis
- Manual topic extraction required

### With API Keys
- Smart topic extraction from natural language
- Advanced gap analysis (methodological, theoretical, etc.)
- Intelligent search query generation
- Context-aware responses

## Usage

### 1. **Start a Research Topic**
Simply describe your research interest:
- "I want to research machine learning in healthcare"
- "sustainable energy storage"
- "Find papers on mental health and social media"

### 2. **Search for Papers**
The system will:
- Generate intelligent search queries
- Search multiple academic databases
- Deduplicate and rank results
- Present papers with metadata

### 3. **Analyze Research Gaps**
Click "Analyze Gaps" to identify:
- Temporal gaps (underexplored time periods)
- Methodological gaps (missing approaches)
- Theoretical gaps (lacking frameworks)
- Application gaps (unexplored use cases)
- Interdisciplinary opportunities

### 4. **Export Results**
Download your findings as JSON for further analysis.

## Architecture

### Core Components

- **LLMProviderManager**: Handles multiple AI providers with fallback
- **AcademicSearchEngine**: Multi-database paper search with caching
- **ResearchGapAnalyzer**: Main analysis engine
- **PaperValidator**: Prevents fabricated results

### Data Flow

1. User input → Topic extraction
2. Topic → Query generation → Paper search
3. Papers → Gap analysis → Recommendations
4. Results → Export/Display

## Deployment

### Local Development
```bash
streamlit run integrated_research_gap_finder.py
```

### Production Deployment

#### Streamlit Cloud
1. Push to GitHub repository
2. Connect to Streamlit Cloud
3. Add secrets for API keys
4. Deploy

#### Docker (Coming Soon)
```dockerfile
# Dockerfile will be provided for containerized deployment
```

#### Heroku/Railway/Render
- Compatible with most Python hosting platforms
- Requires `requirements.txt` and proper port configuration

## API Rate Limits

The application respects API rate limits:
- **Semantic Scholar**: 100 requests/5 minutes
- **Crossref**: 50 requests/second (polite pool)
- **OpenAI**: Depends on your plan
- **Anthropic**: Depends on your plan

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   streamlit run integrated_research_gap_finder.py --server.port 8502
   ```

2. **API key errors**
   - Check `.env` file format
   - Verify API key validity
   - Ensure proper environment loading

3. **No papers found**
   - Try broader search terms
   - Check network connectivity
   - Verify API endpoints are accessible

4. **Slow performance**
   - Reduce concurrent searches
   - Check API rate limits
   - Consider caching optimization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Create a GitHub issue
- Check the troubleshooting section
- Review the logs for error details

## Acknowledgments

- Semantic Scholar API for academic paper data
- Crossref API for publication metadata
- OpenAI, Anthropic, and Google for AI capabilities
- Streamlit for the web framework
