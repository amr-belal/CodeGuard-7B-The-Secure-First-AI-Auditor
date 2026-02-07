import os 
import pandas as pd 
from datasets import Dataset
from huggingface_hub import  login
from dotenv import load_dotenv


load_dotenv()

login(token=os.getenv("HF_TOKEN"))

file_path = "data/processed/dpo_dataset_100.parquet"
df = pd.read_parquet(file_path)

ds = Dataset.from_pandas(df)

ds.push_to_hub("CodeGuard-DPO-100",  private=True)
print("🚀 Dataset uploaded successfully to Hugging Face!")