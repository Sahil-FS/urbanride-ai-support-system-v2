import { useEffect, useState } from "react";
import ChatWindow from "./components/ChatWindow";
import InputBar from "./components/InputBar";
import Sidebar from "./components/Sidebar";
import Header from "./components/Header";
import TicketsPanel from "./components/TicketsPanel";
import Settings from "./components/Settings";
import { sendChatMessage } from "./services/api";

type Message = {
  id: string;
  role: "user" | "bot";
  message: string;
  options?: { label: string; intent: string }[];
  ticket_ref?: string;
};

const intentToText: Record<string, string> = {
  TRACK_RIDE: "track ride",
  DRIVER_ISSUE: "driver issue",
  PAYMENT_ISSUE: "payment issue",
  CANCEL_RIDE: "cancel ride",
  REFUND_REQUEST: "refund request",
  SAFETY_CONCERN: "safety concern",
};

export default function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "bot",
      message:
        "Hello! 👋 I'm your Urban Taxi Support assistant. How can I help you today?",
      options: [
        { label: "Track Ride", intent: "TRACK_RIDE" },
        { label: "Driver Issue", intent: "DRIVER_ISSUE" },
        { label: "Payment Issue", intent: "PAYMENT_ISSUE" },
        { label: "Cancel Ride", intent: "CANCEL_RIDE" },
        { label: "Refund Request", intent: "REFUND_REQUEST" },
        { label: "Safety Concern", intent: "SAFETY_CONCERN" },
      ],
    },
  ]);

  const [loading, setLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const [isBackendUp, setIsBackendUp] = useState(true);
  const [language, setLanguage] = useState("English");

  // 🆕 screen state
  const [activeScreen, setActiveScreen] = useState<"chat" | "tickets" | "settings">("chat");

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/health");
        setIsBackendUp(res.ok);
      } catch {
        setIsBackendUp(false);
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, 5000);
    return () => clearInterval(interval);
  }, []);

  const normalizeInput = (text: string) => {
    const lower = text.toLowerCase();

    const issueKeywords = [
      "lost",
      "refund",
      "payment",
      "driver",
      "cancel",
      "issue",
      "problem",
      "accident",
      "safety",
    ];

    const hasIssue = issueKeywords.some((k) => lower.includes(k));

    return hasIssue ? text : text;
  };

  const handleSend = async (intentOrText: string, label?: string) => {
    if (loading) return;

    const messageToSend =
      intentToText[intentOrText] || normalizeInput(intentOrText);

    const userMsg: Message = {
      id: Date.now().toString(),
      role: "user",
      message: label || intentOrText,
    };

    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);
    setIsTyping(true);
    const startTime = Date.now();

    const hideTyping = () => {
      const elapsed = Date.now() - startTime;
      const delay = Math.max(500 - elapsed, 0);
      setTimeout(() => setIsTyping(false), delay);
    };

    try {
      const res = await sendChatMessage(messageToSend);

      hideTyping();

      if (!res) return;

      const botMsg: Message = {
        id: Date.now().toString(),
        role: "bot",
        message: res.message,
        options: res.next_options || [],
        ticket_ref: res.ticket_ref || undefined,
      };

      setMessages((prev) => [...prev, botMsg]);
    } catch {
      hideTyping();

      setMessages((prev) => [
        ...prev,
        {
          id: Date.now().toString(),
          role: "bot",
          message: "🚨 Server error. Please try again.",
        },
      ]);
    }

    setLoading(false);
  };

  // 🔥 FIXED escalation
  const handleEscalation = async () => {
    const res = await sendChatMessage("escalate");

    if (!res) return;

    const botMsg: Message = {
      id: Date.now().toString(),
      role: "bot",
      message: res.message,
      ticket_ref: res.ticket_ref || undefined,
    };

    setMessages((prev) => [...prev, botMsg]);
  };

  return (
    <div className="h-screen w-screen flex items-center justify-center bg-gradient-to-br from-[#0a0a0f] via-[#1a0b2e] to-[#0a0a0f] text-white">

      {/* 💎 Main Glass Card */}
      <div className="w-[95%] max-w-6xl h-[90vh] bg-white/5 backdrop-blur-xl border border-white/10 rounded-2xl shadow-[0_0_60px_rgba(168,85,247,0.2)] flex overflow-hidden">

        <Sidebar active={activeScreen} onNavigate={setActiveScreen} />

        <div className="flex flex-col flex-1 h-full overflow-hidden">

          <Header
            isBackendUp={isBackendUp}
            language={language}
            onLanguageChange={setLanguage}
          />

          {activeScreen === "chat" && (
            <>
              <ChatWindow
                messages={messages}
                onOptionClick={handleSend}
                onEscalate={handleEscalation}
                loading={loading}
                isTyping={isTyping}
              />

              <InputBar
                onSend={(text: string) => handleSend(text, text)}
                disabled={loading}
              />
            </>
          )}

          {activeScreen === "tickets" && <TicketsPanel />}

          {activeScreen === "settings" && <Settings />}

        </div>
      </div>
    </div>
  );
}