FROM python:3.12-slim

# 1. تثبيت أدوات البناء الضرورية
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. نسخ ملف المتطلبات
COPY requirements.txt .

# 3. (الخدعة الهندسية) تثبيت نسخة CPU من Torch أولاً لتوفير 800 ميجا
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# 4. تثبيت باقي المكتبات مع زيادة وقت الانتظار (Timeout) لـ 1000 ثانية
RUN pip install --no-cache-dir --default-timeout=1000 -r requirements.txt

# 5. نسخ باقي الكود
COPY . .

EXPOSE 8501

ENV PYTHONPATH=/app

CMD ["streamlit", "run", "src/app.py", "--server.port=8501", "--server.address=0.0.0.0"]