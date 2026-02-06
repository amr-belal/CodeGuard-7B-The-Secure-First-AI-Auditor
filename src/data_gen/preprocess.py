import json
import os 
from datasets import Dataset

def convert_to_dpo_format(input_path, output_path):
    if not os.path.exists(input_path):
        print(f"❌ Error: File {input_path} not found!")
        return

    with open(input_path, "r") as f:
        raw_data = json.load(f)

    prompts, chosens, rejecteds = [], [], []
    skipped_count = 0

    for i, item in enumerate(raw_data):
        try:
            # التأكد من وجود المفاتيح وأن القيم نصوص
            p = item.get("prompt")
            c = item.get("chosen")
            r = item.get("rejected")

            if p and c and r:
                # التحويل الإجباري لنص (في حال كان الموديل أرسل dict بالخطأ)
                prompts.append(str(p) if not isinstance(p, str) else p)
                chosens.append(str(c) if not isinstance(c, str) else c)
                rejecteds.append(str(r) if not isinstance(r, str) else r)
            else:
                skipped_count += 1
        except Exception:
            skipped_count += 1

    if not prompts:
        print("❌ No valid data to save.")
        return

    # إنشاء الـ Dataset
    formatted_data = {
        "prompt": prompts,
        "chosen": chosens,
        "rejected": rejecteds
    }
    
    dataset = Dataset.from_dict(formatted_data)

    # حفظ البيانات
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    dataset.to_parquet(output_path)
    
    print(f"✅ Cleaned & Converted: {len(prompts)} samples.")
    print(f"⚠️ Skipped: {skipped_count} samples.")

if __name__ == "__main__":
    input_file = "data/raw/full_dataset_100.json"
    output_file = "data/processed/dpo_dataset_100.parquet"
    convert_to_dpo_format(input_file, output_file)