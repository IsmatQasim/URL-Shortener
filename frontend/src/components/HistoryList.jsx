// Yeh component session ki history dikhata hai
// (Page refresh hone par clear ho jaati hai — localStorage nahi use kar rahe abhi)

export default function HistoryList({ history }) {
  if (history.length === 0) return null

  return (
    <div className="w-full mt-6">
      <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wide mb-3">
        Recent — This Session
      </h2>

      <div className="space-y-2">
        {/* Naye URLs upar dikhao — isliye reverse kiya */}
        {[...history].reverse().map((item) => (
          <div
            key={item.short_id}
            className="flex items-center justify-between bg-white border 
                       border-gray-100 rounded-xl px-4 py-3 gap-3"
          >
            {/* Left side — URLs */}
            <div className="min-w-0">
              <a
                href={item.short_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-violet-600 text-sm font-medium hover:underline"
              >
                {item.short_url}
              </a>
              <p className="text-xs text-gray-400 truncate mt-0.5">
                {item.original_url}
              </p>
            </div>

            {/* Right side — clicks badge */}
            <span className="text-xs bg-violet-100 text-violet-600 
                             px-2 py-1 rounded-lg whitespace-nowrap font-medium">
              {item.clicks} clicks
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}