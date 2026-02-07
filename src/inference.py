# import torch
# from transformers import AutoTokenizer, AutoModelForCausalLM
# from peft import PeftModel

# def run_hybrid_audit(vulnerable_code):
#     # الموديل الأساسي - نسخة الـ 1B (حجم صغير جداً للماك)
#     base_model_id = "meta-llama/Llama-3.2-1B-Instruct"
#     adapter_path = "./models/my_adapter" 

#     print("🍏 Loading Lightweight Base (2GB) + Your Custom Adapter (52MB)...")
    
#     tokenizer = AutoTokenizer.from_pretrained(base_model_id)
    
#     # تحميل الموديل الصغير على الـ GPU بتاع الماك
#     base_model = AutoModelForCausalLM.from_pretrained(
#         base_model_id,
#         torch_dtype=torch.float16,
#         device_map="auto" 
#     )

#     # دمج تعبك (الـ Adapter) فوق الموديل الصغير
#     model = PeftModel.from_pretrained(base_model, adapter_path)
#     model = model.to("mps") # قوة الماك الـ Native

#     prompt = f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\nAudit this code for security:\n{vulnerable_code}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
#     inputs = tokenizer(prompt, return_tensors="pt").to("mps")

#     print("🔍 CodeGuard is analyzing...")
#     with torch.no_grad():
#         outputs = model.generate(**inputs, max_new_tokens=200)
    
#     return tokenizer.decode(outputs[0], skip_special_tokens=True)

# if __name__ == "__main__":
#     test_code = "exec(request.args.get('cmd'))"
#     print(run_hybrid_audit(test_code))