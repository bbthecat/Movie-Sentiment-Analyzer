from __future__ import annotations
from typing import List, Dict, Any

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
    try:
        from transformers import pipeline
        import os
        model_name = os.getenv("HF_MODEL_NAME", "distilbert-base-uncased-finetuned-sst-2-english")
        _pipeline = pipeline("sentiment-analysis", model=model_name)
        return _pipeline
    except Exception:
        _pipeline = None
        return None

def predict(texts: List[str]) -> List[Dict[str, Any]]:
    pipe = _get_pipeline()
    if pipe is None:
        return _fallback_predict(texts)
    
    # จำกัดความยาวของข้อความเพื่อป้องกัน token sequence ยาวเกินไป
    MAX_TEXT_LENGTH = 500  # ประมาณ 500 ตัวอักษรควรจะอยู่ภายใน 512 tokens
    truncated_texts = [text[:MAX_TEXT_LENGTH] if len(text) > MAX_TEXT_LENGTH else text for text in texts]
    
    try:
        results = pipe(truncated_texts)
        out = []
        for r in results:
            label = r.get("label", "").upper()
            score = float(r.get("score", 0.0))
            out.append({"label": label, "score": score})
        return out
    except Exception as e:
        print(f"Error in sentiment analysis: {str(e)}")
        # ใช้ fallback เมื่อเกิดข้อผิดพลาด
        return _fallback_predict(texts)
