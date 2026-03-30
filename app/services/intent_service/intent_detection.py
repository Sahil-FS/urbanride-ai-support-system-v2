import json
import os
import pickle
import re
from typing import Dict, Tuple

import torch  # type: ignore
import torch.nn.functional as F  # type: ignore
from fastapi import FastAPI  # type: ignore
from pydantic import BaseModel, Field  # type: ignore
from transformers import DistilBertForSequenceClassification, DistilBertTokenizerFast  # type: ignore


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_MODEL_PATH = os.path.join(BASE_DIR, "best_intent_model")
LABEL_ENCODER_PATH = os.path.join(BASE_DIR, "label_encoder.pkl")
ID2LABEL_PATH = os.path.join(BASE_DIR, "id2label.json")

MAX_LEN = 64
MAX_TEXT_CHARS = 1000
CONFIDENCE_THRESHOLD = 0.35


class DetectRequest(BaseModel):
    text: str = Field(..., description="Input text to classify")


class DetectResponse(BaseModel):
    intent: str
    confidence: float


def preprocess(text: str) -> str:
    text = str(text).strip().lower()
    contractions = {
        "can't": "cannot",
        "won't": "will not",
        "don't": "do not",
        "didn't": "did not",
        "isn't": "is not",
        "aren't": "are not",
        "wasn't": "was not",
        "weren't": "were not",
        "hasn't": "has not",
        "haven't": "have not",
        "hadn't": "had not",
        "i'm": "i am",
        "i've": "i have",
        "i'll": "i will",
        "i'd": "i would",
        "it's": "it is",
        "that's": "that is",
        "there's": "there is",
        "they're": "they are",
        "we're": "we are",
        "you're": "you are",
        "he's": "he is",
        "she's": "she is",
        "let's": "let us",
        "couldn't": "could not",
        "shouldn't": "should not",
        "wouldn't": "would not",
        "doesn't": "does not",
    }
    for k, v in contractions.items():
        text = text.replace(k, v)

    text = re.sub(r"[^\w\s!?.,'\\-]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def load_model(model_path: str) -> Tuple[DistilBertForSequenceClassification, DistilBertTokenizerFast, Dict[int, str], torch.device]:
    if not os.path.isdir(model_path):
        raise RuntimeError(f"Model directory not found: {model_path}")

    tokenizer = DistilBertTokenizerFast.from_pretrained(model_path)
    model = DistilBertForSequenceClassification.from_pretrained(model_path)
    model.eval()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    if os.path.exists(ID2LABEL_PATH):
        with open(ID2LABEL_PATH, "r", encoding="utf-8") as f:
            raw = json.load(f)
        id2label = {int(k): v for k, v in raw.items()}
    elif os.path.exists(LABEL_ENCODER_PATH):
        with open(LABEL_ENCODER_PATH, "rb") as f:
            le = pickle.load(f)
        id2label = {i: cls for i, cls in enumerate(le.classes_)}
    elif hasattr(model.config, "id2label") and model.config.id2label:
        id2label = {int(k): v for k, v in model.config.id2label.items()}
    else:
        raise RuntimeError("No label mapping found. Add label_encoder.pkl or id2label.json")

    return model, tokenizer, id2label, device


def predict(text: str) -> DetectResponse:
    safe_text = (text or "").strip()
    if not safe_text:
        return DetectResponse(intent="unknown_intent", confidence=0.0)  # type: ignore

    if len(safe_text) > MAX_TEXT_CHARS:
        safe_text = safe_text[:int(MAX_TEXT_CHARS)]  # type: ignore

    clean = preprocess(safe_text)
    if not clean:
        return DetectResponse(intent="unknown_intent", confidence=0.0)  # type: ignore

    enc = TOKENIZER(
        clean,
        return_tensors="pt",
        truncation=True,
        padding="max_length",
        max_length=MAX_LEN,
    )

    with torch.no_grad():
        logits = MODEL(
            input_ids=enc["input_ids"].to(DEVICE),
            attention_mask=enc["attention_mask"].to(DEVICE),
        ).logits

    probs = F.softmax(logits, dim=1).squeeze().cpu().numpy()
    best_idx = int(probs.argmax())
    confidence = float(probs[best_idx])
    intent = ID2LABEL.get(best_idx, f"label_{best_idx}")

    if confidence < CONFIDENCE_THRESHOLD:
        intent = "unknown_intent"

    confidence_val = float(confidence)
    return DetectResponse(intent=intent, confidence=round(confidence_val, 6))  # type: ignore


MODEL, TOKENIZER, ID2LABEL, DEVICE = load_model(DEFAULT_MODEL_PATH)

app = FastAPI(title="Intent Detection API", version="1.0.0")


@app.get("/")
def root() -> Dict[str, str]:
    return {"status": "ok", "message": "Use POST /detect for inference"}


@app.post("/detect", response_model=DetectResponse)
def detect(payload: DetectRequest) -> DetectResponse:
    return predict(payload.text)


if __name__ == "__main__":
    import uvicorn  # type: ignore

    uvicorn.run("intent_detection:app", host="0.0.0.0", port=8001, reload=False)