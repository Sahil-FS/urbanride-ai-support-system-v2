# urbanride-ai-support-system

AI-powered customer support system for a taxi platform with:

- FastAPI backend
- React + Vite frontend
- Local multilingual intent model (XLM-R) running in-process
- English, Marathi, and Hindi conversation support

## Project layout

```text
urbanride-ai-support-system/
	app/                  # Backend application code
	frontend/             # React frontend
	models/               # Local model artifact storage
		intent/             # XLM-R intent model artifacts
		nlp/                # Optional future NLP artifacts
		shared/             # Shared assets (tokenizers, labels, etc.)
```

Important: `app/models/` is for Python schema code, not ML binary files.

## Prerequisites

- Python 3.10+
- Node.js 18+
- npm 9+

## One-time setup

From repository root:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

Set-Location frontend
npm install
Set-Location ..
```

## Start backend service

This starts a single backend service:

- Main chatbot API on `8000`

```powershell
.\.venv\Scripts\Activate.ps1
python run_all.py

```

Backend docs: `http://localhost:8000/docs`

## Start frontend

Open a second terminal:

```powershell
Set-Location frontend
npm run dev
```

Frontend URL: `http://localhost:5173`

## Quick health checks

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/health"
```

```powershell
$body = @{ message = 'Driver Not Arrived'; original_text = 'Driver Not Arrived' } | ConvertTo-Json
Invoke-RestMethod -Uri 'http://localhost:8000/api/v1/chat' -Method Post -ContentType 'application/json' -Body $body
```

```powershell
$body = @{ message = 'पेमेंट समस्या'; original_text = 'पेमेंट समस्या'; language = 'mr' } | ConvertTo-Json
Invoke-RestMethod -Uri 'http://localhost:8000/api/v1/chat' -Method Post -ContentType 'application/json' -Body $body
```

```powershell
$body = @{ message = 'भुगतान समस्या'; original_text = 'भुगतान समस्या'; language = 'hi' } | ConvertTo-Json
Invoke-RestMethod -Uri 'http://localhost:8000/api/v1/chat' -Method Post -ContentType 'application/json' -Body $body
```

## Runtime architecture

Current backend pipeline is local and self-contained:

- Raw user input (English or Marathi)
- Input normalization (quick-reply canonicalization)
- Intent inference using local XLM-R model from `models/intent/`
- Decision tree response generation with sub-option flow
- Final response localization based on requested language

No external NLP API calls are required.

## Where to store models

Store model files in:

- `models/intent/`
- `models/nlp/`
- `models/shared/`

Suggested examples:

- `models/intent/model.safetensors`
- `models/intent/config.json`
- `models/intent/tokenizer.json`
- `models/shared/tokenizer.json`

By default, large model binaries are ignored in `.gitignore`.
