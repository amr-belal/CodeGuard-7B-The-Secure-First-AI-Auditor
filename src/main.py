from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.core import load_llm ,get_chroma
import time
import uvicorn
from prometheus_fastapi_instrumentator import Instrumentator 
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("CodeGuard-API")


app = FastAPI(title="CodeGuard-7B API"  , description="API for CodeGuard-7B Enterprise Security Auditor", version="1.0.0")

Instrumentator().instrument(app).expose(app)


class CodeAuditRequest(BaseModel):
    code: str
    persona : str = "Security Auditor"


@app.post("/audit")
async def audit_code(request :CodeAuditRequest):
    logger.info(f"📥 Received audit request for code snippet...")
    start_time = time.time()
    try:
        if not request.code:
            raise HTTPException(status_code=400, detail="Code input is required.")
        
        cache = get_chroma()
        
        cached_report = cache.check_cache_or_add(request.code)
        
        if cached_report:
            return {"report": cached_report, "source": "cache"}
        
        llm = load_llm()
        
        prompt = f"System: You are a Security Auditor. Find vulnerabilities and provide a fix.\nUser: {request.code}\nAssistant:"
        
        output = llm(prompt, max_tokens=1024)
        
        response_text = output['choices'][0]['text']
        
        
        cache.check_cache_or_add(request.code, response_text=response_text)
        
        duration = time.time() - start_time
        logger.info(f"✅ Audit completed in {duration:.2f}s")
        return {"report": response_text, "source": "llm"}

    except Exception as e:
        logger.error(f"❌ Critical Failure: {str(e)}") # تسجيل الأخطاء
        raise HTTPException(status_code=500, detail="Inference Error")
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    