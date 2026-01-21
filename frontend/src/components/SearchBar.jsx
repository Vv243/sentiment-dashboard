import { useState } from 'react'

function SearchBar({ onSearch, defaultValue = '' }) {
  const [ticker, setTicker] = useState(defaultValue)

  const handleSubmit = (e) => {
    e.preventDefault()
    if (ticker.trim()) {
      onSearch(ticker.trim().toUpperCase())
    }
  }

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl mx-auto">
      <div className="relative">
        <input
          type="text"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
          placeholder="Enter ticker symbol (e.g., TSLA, AAPL, GME)"
          className="w-full px-6 py-4 text-lg border-2 border-gray-300 rounded-xl focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-200 transition-all"
        />
        <button
          type="submit"
          className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors font-medium"
        >
          Search
        </button>
      </div>
      <div className="mt-3 flex flex-wrap gap-2 justify-center">
        {['TSLA', 'AAPL', 'GME', 'AMD', 'NVDA'].map((t) => (
          <button
            key={t}
            type="button"
            onClick={() => {
              setTicker(t)
              onSearch(t)
            }}
            className="px-4 py-1 bg-gray-200 text-gray-700 rounded-full hover:bg-gray-300 transition-colors text-sm font-medium"
          >
            {t}
          </button>
        ))}
      </div>
    </form>
  )
}

export default SearchBar
