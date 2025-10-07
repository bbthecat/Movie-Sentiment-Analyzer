# Lightweight Hugging Face Models สำหรับ RAM น้อย
# ใช้ได้ใน Render free tier (512MB RAM)

LIGHTWEIGHT_MODELS = {
    # Model ที่เบาที่สุด (ใช้ RAM ~200MB)
    "tiny": "cardiffnlp/twitter-roberta-base-sentiment-latest",
    
    # Model ขนาดกลาง (ใช้ RAM ~400MB)  
    "small": "distilbert-base-uncased-finetuned-sst-2-english",
    
    # Model ขนาดเล็ก (ใช้ RAM ~300MB)
    "micro": "nlptown/bert-base-multilingual-uncased-sentiment",
    
    # Model สำหรับภาษาไทย (ใช้ RAM ~350MB)
    "thai": "microsoft/DialoGPT-medium"
}

# การตั้งค่าสำหรับ Render free tier
RENDER_FREE_TIER_CONFIG = {
    "max_length": 128,        # ลด token length
    "batch_size": 1,         # ประมวลผลทีละข้อความ
    "truncation": True,       # ตัดข้อความยาว
    "return_all_scores": False,  # ประหยัด memory
    "device": -1,            # ใช้ CPU เท่านั้น
}

def get_lightweight_model():
    """เลือก model ที่เหมาะสมกับ RAM ที่มี"""
    import psutil
    
    # ตรวจสอบ RAM ที่มี
    available_memory = psutil.virtual_memory().available / (1024**3)  # GB
    
    if available_memory < 0.3:  # น้อยกว่า 300MB
        return None  # ใช้ fallback mode
    elif available_memory < 0.4:  # 300-400MB
        return LIGHTWEIGHT_MODELS["tiny"]
    elif available_memory < 0.5:  # 400-500MB
        return LIGHTWEIGHT_MODELS["small"]
    else:  # มากกว่า 500MB
        return LIGHTWEIGHT_MODELS["micro"]

def get_optimized_config():
    """ได้การตั้งค่าที่เหมาะสมกับ RAM"""
    return RENDER_FREE_TIER_CONFIG
