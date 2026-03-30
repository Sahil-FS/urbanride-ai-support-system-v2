type Props = {
  active: string;
  onNavigate: (screen: "chat" | "tickets" | "settings") => void;
};

const btn = (isActive: boolean) =>
  `w-full text-left px-3 py-2 rounded-lg transition ${
    isActive ? "bg-purple-600 glow" : "hover:bg-white/10"
  }`;

export default function Sidebar({ active, onNavigate }: Props) {
  return (
    <div className="w-64 flex-shrink-0 h-full bg-gradient-to-b from-white/10 to-white/5 backdrop-blur-xl border-r border-white/10 p-4 flex flex-col justify-between shadow-[0_0_40px_rgba(168,85,247,0.15)]">

      {/* Top Section */}
      <div>
        <h1 className="text-xl font-bold mb-6">🚕 UrbanRide</h1>

        <div className="flex flex-col gap-2">
          <button onClick={() => onNavigate("chat")} className={btn(active === "chat")}>
            💬 Chat
          </button>

          <button onClick={() => onNavigate("tickets")} className={btn(active === "tickets")}>
            🎫 Tickets
          </button>

          <button onClick={() => onNavigate("settings")} className={btn(active === "settings")}>
            ⚙️ Settings
          </button>
        </div>
      </div>

      {/* Bottom User */}
      <div className="text-sm text-gray-400 border-t border-white/10 pt-4">
        👤 User
      </div>
    </div>
  );
}