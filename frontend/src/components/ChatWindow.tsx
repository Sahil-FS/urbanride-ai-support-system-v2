import { useEffect, useRef, useState } from "react";

type Message = {
  id: string;
  role: "user" | "bot";
  message: string;
  options?: { label: string; intent: string }[];
  ticket_ref?: string;
};

type Props = {
  messages: Message[];
  onOptionClick: (intent: string, label: string) => void;
  onEscalate: () => void;
  loading: boolean;
  isTyping?: boolean;
};

export default function ChatWindow({
  messages,
  onOptionClick,
  onEscalate,
  loading,
  isTyping = false,
}: Props) {
  const bottomRef = useRef<HTMLDivElement | null>(null);
  const [clickedId, setClickedId] = useState<string | null>(null);

  const [showCallButton, setShowCallButton] = useState(false);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  useEffect(() => {
    setClickedId(null);
    setShowCallButton(false);
  }, [messages.length]);

  // Deduplicate messages (prevents double renders)
  const uniqueMessages = messages.filter((msg, index, self) => {
    return (
      index ===
      self.findIndex((m) => m.message === msg.message && m.role === msg.role)
    );
  });

  const shouldShowEscalation = (msg: Message, index: number) => {
    const text = msg.message.toLowerCase();

    const critical =
      text.includes("accident") ||
      text.includes("safety") ||
      text.includes("emergency") ||
      text.includes("refund not received") ||
      text.includes("payment failed") ||
      text.includes("driver misbehave");

    const frustration =
      uniqueMessages.length > 6 && index === uniqueMessages.length - 1;

    return critical || frustration;
  };

  // ✅ HELPFUL → send "helpful" to backend for clean state reset
  const handleHelpful = () => {
    onOptionClick("helpful", "helpful");
  };

  // ✅ NOT HELPFUL → send "not helpful" to backend
  const handleNotHelpful = () => {
    onOptionClick("not helpful", "not helpful");
  };

  // ✅ ESCALATE → call backend via onEscalate (already wired in App.tsx)
  const handleEscalateClick = () => {
    onEscalate();
  };

  return (
    <div className="flex-1 overflow-y-auto relative">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_30%,rgba(59,130,246,0.2),transparent),radial-gradient(circle_at_70%_70%,rgba(168,85,247,0.2),transparent)] blur-3xl" />

      <div className="relative px-6 py-4 space-y-3">
        {uniqueMessages.map((msg, msgIndex) => {
          if (!msg || !msg.message) return null;

          const isSameAsPrev =
            msgIndex > 0 &&
            uniqueMessages[msgIndex - 1].role === msg.role;

          const isUser = msg.role === "user";
          const isLast = msgIndex === uniqueMessages.length - 1;

          return (
            <div
              key={msg.id}
              className={`flex items-end gap-3 ${
                isUser ? "justify-end" : "justify-start"
              } ${
                !isSameAsPrev ? "mt-3" : "mt-1"
              } ${
                isLast ? "animate-fadeIn" : ""
              }`}
            >
              {!isUser && (
                <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center text-sm backdrop-blur">
                  🤖
                </div>
              )}

              <div
                className={`max-w-[70%] px-5 py-3 rounded-2xl text-sm shadow-md ${
                  isUser
                    ? "bg-gradient-to-r from-purple-600 to-pink-500 text-white rounded-br-none shadow-lg"
                    : "bg-gradient-to-br from-white/10 to-white/5 backdrop-blur-xl border border-white/10 text-gray-100 rounded-bl-none shadow-[0_0_25px_rgba(168,85,247,0.25)] glow-soft"
                }`}
              >
                {msg.message}

                {msg.ticket_ref && (
                  <div className="mt-3 text-xs bg-white/10 px-3 py-2 rounded-lg border border-white/10">
                    🎫 Ticket: {msg.ticket_ref}
                  </div>
                )}

                {/* OPTIONS */}
                {msg.options &&
                  msg.options.length > 0 &&
                  msgIndex === uniqueMessages.length - 1 && (
                    <div className="flex gap-2 mt-4 flex-wrap">
                      {msg.options.map((opt, idx) => {
                        const uniqueId = msg.id + "-" + idx;

                        return (
                          <button
                            key={uniqueId}
                            disabled={clickedId === uniqueId || loading}
                            onClick={() => {
                              setClickedId(uniqueId);
                              onOptionClick(opt.intent, opt.label);
                            }}
                            className="bg-white/10 border border-white/10 backdrop-blur px-4 py-1.5 rounded-full text-sm text-white hover:bg-purple-600 hover:scale-105 hover:shadow-lg transition-all"
                          >
                            {opt.label}
                          </button>
                        );
                      })}
                    </div>
                  )}

                {/* ESCALATE */}
                {msg.role === "bot" &&
                  msgIndex === uniqueMessages.length - 1 &&
                  shouldShowEscalation(msg, msgIndex) && (
                    <div className="flex gap-3 mt-4 flex-wrap">
                      <button
                        onClick={handleEscalateClick}
                        className="text-xs bg-gradient-to-r from-yellow-400 to-orange-500 px-3 py-1 rounded-full"
                      >
                        Escalate
                      </button>

                      <a
                        href="tel:+911234567890"
                        className="text-xs bg-gradient-to-r from-green-400 to-emerald-500 px-3 py-1 rounded-full"
                      >
                        Call Support
                      </a>
                    </div>
                  )}

                {/* FEEDBACK */}
                {msg.role === "bot" &&
                  msgIndex === uniqueMessages.length - 1 && (
                    <div className="flex gap-2 mt-3">
                      <button
                        onClick={handleHelpful}
                        className="text-xs bg-white/10 px-3 py-1 rounded-full hover:bg-white/20"
                      >
                        👍 Helpful
                      </button>

                      {!showCallButton ? (
                        <button
                          onClick={handleNotHelpful}
                          className="text-xs bg-red-500 px-3 py-1 rounded-full hover:bg-red-400"
                        >
                          👎 Not Helpful
                        </button>
                      ) : (
                        <a
                          href="tel:+911234567890"
                          className="text-xs bg-green-500 px-3 py-1 rounded-full"
                        >
                          📞 Call Support
                        </a>
                      )}
                    </div>
                  )}
              </div>

              {isUser && (
                <div className="w-8 h-8 rounded-full bg-purple-700 flex items-center justify-center text-sm">
                  👤
                </div>
              )}
            </div>
          );
        })}

        {/* TYPING INDICATOR */}
        {isTyping && (
          <div className="flex justify-start mt-3 animate-fadeIn">
            <div className="flex items-end gap-3">
              <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center text-sm backdrop-blur">
                🤖
              </div>
              <div className="bg-white/5 backdrop-blur-xl border border-white/10 px-5 py-3 rounded-2xl rounded-bl-none glow-soft text-sm text-gray-400">
                <span className="inline-flex gap-1">
                  <span className="animate-bounce" style={{ animationDelay: "0ms" }}>●</span>
                  <span className="animate-bounce" style={{ animationDelay: "150ms" }}>●</span>
                  <span className="animate-bounce" style={{ animationDelay: "300ms" }}>●</span>
                </span>
              </div>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>
    </div>
  );
}