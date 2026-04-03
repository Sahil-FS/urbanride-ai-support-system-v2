import type { ChatApiResponse } from '../types';

const API_BASE = 'http://localhost:8000';

export async function sendChatMessage(
  message: string,
  originalText?: string,
  language: string = 'en'
): Promise<ChatApiResponse> {
  const response = await fetch(`${API_BASE}/api/v1/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message,
      original_text: originalText || message,
      language,
    }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error ${response.status}`);
  }

  const data = await response.json();
  return {
    ...data,
    subOptions: data.sub_options || [],
    showCallButton: data.show_call_button || false,
  } as ChatApiResponse;
}