import './QuickReplies.css';

export const QUICK_REPLIES = [
  { id: 'track',   label: '🚕 Track Ride' },
  { id: 'driver',  label: '👤 Driver Issue' },
  { id: 'payment', label: '💳 Payment Issue' },
  { id: 'cancel',  label: '❌ Cancel Ride' },
  { id: 'refund',  label: '💰 Refund Request' },
  { id: 'safety',  label: '🆘 Safety Concern' },
  { id: 'support', label: '📞 Talk to Support' },
];

interface QuickRepliesProps {
  onSelect: (text: string) => void;
}

export function QuickReplies({ onSelect }: QuickRepliesProps) {
  return (
    <div className="quick-replies">
      {QUICK_REPLIES.map((item) => (
        <button
          key={item.id}
          className="quick-reply-btn"
          onClick={() => onSelect(item.label)}
        >
          {item.label}
        </button>
      ))}
    </div>
  );
}
