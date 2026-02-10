# import streamlit as st
# from llama_cpp import Llama
# import time
# import os
# import sys
# from database.chroma_conf import ChromaConf
# from src.core import load_llm, get_chroma

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# #  streamlit app.py
# st.set_page_config(page_title="CodeGuard-7B Enterprise", page_icon="🛡️", layout="wide")

# # cache for chroma client
# @st.cache_resource
# def get_chroma():
#     return ChromaConf(db_path="./data/chroma_db")

# # cache for LLM model loading
# @st.cache_resource
# def load_llm():
#     model_path = "/mnt/d/summer-2026/MyModels/CodeGaurd/Meta-Llama-3.1-8B-Instruct.Q4_K_M.gguf"
#     return Llama(model_path=model_path, n_ctx=2048, n_gpu_layers=-1)

# # UI Layout
# st.title("🛡️ CodeGuard-7B: Enterprise Security Dashboard")
# st.markdown("---")

# # Sidebar for system status and role
# with st.sidebar:
#     st.header("System Status")
#     st.success("LLM: Llama-3.1-8B Loaded ✅")
#     st.success("Cache: ChromaDB Active ✅")
#     st.divider()
#     st.info("Role: Principal AI Architect Mode")
    
    

# # User Input
# code_input = st.text_area("Paste Python Code to Audit:", height=250)

# if st.button("🚀 Run AI Audit"):
#     if code_input:
#         db = get_chroma()
#         cached_result = db.check_cache_or_add(code_input)
        
#         # check cache first
#         # this will return the cached report if a similar code snippet is found, otherwise it will return None
#         # cached_report = cache.check_cache_or_add(code_input)
        
#         # if cached_report:
#         #     st.warning("⚡ Instant Insight (Found in Semantic Cache)")
#         #     st.markdown(cached_report)
#         if cached_result:
#             st.success("⚡ Found in Memory Cache!")
#             st.markdown(cached_result)
        
#         else:
#             # Step 2: If not found in cache, run the LLM to get a new audit report
#             with st.spinner("🔍 Deep Analysis by CodeGuard-7B..."):
#                 llm = load_llm()
#                 prompt = f"System: You are a Security Auditor. Find vulnerabilities and provide a fix.\nUser: {code_input}\nAssistant:"
                
#                 start_time = time.time()
#                 output = llm(prompt, max_tokens=1024)
#                 response_text = output['choices'][0]['text']
#                 end_time = time.time()
                
#                 # after getting the response from LLM, add it to cache for future reference
#                 db.check_cache_or_add(code_input, response_text=response_text)
                
#                 st.subheader("🛡️ Audit Report")
#                 st.markdown(response_text)
#                 st.caption(f"Inference Time: {end_time - start_time:.2f}s")
#     else:
#         st.error("Please provide code to analyze!")


import streamlit as st
import requests
import time

# إعداد الصفحة كأول أمر في السكربت
st.set_page_config(
    page_title="CodeGuard-7B Enterprise",
    page_icon="🛡️",
    layout="wide"
)

# CSS بسيط لتحسين شكل التقارير
st.markdown("""
    <style>
    .report-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #1e2130;
        border: 1px solid #3d4466;
    }
    </style>
""", unsafe_allow_html=True)

# UI Layout
st.title("🛡️ CodeGuard-7B: Enterprise Security Dashboard")
st.info("Role: Principal AI Architect Mode | Connected to AI Inference Engine via API")
st.markdown("---")

# Sidebar للتحقق من حالة النظام
with st.sidebar:
    st.header("Infrastructure Status")
    st.success("Frontend: Streamlit Active ✅")
    st.success("Backend: FastAPI Engine Linked ✅")
    st.divider()
    st.caption("Project: CodeGuard-7B v1.0")

# منطقة إدخال الكود
code_input = st.text_area("Paste Python Code to Audit:", height=300, placeholder="Write your code here...")

if st.button("🚀 Run AI Audit"):
    if code_input:
        # Spinner يوضح إننا بنكلم السيرفر
        with st.spinner("🛰️ Communicating with AI Inference Cluster..."):
            try:
                # إرسال الطلب للـ API باستخدام اسم الخدمة في دوكر
                # ملاحظة: نستخدم 'api' لأن Docker Compose يعرّف الخدمات بأسماءها في الشبكة الداخلية
                start_time = time.time()
                response = requests.post(
                    "http://api:8000/audit", 
                    json={"code": code_input},
                    timeout=300 # وقت انتظار كافي للموديلات الكبيرة
                )
                
                if response.status_code == 200:
                    result = response.json()
                    end_time = time.time()
                    
                    # عرض النتائج
                    st.subheader(f"🛡️ Audit Report (Source: {result['source'].upper()})")
                    st.markdown(result['report'])
                    
                    st.divider()
                    st.caption(f"⏱️ Round-trip Time: {end_time - start_time:.2f}s")
                else:
                    st.error(f"❌ API Error ({response.status_code}): {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("🚨 Connection Failed: Ensure the 'api' container is running on port 8000.")
            except Exception as e:
                st.error(f"⚠️ Unexpected Error: {str(e)}")
    else:
        st.warning("Please provide a code snippet to analyze.")