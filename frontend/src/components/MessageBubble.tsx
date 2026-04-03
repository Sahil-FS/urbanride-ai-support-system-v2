import { useState } from 'react';
import type { Message } from '../types';
import './MessageBubble.css';
import { useLanguage } from '../contexts/LanguageContext';

interface MessageBubbleProps {
  message: Message;
  onSubOptionClick: (text: string) => void;
  onCallClick: () => void;
  onResolved?: () => void;
}

function formatTime(date: Date): string {
  return date.toLocaleTimeString('en-IN', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
  });
}

export function MessageBubble({
  message,
  onSubOptionClick,
  onCallClick,
  onResolved,
}: MessageBubbleProps) {
  const { t } = useLanguage();
  const isUser = message.role === 'user';

  const [optionsUsed, setOptionsUsed] = useState(false);
  const [callDone, setCallDone] = useState(false);
  const [needsHelpCallDone, setNeedsHelpCallDone] = useState(false);
  const [satisfactionState, setSatisfactionState] =
    useState<'idle' | 'resolved' | 'needsHelp'>('idle');

  const isFinalAnswer =
    !isUser &&
    (!message.subOptions || message.subOptions.length === 0) &&
    !message.showCallButton &&
    !message.isEscalation &&
    message.id !== 'welcome';

  const triggerCall = () => {
    onCallClick();
    const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
    if (isMobile) {
      window.location.href = 'tel:+919271035646';
    } else {
      alert(`Call us at: +91 92710 35646\n\nAvailable 24/7`);
    }
  };

  const renderApiCallButton = () => {
    if (callDone) {
      return (
        <div className="call-section">
          <p className="resolved-text">Connecting you to support...</p>
        </div>
      );
    }
    return (
      <div className="call-section">
        <button
          className="call-support-btn"
          onClick={() => {
            setCallDone(true);
            triggerCall();
          }}
        >
          {t('messageBubble.callSupport')}
        </button>
      </div>
    );
  };

  const renderSatisfactionCallButton = () => {
    if (needsHelpCallDone) {
      return (
        <div className="call-section">
          <p className="resolved-text">Connecting you to support...</p>
        </div>
      );
    }
    return (
      <div className="call-section">
        <button
          className="call-support-btn"
          onClick={() => {
            setNeedsHelpCallDone(true);
            triggerCall();
          }}
        >
          {t('messageBubble.callSupport')}
        </button>
      </div>
    );
  };

  return (
    <div className={`bubble-row ${isUser ? 'bubble-row--user' : 'bubble-row--bot'}`}>
      {!isUser && (
        <div className="bubble-avatar bubble-avatar--bot">
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M12 2a2 2 0 0 1 2 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 0 1 7 7H3a7 7 0 0 1 7-7h1V5.73c-.6-.34-1-.99-1-1.73a2 2 0 0 1 2-2z" />
            <path d="M9 14a1 1 0 0 1-2 0v-1a1 1 0 0 1 2 0v1z" />
            <path d="M17 14a1 1 0 0 1-2 0v-1a1 1 0 0 1 2 0v1z" />
            <path d="M3 21h18" />
            <path d="M5 18v3M19 18v3" />
          </svg>
        </div>
      )}

      <div className="bubble-content">
        {!isUser && <span className="bubble-sender">{t('header.title')}</span>}

        <div className={`bubble ${isUser ? 'bubble--user' : 'bubble--bot'}`}>
          <p className="bubble-text">{message.text}</p>
        </div>

        {!isUser &&
          message.subOptions &&
          message.subOptions.length > 0 &&
          !optionsUsed && (
            <div className="sub-options-container">
              {message.subOptions.map((option, index) => (
                <button
                  key={index}
                  className="sub-option-pill"
                  onClick={() => {
                    setOptionsUsed(true);
                    onSubOptionClick(option);
                  }}
                >
                  {option}
                </button>
              ))}
            </div>
          )}

        {!isUser && message.showCallButton && renderApiCallButton()}

        {isFinalAnswer && satisfactionState === 'idle' && (
          <div className="satisfaction-check">
            <span>Was this helpful?</span>
            <button
              className="satisfy-yes"
              onClick={() => {
                setSatisfactionState('resolved');
                onResolved?.();
              }}
            >
              {t('messageBubble.yes')}
            </button>
            <button
              className="satisfy-no"
              onClick={() => setSatisfactionState('needsHelp')}
            >
              {t('messageBubble.no')}
            </button>
          </div>
        )}

        {isFinalAnswer && satisfactionState === 'resolved' && (
          <p className="resolved-text">Glad we could help!</p>
        )}

        {isFinalAnswer &&
          satisfactionState === 'needsHelp' &&
          renderSatisfactionCallButton()}

        <span className="bubble-time">{formatTime(message.timestamp)}</span>
      </div>

      {isUser && <div className="bubble-avatar bubble-avatar--user">AK</div>}
    </div>
  );
}
