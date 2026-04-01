# urbanride-ai-support-system

AI-powered customer support system for a taxi platform with:

- FastAPI backend
- React + Vite frontend
- Mock NLP and intent services for local development

## Project layout

```text
urbanride-ai-support-system/
	app/                  # Backend application code
	frontend/             # React frontend
	mocks/                # Mock NLP + intent APIs
	models/               # Local model artifact storage
		intent/             # Intent models
		nlp/                # NLP/translation models
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

## Start backend services

This starts:

- Main chatbot API on `8000`
- Mock intent API on `8001`
- Mock NLP API on `8002`

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

## Where to store models

Store model files in:

- `models/intent/`
- `models/nlp/`
- `models/shared/`

Suggested examples:

- `models/intent/model.joblib`
- `models/intent/labels.json`
- `models/nlp/translator.onnx`
- `models/shared/tokenizer.json`

By default, large model binaries are ignored in `.gitignore`.
