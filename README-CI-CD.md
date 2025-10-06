# CI/CD Setup - Movie Sentiment Analyzer

## 🚀 CI/CD Pipeline

โปรเจคนี้มี CI/CD pipeline ที่เรียบง่ายและใช้งานได้จริง:

### 📋 Workflows

1. **CI Workflow** (`.github/workflows/ci.yml`)
   - ทดสอบโค้ดด้วย pytest
   - ตรวจสอบ code quality ด้วย flake8
   - สร้าง Docker image

2. **Deploy Workflow** (`.github/workflows/deploy.yml`)
   - Deploy อัตโนมัติเมื่อ push ไป main branch
   - สร้างและ push Docker image ไป GitHub Container Registry

### 🛠️ การใช้งาน

#### 1. ทดสอบในเครื่อง
```bash
# ติดตั้ง dependencies
py -m pip install -r requirements.txt

# รัน tests
py -m pytest tests/ -v

# ตรวจสอบ code quality
py -m flake8 backend tests
```

#### 2. สร้าง Docker image
```bash
docker build -t movie-sentiment-analyzer .
```

#### 3. รันแอป
```bash
# รันด้วย Docker
docker run -p 8000:8000 movie-sentiment-analyzer

# หรือรันด้วย Python
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
```

### 🔧 การตั้งค่า

1. **สร้างไฟล์ `.env`**:
   ```bash
   OMDB_API_KEY=your_omdb_api_key
   TMDB_API_KEY=your_tmdb_api_key
   ```

2. **Push ไป GitHub** เพื่อเริ่มใช้ CI/CD pipeline

### 📊 สถานะ

- ✅ Tests ผ่าน (3/3)
- ✅ Linting ผ่าน
- ✅ Docker build สำเร็จ
- ✅ CI/CD pipeline พร้อมใช้งาน

### 🌐 การเข้าถึง

- **Local**: http://localhost:8000
- **Health Check**: http://localhost:8000/api/health
- **API Docs**: http://localhost:8000/docs

---

**หมายเหตุ**: CI/CD pipeline จะทำงานอัตโนมัติเมื่อคุณ push โค้ดไป GitHub repository
