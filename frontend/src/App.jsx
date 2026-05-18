import { useState } from "react"
import { shortenURL } from "./services/api"
import URLInput from "./components/URLInput"
import ResultCard from "./components/ResultCard"
import HistoryList from "./components/HistoryList"

export default function App() {
  // State — App ki "yaadaasht"
  const [result, setResult]   = useState(null)   // Latest short URL result
  const [history, setHistory] = useState([])     // Is session mein banaye gaye sare URLs
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")

  // Jab user "Shorten" button dabaye
  async function handleShorten(longUrl, customAlias) {
    setIsLoading(true)
    setError("")
    setResult(null)

    try {
      const data = await shortenURL(longUrl, customAlias)

      setResult(data)                               // Result card dikhao
      setHistory((prev) => [...prev, data])         // History mein add karo

    } catch (err) {
      setError(err.message)                         // Error message dikhao
    } finally {
      setIsLoading(false)                           // Loading band karo — chahe success ho ya fail
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-violet-50 to-white flex flex-col items-center px-4 py-16">

      {/* Header */}
      <div className="text-center mb-10">
        <h1 className="text-4xl font-bold text-gray-800 mb-2">
          ✂️ URL Shortener
        </h1>
        <p className="text-gray-400 text-sm">
          Paste a long URL — get a short one instantly
        </p>
      </div>

      {/* Main Card */}
      <div className="w-full max-w-xl bg-white rounded-3xl shadow-xl shadow-violet-100 p-8 space-y-5">

        {/* Input Form */}
        <URLInput onShorten={handleShorten} isLoading={isLoading} />

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-600 
                          text-sm rounded-xl px-4 py-3">
            ⚠️ {error}
          </div>
        )}

        {/* Result */}
        {result && <ResultCard result={result} />}

      </div>

      {/* History */}
      <div className="w-full max-w-xl">
        <HistoryList history={history} />
      </div>

    </main>
  )
}