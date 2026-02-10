### Virtual env :
```python
python3 -m venv .venv
source .venv/bin/activate

```

### run docker image 
```bash
docker run -p 8501:8501 \
  -v "/mnt/d/summer-2026/MyModels/CodeGaurd:/app/models" \
  -v "/mnt/d/summer-2026/CodeGuard-7B The Secure First AI Auditor/CodeGuard-7B-The-Secure-First-AI-Auditor/data:/app/data" \
  --name codeguard-instance \
  codeguard-app
  
```