import type { BackendStatus } from '../types';
import './Sidebar.css';
import { useLanguage } from '../contexts/LanguageContext';

interface SidebarProps {
  activeNav: string;
  onNavChange: (id: string) => void;
  backendStatus: BackendStatus;
}

export function Sidebar({ activeNav, onNavChange, backendStatus }: SidebarProps) {
  const { t } = useLanguage();

  const navItems = [
    {
      id: 'chat', label: t('sidebar.navChat'),
      icon: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>,
    },
    {
      id: 'help', label: t('sidebar.navHelp'),
      icon: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>,
    },
    {
      id: 'rides', label: t('sidebar.navComplaints'),
      icon: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="1" y="3" width="15" height="13" rx="2"/><path d="M16 8h4l3 5v3h-7V8z"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>,
    },
    {
      id: 'settings', label: t('sidebar.navSettings'),
      icon: <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>,
    },
  ];

  const statusLabel =
    backendStatus === 'connected' ? 'Backend Connected' :
    backendStatus === 'offline'   ? 'Backend Offline' :
    'Checking...';

  return (
    <aside className="sidebar">
      {/* Logo */}
      <div className="sidebar-logo">
        <div className="sidebar-logo__icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <rect x="1" y="3" width="15" height="13" rx="2"/>
            <path d="M16 8h4l3 5v3h-7V8z"/>
            <circle cx="5.5" cy="18.5" r="2.5"/>
            <circle cx="18.5" cy="18.5" r="2.5"/>
          </svg>
        </div>
        <span className="sidebar-logo__name">Urban<span className="sidebar-logo__accent">Ride</span></span>
      </div>

      {/* Menu label */}
      <p className="sidebar-section-label">MAIN MENU</p>

      {/* Nav */}
      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <button
            key={item.id}
            className={`sidebar-nav__item ${activeNav === item.id ? 'sidebar-nav__item--active' : ''}`}
            onClick={() => onNavChange(item.id)}
          >
            <span className="sidebar-nav__icon">{item.icon}</span>
            <span className="sidebar-nav__label">{item.label}</span>
            {activeNav === item.id && <span className="sidebar-nav__indicator" />}
          </button>
        ))}
      </nav>

      <div className="sidebar__spacer" />

      {/* Backend status */}
      <div className={`sidebar-status sidebar-status--${backendStatus}`}>
        <span className="sidebar-status__dot" />
        <span className="sidebar-status__label">{statusLabel}</span>
      </div>

      {/* User profile */}
      <div className="sidebar-profile">
        <div className="sidebar-profile__avatar">AK</div>
        <div className="sidebar-profile__info">
          <p className="sidebar-profile__name">Aditya Kumar</p>
          <p className="sidebar-profile__role">Rider · Mumbai</p>
        </div>
        <button className="sidebar-profile__menu" aria-label="Profile options">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" width="14" height="14">
            <circle cx="12" cy="5" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="12" cy="19" r="1"/>
          </svg>
        </button>
      </div>
    </aside>
  );
}
