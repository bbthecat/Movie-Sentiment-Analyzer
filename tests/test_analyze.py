from backend.sentiment_hf import predict


def test_fallback_or_model():
    texts = [
        "I love this movie, it was amazing!",
        "This was boring and terrible.",
        "It exists."
    ]
    out = predict(texts)
    assert len(out) == 3
    labels = {o['label'] for o in out}
    assert labels  # non-empty
