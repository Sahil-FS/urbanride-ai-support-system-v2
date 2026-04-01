export type MessageRole = 'user' | 'bot';
export type BackendStatus = 'unknown' | 'connected' | 'offline';

export interface Message {
  id: string;
  role: MessageRole;
  text: string;
  timestamp: Date;
  subOptions?: string[];
  showCallButton?: boolean;
  isEscalation?: boolean;
}

export interface ChatApiRequest {
  message: string;
}

export interface ChatApiResponse {
  intent: string;
  response: string;
  confidence: number;
  sub_options?: string[];
  show_call_button?: boolean;
  /** Mapped camelCase versions (populated by api.ts) */
  subOptions?: string[];
  showCallButton?: boolean;
}
