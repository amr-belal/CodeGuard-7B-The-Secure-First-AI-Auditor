# src/core.py
from llama_cpp import Llama
from database.chroma_conf import ChromaConf
import os
from functools import lru_cache

# غيرنا الاسم لـ load_llm عشان main.py يشوفه
@lru_cache(maxsize=1)
def load_llm(): 
    print("⚙️ Loading LLM Model (Core Version)...")
    # تأكد من اسم الموديل بتاعك هنا
    model_path = "/app/models/Meta-Llama-3.1-8B-Instruct.Q4_K_M.gguf" 
    return Llama(model_path=model_path, n_ctx=512, n_gpu_layers=-1)

# غيرنا الاسم لـ get_chroma
def get_chroma():
    return ChromaConf(db_path="/app/data/chroma_db")