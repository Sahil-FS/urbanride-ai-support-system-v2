import { useState } from 'react';
import './ChatHeader.css';
import { useLanguage } from '../contexts/LanguageContext';

interface ChatHeaderProps {
  onClearChat: () => void;
}

export function ChatHeader({ onClearChat }: ChatHeaderProps) {
  const { language, setLanguage, t } = useLanguage();
  const [showLanguageDropdown, setShowLanguageDropdown] = useState(false);

  const handleLanguageChange = (lang: 'en' | 'mr') => {
    setLanguage(lang);
    setShowLanguageDropdown(false);
  };

  return (
    <header className="chat-header">
      {/* Left: bot info */}
      <div className="chat-header__left">
        <div className="chat-header__avatar">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <rect x="1" y="3" width="15" height="13" rx="2"/>
            <path d="M16 8h4l3 5v3h-7V8z"/>
            <circle cx="5.5" cy="18.5" r="2.5"/>
            <circle cx="18.5" cy="18.5" r="2.5"/>
          </svg>
        </div>
        <div className="chat-header__bot-info">
          <div className="chat-header__name-row">
            <h1 className="chat-header__name">{t('header.title')}</h1>
            <span className="chat-header__online-dot" />
          </div>
          <p className="chat-header__subtitle">{t('header.subtitle')}</p>
        </div>
      </div>

      {/* Center label */}
      <div className="chat-header__center">
        <span className="chat-header__center-label">{t('header.aiLabel')}</span>
      </div>

      {/* Right: badge + actions */}
      <div className="chat-header__right">
        <span className="chat-header__badge">
          <span className="chat-header__badge-dot" />
          {t('header.badge')}
        </span>

        {/* Language Selector */}
        <div className="chat-header__language-selector">
          <button
            className="chat-header__language-btn"
            aria-label="Change language"
            onClick={() => setShowLanguageDropdown(!showLanguageDropdown)}
            title="Select language"
          >
            🌐 {language.toUpperCase()}
          </button>
          {showLanguageDropdown && (
            <div className="chat-header__language-dropdown">
              <button
                className={`chat-header__language-option ${language === 'en' ? 'active' : ''}`}
                onClick={() => handleLanguageChange('en')}
              >
                English
              </button>
              <button
                className={`chat-header__language-option ${language === 'mr' ? 'active' : ''}`}
                onClick={() => handleLanguageChange('mr')}
              >
                मराठी
              </button>
            </div>
          )}
        </div>

        <button
          className="chat-header__action"
          aria-label={t('header.clearBtn')}
          onClick={onClearChat}
          title={t('header.clearBtn')}
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" width="17" height="17">
            <polyline points="3 6 5 6 21 6"/>
            <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>
            <path d="M10 11v6M14 11v6"/>
            <path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/>
          </svg>
        </button>
      </div>
    </header>
  );
}
