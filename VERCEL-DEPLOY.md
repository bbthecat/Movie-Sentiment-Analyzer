# Deploy to Vercel Guide

## 🚀 การ Deploy Movie Sentiment Analyzer ลง Vercel

### 📋 ข้อกำหนดเบื้องต้น

1. **Vercel Account**: สมัครที่ [vercel.com](https://vercel.com)
2. **GitHub Repository**: โปรเจคต้องอยู่ใน GitHub
3. **API Keys**: OMDb และ TMDb API keys

### 🔧 การเตรียมโปรเจค

#### 1. ไฟล์ที่จำเป็น
- ✅ `vercel.json` - Vercel configuration
- ✅ `app.py` - Main FastAPI application
- ✅ `requirements-vercel.txt` - Python dependencies
- ✅ `env.vercel.example` - Environment variables template

#### 2. Environment Variables
สร้างไฟล์ `.env.local` สำหรับ local development:
```bash
cp env.vercel.example .env.local
```

แก้ไข `.env.local`:
```bash
OMDB_API_KEY=your_actual_omdb_api_key
TMDB_API_KEY=your_actual_tmdb_api_key
TRAKT_CLIENT_ID=your_actual_trakt_client_id
HF_MODEL_NAME=distilbert-base-uncased-finetuned-sst-2-english
DATA_DIR=/tmp/data
```

### 🌐 การ Deploy

#### วิธีที่ 1: ผ่าน Vercel Dashboard

1. **เข้า Vercel Dashboard**:
   - ไปที่ [vercel.com/dashboard](https://vercel.com/dashboard)
   - คลิก "New Project"

2. **Import GitHub Repository**:
   - เลือก "Import Git Repository"
   - เลือก repository ของคุณ
   - คลิก "Import"

3. **ตั้งค่า Project**:
   - **Framework Preset**: Other
   - **Root Directory**: `./` (default)
   - **Build Command**: (ว่าง)
   - **Output Directory**: (ว่าง)

4. **Environment Variables**:
   - คลิก "Environment Variables"
   - เพิ่มตัวแปรต่อไปนี้:
     ```
     OMDB_API_KEY = your_omdb_api_key
     TMDB_API_KEY = your_tmdb_api_key
     TRAKT_CLIENT_ID = your_trakt_client_id
     HF_MODEL_NAME = distilbert-base-uncased-finetuned-sst-2-english
     DATA_DIR = /tmp/data
     ```

5. **Deploy**:
   - คลิก "Deploy"
   - รอให้ build เสร็จ

#### วิธีที่ 2: ผ่าน Vercel CLI

1. **ติดตั้ง Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel
   ```

4. **Set Environment Variables**:
   ```bash
   vercel env add OMDB_API_KEY
   vercel env add TMDB_API_KEY
   vercel env add TRAKT_CLIENT_ID
   vercel env add HF_MODEL_NAME
   vercel env add DATA_DIR
   ```

### 🧪 การทดสอบ

#### 1. Health Check
```bash
curl https://your-app.vercel.app/api/health
```

#### 2. API Documentation
เปิดเบราว์เซอร์ไปที่:
```
https://your-app.vercel.app/docs
```

#### 3. ทดสอบ Sentiment Analysis
```bash
curl -X POST "https://your-app.vercel.app/api/analyze-text" \
     -H "Content-Type: application/json" \
     -d '{"text": "I love this movie!"}'
```

### ⚠️ ข้อจำกัดของ Vercel

1. **Serverless Functions**:
   - จำกัดเวลา execution: 10 วินาที (Hobby), 60 วินาที (Pro)
   - จำกัด memory: 1024MB
   - จำกัด payload size: 4.5MB

2. **File System**:
   - ใช้ `/tmp` directory สำหรับ temporary files
   - ไฟล์จะหายไปเมื่อ function จบการทำงาน

3. **Cold Start**:
   - การโหลด model อาจใช้เวลานาน
   - ใช้ caching เพื่อลด cold start

### 🔧 การปรับแต่ง

#### 1. เพิ่ม Timeout
แก้ไข `vercel.json`:
```json
{
  "functions": {
    "app.py": {
      "maxDuration": 60
    }
  }
}
```

#### 2. เพิ่ม Caching
```python
# ใน app.py
from functools import lru_cache

@lru_cache(maxsize=1)
def get_model():
    return load_sentiment_model()
```

#### 3. Error Handling
```python
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )
```

### 📊 Monitoring

1. **Vercel Analytics**:
   - ดู performance metrics
   - ตรวจสอบ error rates

2. **Function Logs**:
   - ดู logs ใน Vercel dashboard
   - ใช้ `vercel logs` command

### 🚨 Troubleshooting

#### 1. Build Failures
- ตรวจสอบ `requirements-vercel.txt`
- ตรวจสอบ Python version compatibility

#### 2. Runtime Errors
- ตรวจสอบ environment variables
- ดู function logs

#### 3. Timeout Issues
- ลดขนาด model
- ใช้ model caching
- เพิ่ม maxDuration

### 🎯 Best Practices

1. **Environment Variables**:
   - ใช้ Vercel dashboard สำหรับ production
   - ใช้ `.env.local` สำหรับ development

2. **Dependencies**:
   - ใช้ `requirements-vercel.txt` แทน `requirements.txt`
   - ลดขนาด dependencies ให้มากที่สุด

3. **Performance**:
   - Cache models และ heavy computations
   - ใช้ async/await สำหรับ I/O operations

4. **Security**:
   - ไม่ commit API keys
   - ใช้ environment variables

### 📈 Scaling

1. **Vercel Pro Plan**:
   - เพิ่ม timeout เป็น 60 วินาที
   - เพิ่ม memory เป็น 3008MB
   - เพิ่ม bandwidth

2. **Edge Functions**:
   - ใช้สำหรับ lightweight operations
   - ลด latency

3. **Database Integration**:
   - ใช้ Vercel Postgres
   - ใช้ external databases

---

**หมายเหตุ**: Vercel เหมาะสำหรับ API endpoints และ serverless functions แต่ไม่เหมาะสำหรับ long-running processes หรือ heavy ML models
