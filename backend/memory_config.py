# การตั้งค่าสำหรับ Render free tier (512MB RAM)
# ใช้ RAM น้อยที่สุดเท่าที่เป็นไปได้

import os
import psutil

def get_memory_info():
    """ตรวจสอบ RAM ที่มี"""
    memory = psutil.virtual_memory()
    return {
        "total": memory.total / (1024**3),  # GB
        "available": memory.available / (1024**3),  # GB
        "used": memory.used / (1024**3),  # GB
        "percent": memory.percent
    }

def should_use_ai_model():
    """ตัดสินใจว่าจะใช้ AI model หรือไม่"""
    memory_info = get_memory_info()
    available_mb = memory_info["available"] * 1024  # แปลงเป็น MB
    
    # ถ้า RAM น้อยกว่า 400MB ให้ใช้ fallback
    if available_mb < 400:
        print(f"Not enough RAM ({available_mb:.1f}MB available), using fallback mode")
        return False
    
    print(f"RAM available: {available_mb:.1f}MB, using AI model")
    return True

def get_ultra_lightweight_config():
    """การตั้งค่าที่ประหยัด RAM สูงสุด"""
    return {
        "max_length": 32,  # ลด token length มาก
        "batch_size": 1,    # ประมวลผลทีละข้อความ
        "truncation": True,
        "return_all_scores": False,
        "device": -1,       # CPU only
        "torch_dtype": "float16",  # half precision
        "low_cpu_mem_usage": True,  # ประหยัด CPU memory
    }

def get_lightweight_model_name():
    """เลือก model ที่เบาที่สุด"""
    # ใช้ model ที่เบาที่สุดที่หาได้
    return "cardiffnlp/twitter-roberta-base-sentiment-latest"
