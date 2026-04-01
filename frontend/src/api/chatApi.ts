const API_BASE = 'http://localhost:8000';

export interface ChatRequest {
  message: string;
}

export interface ChatResponse {
  intent: string;
  response: string;
  confidence: number;
}

export async function sendMessage(message: string): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/api/v1/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message } satisfies ChatRequest),
  });

  if (!res.ok) {
    throw new Error(`HTTP ${res.status}`);
  }

  return res.json() as Promise<ChatResponse>;
}
