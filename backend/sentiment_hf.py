from __future__ import annotations
from typing import List, Dict, Any
import os
import gc  # สำหรับ garbage collection

def _fallback_predict(texts: List[str]) -> List[Dict[str, Any]]:
    out = []
    pos_words = {"good", "great", "love", "amazing", "stunning", "awesome", "breathtaking", "fantastic", "enjoyed"}
    neg_words = {"bad", "boring", "slow", "terrible", "awful", "overhyped", "hate", "dull", "disappointing"}
    for t in texts:
        tl = t.lower()
        p = sum(w in tl for w in pos_words)
        n = sum(w in tl for w in neg_words)
        if p > n:
            out.append({"label": "POSITIVE", "score": 0.85})
        elif n > p:
            out.append({"label": "NEGATIVE", "score": 0.85})
        else:
            out.append({"label": "NEUTRAL", "score": 0.60})
    return out

_pipeline = None

def _get_pipeline():
    global _pipeline
    if _pipeline is not None:
        return _pipeline
    # Lightweight mode skips HF model to save memory
    if os.getenv("LIGHTWEIGHT_MODE", "0") in {"1", "true", "True"}:
        _pipeline = None
        return None
    try:
        from transformers import pipeline
        from .lightweight_models import get_lightweight_model, get_optimized_config
        
        # เลือก model ที่เหมาะสมกับ RAM
        model_name = get_lightweight_model()
        if model_name is None:
            print("Not enough RAM for AI model, using fallback mode")
            _pipeline = None
            return None
            
        # ใช้การตั้งค่าที่เหมาะสม
        config = get_optimized_config()
        
        _pipeline = pipeline(
            "sentiment-analysis",
            model=model_name,
            **config
        )
        return _pipeline
    except Exception:
        _pipeline = None
        return None

def predict(texts: List[str]) -> List[Dict[str, Any]]:
    pipe = _get_pipeline()
    if pipe is None:
        return _fallback_predict(texts)
    
    # จำกัดความยาวของข้อความเพื่อประหยัด memory
    MAX_TEXT_LENGTH = 128  # ลดจาก 500 เป็น 128
    truncated_texts = [text[:MAX_TEXT_LENGTH] if len(text) > MAX_TEXT_LENGTH else text for text in texts]
    
    try:
        # ประมวลผลทีละข้อความเพื่อประหยัด memory
        out = []
        for text in truncated_texts:
            try:
                result = pipe(text)  # ประมวลผลทีละข้อความ
                if isinstance(result, list):
                    result = result[0]  # เอาแค่ผลลัพธ์แรก
                
                label = result.get("label", "").upper()
                score = float(result.get("score", 0.0))
                out.append({"label": label, "score": score})
            except Exception as e:
                print(f"Error processing text: {str(e)}")
                # ใช้ fallback สำหรับข้อความนี้
                out.append(_fallback_predict([text])[0])
        
        # ทำ garbage collection เพื่อประหยัด memory
        gc.collect()
        return out
    except Exception as e:
        print(f"Error in sentiment analysis: {str(e)}")
        # ใช้ fallback เมื่อเกิดข้อผิดพลาด
        return _fallback_predict(texts)
