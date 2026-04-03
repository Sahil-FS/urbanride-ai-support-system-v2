"""
intent_model.py — Local intent classification using XLM-R style multilingual models.
Loads model artifacts from models/intent.
"""

import logging
import os
from pathlib import Path
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from app.models.schemas import IntentResult

logger = logging.getLogger(__name__)

# Determine model path relative to this file
MODELS_DIR = Path(__file__).parent.parent.parent / "models" / "intent"

class IntentModel:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.id2label = {}
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"Using device: {self.device}")
        
    def load(self):
        """Load model and tokenizer from local files"""
        try:
            if not MODELS_DIR.exists():
                logger.error(f"Model directory not found: {MODELS_DIR}")
                return False
            
            logger.info(f"Loading intent model from {MODELS_DIR}...")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(str(MODELS_DIR))
            logger.info("Tokenizer loaded successfully")
            
            # Load model
            self.model = AutoModelForSequenceClassification.from_pretrained(str(MODELS_DIR))
            self.model.to(self.device)
            self.model.eval()
            logger.info("Model loaded successfully")
            
            # Load id2label mapping from config
            import json
            config_path = MODELS_DIR / "config.json"
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    self.id2label = config.get("id2label", {})
                    logger.info(f"Loaded {len(self.id2label)} intent labels")
            
            return True
        except Exception as e:
            logger.error(f"Failed to load intent model: {e}")
            return False
    
    def predict(self, text: str) -> IntentResult:
        """Classify text and return intent with confidence"""
        if self.model is None or self.tokenizer is None:
            logger.error("Model not loaded")
            return IntentResult(intent="unknown_intent", confidence=0.0)
        
        try:
            # Tokenize input
            inputs = self.tokenizer(
                text,
                truncation=True,
                padding=True,
                max_length=512,
                return_tensors="pt"
            )
            
            # Move to device
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Inference
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
                probabilities = torch.softmax(logits, dim=-1)
                confidence, predicted_id = torch.max(probabilities, dim=-1)
                
                intent_id = predicted_id.item()
                confidence_score = confidence.item()
                
                # Map ID to label
                intent_label = self.id2label.get(str(intent_id), "unknown_intent")
                
                logger.debug(f"Text: '{text}' -> Intent: {intent_label} (confidence: {confidence_score:.4f})")
                
                return IntentResult(
                    intent=intent_label,
                    confidence=confidence_score
                )
        
        except Exception as e:
            logger.error(f"Inference error: {e}")
            return IntentResult(intent="unknown_intent", confidence=0.0)


# Global instance
_intent_model = None

def get_intent_model() -> IntentModel:
    """Get or initialize the intent model (lazy loading)"""
    global _intent_model
    if _intent_model is None:
        _intent_model = IntentModel()
        _intent_model.load()
    return _intent_model
