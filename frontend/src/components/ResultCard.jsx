import { useState } from "react"

// Yeh component short URL result dikhata hai
// Copy button bhi isi mein hai

export default function ResultCard({ result }) {
  const [copied, setCopied] = useState(false)

  async function handleCopy() {
    await navigator.clipboard.writeText(result.short_url)
    setCopied(true)
    // 2 second baad "Copied!" wapas "Copy" ho jaata hai
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="w-full bg-violet-50 border border-violet-200 rounded-2xl p-5 space-y-4">

      {/* Short URL + Copy button */}
      <div className="flex items-center justify-between gap-3">
        <div>
          <p className="text-xs text-gray-400 mb-1">Your short URL</p>
          <a
            href={result.short_url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-violet-600 font-semibold hover:underline break-all"
          >
            {result.short_url}
          </a>
        </div>
        <button
          onClick={handleCopy}
          className={`px-4 py-2 rounded-xl text-sm font-medium transition-all whitespace-nowrap
            ${copied
              ? "bg-green-500 text-white"
              : "bg-violet-600 hover:bg-violet-700 text-white"
            }`}
        >
          {copied ? "✓ Copied!" : "Copy"}
        </button>
      </div>

      {/* Original URL — truncated */}
      <div>
        <p className="text-xs text-gray-400 mb-1">Original URL</p>
        <p className="text-sm text-gray-500 truncate">{result.original_url}</p>
      </div>

      {/* Stats row */}
      <div className="flex gap-6 pt-2 border-t border-violet-100">
        <div>
          <p className="text-xs text-gray-400">Short ID</p>
          <p className="text-sm font-mono font-semibold text-gray-700">{result.short_id}</p>
        </div>
        <div>
          <p className="text-xs text-gray-400">Clicks</p>
          <p className="text-sm font-semibold text-gray-700">{result.clicks}</p>
        </div>
        <div>
          <p className="text-xs text-gray-400">Expires in</p>
          <p className="text-sm font-semibold text-gray-700">7 days</p>
        </div>
      </div>

    </div>
  )
}