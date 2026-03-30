type Props = {
  isBackendUp: boolean;
  language: string;
  onLanguageChange: (lang: string) => void;
};

export default function Header({ isBackendUp, language, onLanguageChange }: Props) {
  return (
    <div className="px-6 py-4 flex justify-between items-center bg-gradient-to-r from-white/10 to-white/5 backdrop-blur-xl border-b border-white/10 shadow-[0_0_30px_rgba(168,85,247,0.15)]">
      <div className="font-semibold text-lg tracking-wide">
        🚖 UrbanRide Support
      </div>

      <div className="flex items-center gap-5">
        <div className="flex items-center gap-2 text-sm">
          <span
            className={`w-2.5 h-2.5 rounded-full ${
              isBackendUp ? "bg-green-400" : "bg-red-500"
            }`}
          />
          <span>{isBackendUp ? "Online" : "Offline"}</span>
        </div>

        <select
          value={language}
          onChange={(e) => onLanguageChange(e.target.value)}
          className="bg-black/30 backdrop-blur-xl text-white text-sm px-3 py-1 rounded-lg border border-white/10 outline-none cursor-pointer hover:bg-white/10 transition"
        >
          <option>English</option>
          <option>Hindi</option>
          <option>Marathi</option>
        </select>
      </div>
    </div>
  );
}
