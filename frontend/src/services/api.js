const BASE_URL = "https://ismat18-url-shortener-backend.hf.space"
// Long URL ko short karo
// POST /api/shorten
export async function shortenURL(longUrl, customAlias = "") {
  const body = { url: longUrl }

  // Agar user ne custom alias diya hai toh include karo
  if (customAlias.trim()) {
    body.custom_alias = customAlias.trim()
  }

  const response = await fetch(`${BASE_URL}/api/shorten`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  })

  const data = await response.json()

  // Agar backend ne error diya (jaise alias already exists)
  if (!response.ok) {
    throw new Error(data.detail || "Something went wrong")
  }

  return data
}


// MongoDB se saari URLs ki history lao
// GET /api/urls
export async function fetchHistory() {
  const response = await fetch(`${BASE_URL}/api/urls`)

  if (!response.ok) {
    throw new Error("Could not load history")
  }

  return response.json()
}