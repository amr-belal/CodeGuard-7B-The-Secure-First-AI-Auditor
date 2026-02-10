# CodeGuard-7B: The Secure-First AI Auditor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

An enterprise-grade AI-powered security auditor built with Direct Preference Optimization (DPO) to identify vulnerabilities and provide secure code fixes in real-time.

## 🎯 Overview

CodeGuard-7B is a specialized large language model fine-tuned for security code auditing. It leverages DPO training to distinguish between secure and insecure coding patterns, providing developers with instant security feedback and remediation suggestions.

### Key Features

- **Real-time Security Auditing**: Analyze code snippets for vulnerabilities instantly
- **Intelligent Caching**: ChromaDB-powered semantic caching for faster repeat queries
- **Production Monitoring**: Built-in Prometheus metrics and Grafana dashboards
- **API & Dashboard**: RESTful API and interactive Streamlit interface
- **Container-Ready**: Fully Dockerized with docker-compose orchestration
- **DPO Training Pipeline**: Complete workflow for generating security-focused training data

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Streamlit     │────▶│   CodeGuard-7B   │────▶│   ChromaDB      │
│   Dashboard     │     │   LLM Engine     │     │   Cache Layer   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │
                               ▼
┌─────────────────┐     ┌──────────────────┐
│   FastAPI       │────▶│   Prometheus     │────▶ Grafana Dashboard
│   REST API      │     │   Monitoring     │
└─────────────────┘     └──────────────────┘
```

## 📋 Prerequisites

- Python 3.12+
- Docker & Docker Compose
- 4GB+ RAM (8GB recommended)
- Linux/macOS/WSL2 for development

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/amr-belal/codeguard-7b-the-secure-first-ai-auditor.git
cd codeguard-7b-the-secure-first-ai-auditor
```

### 2. Environment Setup

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Add your API keys:

```env
GROQ_API_KEY="your_groq_api_key_here"
HF_TOKEN="your_huggingface_token_here"  # Optional, for dataset upload
```

### 3. Running with Docker Compose (Recommended)

The easiest way to get started is using Docker Compose, which orchestrates all services:

```bash
docker-compose up --build
```

This will start:
- **Dashboard**: http://localhost:8501 (Streamlit UI)
- **API**: http://localhost:8000 (FastAPI endpoints)
- **Prometheus**: http://localhost:9090 (Metrics)
- **Grafana**: http://localhost:3000 (Visualization - default login: admin/admin)

### 4. Running Individual Services

#### Option A: Docker (Manual)

```bash
# Build the image
docker build -t codeguard-app .

# Run the dashboard
docker run -p 8501:8501 \
  -v "$(pwd)/models:/app/models" \
  -v "$(pwd)/data:/app/data" \
  --name codeguard-instance \
  codeguard-app
```

#### Option B: Local Development

```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run src/app.py

# Or run the API (in a separate terminal)
python src/main.py
```

## 📡 API Usage

### Audit Endpoint

**Endpoint**: `POST /audit`

**Request Body**:
```json
{
  "code": "import os\npassword = 'admin123'\ndb_connect(password)",
  "persona": "Security Auditor"
}
```

**Response**:
```json
{
  "report": "**VULNERABILITY FOUND**: Hardcoded credentials detected...\n**FIX**: Use environment variables...",
  "source": "llm"  // or "cache" if found in ChromaDB
}
```

**Example with cURL**:
```bash
curl -X POST http://localhost:8000/audit \
  -H "Content-Type: application/json" \
  -d '{"code": "password = \"admin123\""}'
```

**Example with Python**:
```python
import requests

response = requests.post(
    "http://localhost:8000/audit",
    json={"code": "password = 'admin123'"}
)
print(response.json()["report"])
```

## 🧪 Data Generation Pipeline

CodeGuard-7B includes a complete pipeline for generating security-focused training data using DPO (Direct Preference Optimization).

### 1. Generate Security Scenarios

```bash
python src/data_gen/generate.py
```

This creates 100 security vulnerability scenarios covering:
- Web frameworks (Flask, Django)
- Cloud services (AWS, Azure)
- Cryptography
- Operating system security
- Data science libraries

Output: `data/raw/full_dataset_100.json`

### 2. Preprocess for DPO Training

```bash
python src/data_gen/preprocess.py
```

Converts raw data into DPO format with three columns:
- `prompt`: User's security-related request
- `rejected`: Insecure implementation
- `chosen`: Secure implementation

