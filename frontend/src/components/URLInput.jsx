import { useState } from "react"

// Yeh component sirf ek kaam karta hai:
// User se URL lena aur parent ko dena

export default function URLInput({ onShorten, isLoading }) {
  const [longUrl, setLongUrl] = useState("")
  const [customAlias, setCustomAlias] = useState("")
  const [showAlias, setShowAlias] = useState(false)

  function handleSubmit(e) {
    e.preventDefault() // Page reload rokta hai

    // Basic validation
    if (!longUrl.trim()) return

    // Parent component (App.jsx) ko data do
    onShorten(longUrl, customAlias)
  }

  return (
    <form onSubmit={handleSubmit} className="w-full space-y-3">

      {/* Long URL input */}
      <div className="flex gap-2">
        <input
          type="url"
          value={longUrl}
          onChange={(e) => setLongUrl(e.target.value)}
          placeholder="https://very-long-url.com/paste-here"
          required
          className="flex-1 px-4 py-3 rounded-xl border border-gray-200 
                     focus:outline-none focus:ring-2 focus:ring-violet-400
                     text-gray-700 text-sm"
        />
        <button
          type="submit"
          disabled={isLoading}
          className="px-6 py-3 bg-violet-600 hover:bg-violet-700 
                     text-white font-semibold rounded-xl transition-all
                     disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? "..." : "Shorten"}
        </button>
      </div>

      {/* Custom alias toggle */}
      <button
        type="button"
        onClick={() => setShowAlias(!showAlias)}
        className="text-sm text-violet-500 hover:text-violet-700 transition-colors"
      >
        {showAlias ? "− Remove custom alias" : "+ Add custom alias (optional)"}
      </button>

      {/* Custom alias input — sirf tab dikhao jab user ne toggle kiya */}
      {showAlias && (
        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-400 whitespace-nowrap">
            localhost:8000/
          </span>
          <input
            type="text"
            value={customAlias}
            onChange={(e) => setCustomAlias(e.target.value.toLowerCase().replace(/\s/g, ""))}
            placeholder="my-custom-link"
            className="flex-1 px-4 py-2 rounded-xl border border-gray-200
                       focus:outline-none focus:ring-2 focus:ring-violet-400
                       text-gray-700 text-sm"
          />
        </div>
      )}

    </form>
  )
}