import { useState, useCallback, useRef } from 'react';
import './App.css';
import { Sidebar } from './components/Sidebar';
import { ChatHeader } from './components/ChatHeader';
import { ChatWindow } from './components/ChatWindow';
import { InputBar } from './components/InputBar';
import type { Message, BackendStatus } from './types';
import { sendChatMessage } from './services/api';

const WELCOME: Message = {
  id: 'welcome',
  role: 'bot',
  text: "Hello! 👋 I'm your Urban Taxi Support assistant. How can I help you today? You can ask me about your rides, billing, driver issues, or anything else related to your trip.",
  timestamp: new Date(),
};

function uid() {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 6)}`;
}

const INTENT_SHORTCUTS: Record<string, string> = {
  "sos emergency": "sos help emergency danger now",
  "accident report": "accident crash collision happened",
  "driver misbehavior": "driver rude misbehaved misconduct",
  "rash driving": "driver rash fast speed dangerous",
  "report this driver": "formally report this driver complaint",
  "driver not arrived": "driver not arrived waiting long time",
  "driver is late": "driver is late taking too long",
  "cannot contact driver": "cannot contact driver not answering unreachable",
  "contact driver": "contact my driver call message",
  "ask driver to start": "driver not starting trip begin ride",
  "update pickup pin": "update pickup location pin change",
  "cancel my current ride": "cancel ride now immediately current trip",
  "driver cancelled on me": "driver cancelled my ride on me",
  "cancellation fee issue": "cancellation fee charged unfair dispute",
  "cancel ride for free": "cancel ride free no charge waive",
  "dispute the fee": "dispute cancellation fee overcharged",
  "payment failed": "payment failed declined transaction error",
  "i was charged twice": "double payment charged twice duplicate charge",
  "wrong fare charged": "overcharged wrong fare extra money billed",
  "change payment method": "change payment card upi add new method",
  "dispute the fare": "dispute fare overcharged wrong amount billing",
  "dispute the charge": "dispute charge overcharged duplicate billing",
  "dispute the route": "wrong route dispute navigation taken",
  "check refund status": "refund status when will I get my money",
  "refund not received": "refund not received pending missing delayed",
  "request a new refund": "request new refund initiate money back process",
  "escalate my refund": "escalate refund urgent priority not received",
  "driver took long route": "long route unnecessary extra km taken",
  "call support now": "contact support agent human live call",
  "talk to support": "contact support agent human live call",
  "report issue": "report issue complaint formal submit",
  "report lost item": "lost item forgot left in cab report",
  "login problem": "login problem cannot sign in password otp",
  "update my profile": "update profile change details edit name",
  "retry the coupon": "retry coupon promo code again apply",
};

export default function App() {
  const [activeNav, setActiveNav] = useState('chat');
  const [messages, setMessages] = useState<Message[]>([WELCOME]);
  const [isLoading, setIsLoading] = useState(false);
  const [showQuickReplies, setShowQuickReplies] = useState(true);
  const [backendStatus, setBackendStatus] = useState<BackendStatus>('unknown');
  const [isResolved, setIsResolved] = useState(false);

  const hasEscalatedRef = useRef(false);
  const callButtonShownRef = useRef(false);
  const isLoadingRef = useRef(false);
  const botMessageCountRef = useRef(0);

  // Generates ticket message when call button is clicked
  const handleCallClick = useCallback(() => {
    const ticket = 'URB-' + Math.floor(1000 + Math.random() * 9000);
    setMessages(prev => [...prev, {
      id: uid(),
      role: 'bot',
      text: `Your complaint has been registered.\nTicket ID: ${ticket}\nOur team will assist you shortly.`,
      timestamp: new Date(),
      isEscalation: true,
    }]);
  }, []);

  // Called when customer clicks "Yes, resolved"
  const handleResolved = useCallback(() => {
    setIsResolved(true);
    hasEscalatedRef.current = true; // stop escalation after resolved
  }, []);

  const handleSend = useCallback(async (text: string) => {
    if (isLoadingRef.current) return;
    isLoadingRef.current = true;
    setIsLoading(true);

    setShowQuickReplies(false);

    const userMsg: Message = {
      id: uid(),
      role: 'user',
      text,
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, userMsg]);

    try {
      const originalText = text;
      const messageToSend = INTENT_SHORTCUTS[text.toLowerCase()] || text;

      const data = await sendChatMessage(messageToSend, originalText);
      setBackendStatus('connected');

      const apiShowCall = data.showCallButton || (data as any).show_call_button || false;
      const shouldShowCall = apiShowCall && !callButtonShownRef.current;
      if (shouldShowCall) callButtonShownRef.current = true;

      const botMessage: Message = {
        id: uid(),
        role: 'bot',
        text: data.response,
        timestamp: new Date(),
        subOptions: data.subOptions || (data as any).sub_options || [],
        showCallButton: shouldShowCall,
      };

      setMessages(msgs => [...msgs, botMessage]);

      // ── Escalation counter logic ───────────────────────────────────────────
      // Rule 1: Final answer (no pills, no call button from API)
      //         → customer got a resolution → reset counter to 0
      //         → "Was this helpful?" will appear in MessageBubble
      //         → if customer clicks "No still need help" → call button
      //            appears directly in that bubble (handled in MessageBubble)
      //
      // Rule 2: Bot gave pills or call button (still in flow)
      //         → increment counter
      //         → after 3 back-and-forth → auto escalation fires ONCE
      //
      // Rule 3: Auto escalation already fired or user resolved
      //         → never fire again

      const hasPills = (botMessage.subOptions?.length ?? 0) > 0;
      const isFinalAnswer = !hasPills && !shouldShowCall;

      {
        const prev = botMessageCountRef.current;
        // Final answer → reset, satisfaction check handles "still need help"
        if (isFinalAnswer) {
          botMessageCountRef.current = 0;
          return;
        }

        // Already escalated or resolved → don't count anymore
        if (hasEscalatedRef.current || isResolved) return;

        const newCount = prev + 1;
        if (newCount >= 3) {
          hasEscalatedRef.current = true;

          const showEscCallBtn = !callButtonShownRef.current;
          if (showEscCallBtn) callButtonShownRef.current = true;

          setTimeout(() => {
            setMessages(msgs => [...msgs, {
              id: Date.now().toString(),
              role: 'bot',
              text: 'I notice we have been going back and forth. Would you like to speak directly with a live support agent?',
              timestamp: new Date(),
              subOptions: [],
              showCallButton: showEscCallBtn,
              isEscalation: true,
            }]);
          }, 500);

          botMessageCountRef.current = 0;
          return;
        }
        botMessageCountRef.current = newCount;
      }

    } catch {
      setBackendStatus('offline');
      setMessages(prev => [...prev, {
        id: uid(),
        role: 'bot',
        text: 'Sorry, something went wrong. Please try again.',
        timestamp: new Date(),
      }]);
    } finally {
      isLoadingRef.current = false;
      setIsLoading(false);
    }
  }, [isResolved]);

  const handleClearChat = useCallback(() => {
    setMessages([WELCOME]);
    setShowQuickReplies(true);
    setBackendStatus('unknown');
    botMessageCountRef.current = 0;
    setIsResolved(false);
    setIsLoading(false);
    hasEscalatedRef.current = false;
    callButtonShownRef.current = false;
    isLoadingRef.current = false;
  }, []);

  return (
    <div className="app">
      <Sidebar
        activeNav={activeNav}
        onNavChange={setActiveNav}
        backendStatus={backendStatus}
      />
      <main className="app__main">
        <ChatHeader onClearChat={handleClearChat} />
        <ChatWindow
          messages={messages}
          isLoading={isLoading}
          showQuickReplies={showQuickReplies}
          onQuickReply={handleSend}
          onSubOptionClick={handleSend}
          onCallClick={handleCallClick}
          onResolved={handleResolved}
        />
        <InputBar onSend={handleSend} disabled={isLoading} />
      </main>
    </div>
  );
}