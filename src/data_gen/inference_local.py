from llama_cpp import Llama

# مسار ملف الـ GGUF اللي أنت لسه منزله
# model_path = r"D:\summer-2026\MyModels\CodeGaurd\Meta-Llama-3.1-8B-Instruct.Q4_K_M.gguf"
model_path = "/mnt/d/summer-2026/MyModels/CodeGaurd/Meta-Llama-3.1-8B-Instruct.Q4_K_M.gguf"

print("🚀 Loading CodeGuard-7B into RAM...")

# تحميل الموديل
llm = Llama(
    model_path=model_path,
    n_ctx=2048,             # حجم الكود اللي يقدر يقرأه
    n_gpu_layers=-1,        # استخدم كارت الشاشة بالكامل (-1 يعني كله)
    verbose=False
)

def audit_my_code(user_code):
    # الـ Prompt اللي الموديل اتدرب عليه
    prompt = f"System: You are a Security Auditor. Find vulnerabilities and provide a fix.\nUser: {user_code}\nAssistant:"
    
    print("🔍 Analyzing security...")
    output = llm(prompt, max_tokens=512, stop=["User:", "\n"], echo=False)
    return output['choices'][0]['text']

if __name__ == "__main__":
    # كود اختبار فيه ثغرة SQL Injection
    test_code = "query = 'SELECT * FROM users WHERE id = ' + user_input"
    result = audit_my_code(test_code)
    print("\n🛡️ CodeGuard Report:\n", result)