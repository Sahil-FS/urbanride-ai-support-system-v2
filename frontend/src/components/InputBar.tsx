import { useState, useRef, type KeyboardEvent } from 'react';
import './InputBar.css';
import { useLanguage } from '../contexts/LanguageContext';

interface InputBarProps {
  onSend: (text: string) => void;
  disabled: boolean;
}

export function InputBar({ onSend, disabled }: InputBarProps) {
  const [text, setText] = useState('');
  const fileRef = useRef<HTMLInputElement>(null);
  const { t } = useLanguage();

  const handleSend = () => {
    const trimmed = text.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setText('');
  };

  const handleKey = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const canSend = text.trim().length > 0 && !disabled;

  return (
    <div className="input-bar">
      <div className="input-bar__shell">
        {/* Image upload */}
        <button
          className="input-bar__icon-btn"
          aria-label={t('inputBar.uploadImage')}
          onClick={() => fileRef.current?.click()}
          disabled={disabled}
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" width="19" height="19">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
            <circle cx="8.5" cy="8.5" r="1.5"/>
            <polyline points="21 15 16 10 5 21"/>
          </svg>
        </button>
        <input ref={fileRef} type="file" accept="image/*" className="sr-only" aria-label={t('inputBar.uploadImage')} />

        {/* Textarea */}
        <textarea
          id="chat-input"
          className="input-bar__field"
          placeholder={t('inputBar.placeholder')}
          value={text}
          rows={1}
          disabled={disabled}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={handleKey}
          aria-label={t('inputBar.placeholder')}
        />

        {/* Mic */}
        <button className="input-bar__icon-btn" aria-label={t('inputBar.voiceMessage')} disabled={disabled}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" width="19" height="19">
            <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/>
            <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
            <line x1="12" y1="19" x2="12" y2="23"/>
            <line x1="8" y1="23" x2="16" y2="23"/>
          </svg>
        </button>

        {/* Send */}
        <button
          id="send-btn"
          className={`input-bar__send ${canSend ? 'input-bar__send--active' : ''}`}
          onClick={handleSend}
          disabled={!canSend}
          aria-label={t('inputBar.placeholder')}
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" width="16" height="16">
            <line x1="22" y1="2" x2="11" y2="13"/>
            <polygon points="22 2 15 22 11 13 2 9 22 2"/>
          </svg>
        </button>
      </div>
      <p className="input-bar__hint">Press <kbd>Enter</kbd> {t('inputBar.hintEnter').split('Enter')[0]} · <kbd>Shift+Enter</kbd> {t('inputBar.hintShift').toLowerCase()}</p>
    </div>
  );
}
