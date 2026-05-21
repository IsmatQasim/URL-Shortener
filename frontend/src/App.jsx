import { useState, useEffect } from "react"
import { shortenURL, fetchHistory } from "./services/api"
import URLInput from "./components/URLInput"
import ResultCard from "./components/ResultCard"
import HistoryList from "./components/HistoryList"

export default function App() {
  const [result, setResult] = useState(null)
  const [history, setHistory] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")
  const [historyLoading, setHistoryLoading] = useState(true)
const isRedirecting = window.location.pathname.slice(1) !== ""

  useEffect(() => {
  const path = window.location.pathname.slice(1)

  if (path) {
    fetch(`https://ismat18-url-shortener-backend.hf.space/api/resolve/${path}`)
      .then(res => res.json())
      .then(data => {
        if (data.original_url) {
          window.location.href = data.original_url
        }
      })
  }
}, [])
  
  useEffect(() => {
  async function loadHistory() {
    try {
      setHistoryLoading(true)
      const data = await fetchHistory()
      setHistory(data)
    } catch (err) {
      console.error("History load failed:", err)
    } finally {
      setHistoryLoading(false)
    }
  }

  loadHistory()
}, []) // [] matlab: sirf ek baar — page load pe

  async function handleShorten(longUrl, customAlias) {
    setIsLoading(true)
    setError("")
    setResult(null)

    try {
      const data = await shortenURL(longUrl, customAlias)
      setResult(data)

      // Naya URL history mein UPAR add karo — DB se dobara fetch ki zarurat nahi
      setHistory((prev) => [data, ...prev])

    } catch (err) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }


  if (isRedirecting) {
    return (
      <main className="min-h-screen bg-gradient-to-br from-violet-50 to-white flex items-center justify-center">
        <div className="text-center">
          <p className="text-2xl mb-2">✂️</p>
          <p className="text-gray-500 text-sm">Redirecting...</p>
        </div>
      </main>
    )
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

        <URLInput onShorten={handleShorten} isLoading={isLoading} />

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-600
                          text-sm rounded-xl px-4 py-3">
            ⚠️ {error}
          </div>
        )}

        {result && <ResultCard result={result} />}

      </div>

      {/* History — real MongoDB data */}
      <div className="w-full max-w-xl">
        {historyLoading
          ? <p className="text-center text-gray-400 text-sm mt-8">Loading history...</p>
          : <HistoryList history={history} />
        }
      </div>

    </main>
  )
}