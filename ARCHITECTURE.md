# Architecture Overview

This project uses a local, single-service backend architecture for multilingual taxi support.

## High-level flow

1. Frontend sends chat payload to `POST /api/v1/chat`.
2. Backend normalizes user input for stable routing.
3. Local XLM-R intent model predicts intent from normalized text.
4. Rule-based decision tree resolves response strategy:
   - direct answer
   - sub-options for deeper troubleshooting
   - emergency/call escalation
5. Response and sub-options are localized based on selected language (`en` or `mr`).
6. Frontend renders message, follow-up pills, and escalation actions.

## Components

- `frontend/`: React + Vite UI and multilingual UX.
- `app/api/routes/chat.py`: Main chat endpoint and pipeline orchestration.
- `app/services/intent_model.py`: Local model loading and inference.
- `app/services/intent_client.py`: Input preprocessing and intent call wrapper.
- `app/services/chatbot_engine.py`: Decision tree, sub-options, escalation rules.
- `app/services/translation_service.py`: Label normalization and response localization.
- `models/intent/`: XLM-R model artifacts (`model.safetensors`, tokenizer, config).

## Language handling

- Supported user-facing languages: English (`en`) and Marathi (`mr`).
- Quick replies are canonicalized so icon and non-icon variants map consistently.
- Parent intents (for example, payment/cancel/refund/safety) always return follow-up options in the selected language.

## External dependencies and calls

- No external NLP microservice is required for runtime.
- Inference runs in-process with local model artifacts.

## Runtime ports

- Backend API: `8000`
- Frontend (Vite dev): `5173`

## Operational notes

- Keep `CONFIDENCE_THRESHOLD` calibrated to your trained model output range.
- If you retrain the model, validate confidence distribution before adjusting threshold.
- Use structured logging from chat route and decision tree when debugging intent regressions.
