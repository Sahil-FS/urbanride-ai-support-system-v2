import { useState } from "react";

type Props = {
  onSend: (text: string) => void;
  disabled?: boolean;
};

export default function InputBar({ onSend, disabled }: Props) {
  const [input, setInput] = useState("");

  const startVoice = () => {
    const recognition = new (window as any).webkitSpeechRecognition();
    recognition.lang = "en-IN";

    recognition.onresult = (e: any) => {
      setInput(e.results[0][0].transcript);
    };

    recognition.start();
  };

  const handleSubmit = () => {
    if (!input.trim() || disabled) return;
    onSend(input);
    setInput("");
  };

  return (
    <div className="p-4 border-t border-white/10 bg-white/5 backdrop-blur-xl">
      <div className="max-w-4xl mx-auto">

        <div className="flex items-center gap-3 bg-gradient-to-r from-white/10 to-white/5 backdrop-blur-xl border border-white/10 rounded-full px-4 py-2 shadow-[0_0_25px_rgba(168,85,247,0.2)] glow-soft">

          <input
            className="flex-1 bg-transparent text-white outline-none px-2 text-sm focus:ring-0 placeholder-gray-400"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Describe your issue..."
            disabled={disabled}
            onKeyDown={(e) => {
              if (e.key === "Enter") handleSubmit();
            }}
          />

          <button onClick={startVoice} className="p-2 rounded-full hover:bg-white/10">
            🎤
          </button>

          <button
            onClick={handleSubmit}
            disabled={disabled}
            className="bg-gradient-to-r from-purple-600 to-pink-500 p-2 rounded-full hover:scale-105 transition disabled:opacity-40"
          >
            ➤
          </button>

        </div>

      </div>
    </div>
  );
}