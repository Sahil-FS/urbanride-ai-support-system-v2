export default function TicketsPanel() {
  return (
    <div className="flex-1 overflow-y-auto p-6">
      <h2 className="text-lg font-semibold mb-4">Your Tickets</h2>

      <div className="bg-white/10 backdrop-blur-md p-4 rounded-lg border border-white/10 text-sm text-gray-200">
        🎫 Ticket ID: <span className="font-mono">URB-202603-30313</span>
        <div className="text-xs text-gray-400 mt-1">Status: Open · Driver Unreachable</div>
      </div>

      <div className="mt-4 text-xs text-gray-500">
        Full ticket history will appear here once the ticket API is integrated.
      </div>
    </div>
  );
}
