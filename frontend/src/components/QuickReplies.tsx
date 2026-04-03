import './QuickReplies.css';
import { useLanguage } from '../contexts/LanguageContext';

const QUICK_REPLIES_KEYS = [
  { id: 'track', key: 'quickReplies.trackRide' },
  { id: 'driver', key: 'quickReplies.driverIssue' },
  { id: 'payment', key: 'quickReplies.paymentIssue' },
  { id: 'cancel', key: 'quickReplies.cancelRide' },
  { id: 'refund', key: 'quickReplies.refundRequest' },
  { id: 'safety', key: 'quickReplies.safetyConcern' },
  { id: 'support', key: 'quickReplies.talkToSupport' },
];

interface QuickRepliesProps {
  onSelect: (text: string) => void;
}

export function QuickReplies({ onSelect }: QuickRepliesProps) {
  const { t } = useLanguage();

  return (
    <div className="quick-replies">
      {QUICK_REPLIES_KEYS.map((item) => (
        <button
          key={item.id}
          className="quick-reply-btn"
          onClick={() => onSelect(t(item.key))}
        >
          {t(item.key)}
        </button>
      ))}
    </div>
  );
}