Output: `data/processed/dpo_dataset_100.parquet`

### 3. Upload to Hugging Face (Optional)

```bash
python src/data_gen/upload.py
```

Uploads the processed dataset to your Hugging Face account.

## 🏛️ Project Structure

```
codeguard-7b/
├── src/
│   ├── app.py                 # Streamlit dashboard
│   ├── main.py                # FastAPI application
│   ├── core.py                # LLM initialization logic
│   ├── inference.py           # Inference utilities
│   └── data_gen/
│       ├── generate.py        # DPO dataset generation
│       ├── preprocess.py      # Data formatting
│       └── upload.py          # HuggingFace upload
├── database/
│   └── chroma_conf.py         # ChromaDB configuration
├── tests/
│   └── test_data_gen.py       # Unit tests
├── docker-compose.yml         # Multi-service orchestration
├── dockerfile                 # Container definition
├── requirements.txt           # Python dependencies
├── prometheus.yml             # Metrics configuration
└── pyproject.toml            # Project metadata
```

## 🔍 Features in Detail

### Semantic Caching with ChromaDB

CodeGuard uses vector similarity search to cache audit results:

```python
# Automatically checks cache before LLM inference
cache = ChromaConf()
cached_result = cache.check_cache_or_add(code_snippet)

if cached_result:
    return cached_result  # Instant response
else:
    # Generate new audit and cache it
    audit = llm.audit(code_snippet)
    cache.check_cache_or_add(code_snippet, audit)
```

**Benefits**:
- Sub-second response for similar code patterns
- Reduces inference costs by 60-80%
- Configurable similarity threshold (default: 0.6)

### Monitoring & Observability

#### Prometheus Metrics

Access raw metrics at: `http://localhost:8000/metrics`

Key metrics tracked:
- Request count and latency
- Cache hit/miss ratio
- Model inference time
- Error rates

#### Grafana Dashboards

Login at `http://localhost:3000` (admin/admin) to visualize:
- Real-time request throughput
- P95/P99 latency percentiles
- Cache efficiency trends
- System resource usage

## 🧰 Development

### Code Quality Checks

The project uses GitHub Actions for automated quality gates:

```bash
# Run linting locally
black --check .
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

# Run tests
pytest tests/
```

### Adding New Features

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make changes and add tests
3. Ensure all checks pass: `pytest && black . && flake8 .`
4. Submit a pull request to `develop` branch

## 🐛 Troubleshooting

### Common Issues

**Issue**: Container fails to start with "Port already in use"

**Solution**: 
```bash
# Check what's using the port
lsof -i :8501  # or :8000, :9090, :3000
# Kill the process or change ports in docker-compose.yml
```

**Issue**: Out of memory during model loading

**Solution**:
```bash
# Increase Docker memory limit to 8GB
# Docker Desktop → Settings → Resources → Memory
```

**Issue**: ChromaDB cache not working

**Solution**:
```bash
# Ensure data directory is mounted correctly
docker run -v "$(pwd)/data:/app/data" ...

# Check permissions
chmod -R 755 data/
```

## 📊 Performance Benchmarks

| Metric | Value |
|--------|-------|
| Average Inference Time | 1.2s - 3.5s |
| Cache Hit Rate | 65-75% (after warmup) |
| Throughput | ~30 requests/min (single container) |
| Model Size | ~4.3GB (GGUF quantized) |

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Ensure code quality checks pass
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [llama.cpp](https://github.com/ggerganov/llama.cpp) for efficient inference
- Powered by [ChromaDB](https://www.trychroma.com/) for semantic caching
- UI framework: [Streamlit](https://streamlit.io/)
- Monitoring: [Prometheus](https://prometheus.io/) + [Grafana](https://grafana.com/)

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/amr-belal/codeguard-7b/issues)
- **Discussions**: [GitHub Discussions](https://github.com/amr-belal/codeguard-7b/discussions)
- **Email**: your.email@example.com

## 🗺️ Roadmap

- [ ] Support for additional programming languages (Go, Rust, TypeScript)
- [ ] Integration with GitHub Actions for PR comments
- [ ] VSCode extension for inline security hints
- [ ] Fine-tuned models for specific frameworks (Django, FastAPI, etc.)
- [ ] Multi-file project analysis
- [ ] SARIF output format for CI/CD integration

---

**Built with ❤️ by Amr Belal** | [GitHub](https://github.com/amr-belal) | [LinkedIn](https://linkedin.com/in/amr-belal)
