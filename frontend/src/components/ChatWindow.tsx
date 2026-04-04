import { useEffect, useRef } from 'react';
import type { Message } from '../types';
import { MessageBubble } from './MessageBubble';
import { TypingIndicator } from './TypingIndicator';
import { QuickReplies } from './QuickReplies';
import './ChatWindow.css';
import { useLanguage } from '../contexts/LanguageContext';

interface ChatWindowProps {
  messages: Message[];
  isLoading: boolean;
  showQuickReplies: boolean;
  onQuickReply: (text: string) => void;
  onSubOptionClick: (text: string) => void;
  onCallClick: () => void;
  onResolved: () => void;
}

export function ChatWindow({ messages, isLoading, showQuickReplies, onQuickReply, onSubOptionClick, onCallClick, onResolved }: ChatWindowProps) {
  const bottomRef = useRef<HTMLDivElement>(null);
  const { t } = useLanguage();

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  return (
    <div className="chat-window">
      {/* Date separator */}
      <div className="chat-window__date">
        <span>{t('chatWindow.today')}</span>
      </div>

      {/* Render messages */}
      {messages.map((msg, idx) => (
        <div key={msg.id}>
          <MessageBubble 
            message={msg} 
            onSubOptionClick={onSubOptionClick} 
            onCallClick={onCallClick} 
            onResolved={onResolved} 
          />
          {/* Quick replies appear below the first (welcome) bot message */}
          {idx === 0 && showQuickReplies && (
            <QuickReplies onSelect={onQuickReply} />
          )}
        </div>
      ))}

      {/* Typing indicator */}
      {isLoading && <TypingIndicator />}

      <div ref={bottomRef} />
    </div>
  );
}
