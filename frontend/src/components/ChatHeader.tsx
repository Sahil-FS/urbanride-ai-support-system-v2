import './ChatHeader.css';

interface ChatHeaderProps {
  onClearChat: () => void;
}

export function ChatHeader({ onClearChat }: ChatHeaderProps) {
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
            <h1 className="chat-header__name">Urban Taxi Support</h1>
            <span className="chat-header__online-dot" />
          </div>
          <p className="chat-header__subtitle">Online · Typically replies instantly</p>
        </div>
      </div>

      {/* Center label */}
      <div className="chat-header__center">
        <span className="chat-header__center-label">AI SUPPORT CHAT</span>
      </div>

      {/* Right: badge + actions */}
      <div className="chat-header__right">
        <span className="chat-header__badge">
          <span className="chat-header__badge-dot" />
          AI-POWERED
        </span>
        <button
          className="chat-header__action"
          aria-label="Clear chat"
          onClick={onClearChat}
          title="Clear conversation"
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
