import { useEffect, useState } from 'react'
import './App.css'

// API URL from environment variable
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [text, setText] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [history, setHistory] = useState([])
  const [loadingHistory, setLoadingHistory] = useState(false)

  // Fetch history when component mounts
  useEffect(() => {
    fetchHistory()
  }, [])

  const fetchHistory = async () => {
    setLoadingHistory(true)
    try {
      const response = await fetch(`${API_URL}/api/v1/sentiment/history?limit=10`)
      if (response.ok) {
        const data = await response.json()
        setHistory(data.analyses)
      }
    } catch (err) {
      console.error('Failed to fetch history:', err)
    } finally {
      setLoadingHistory(false)
    }
  }

  const analyzeSentiment = async (e) => {
    e.preventDefault()

    if (!text.trim()) {
      setError('Please enter some text to analyze')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch(`${API_URL}/api/v1/sentiment/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      })

      if (!response.ok) {
        throw new Error('Failed to analyze sentiment')
      }

      const data = await response.json()
      setResult(data)

      // Refresh history after new analysis
      fetchHistory()

      // Clear input
      setText('')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const formatDate = (timestamp) => {
    return new Date(timestamp).toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>🎭 Sentiment Analysis Dashboard</h1>
          <p>Analyze the emotional tone of any text using AI</p>
        </header>

        <form onSubmit={analyzeSentiment} className="analysis-form">
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Enter text to analyze... (e.g., 'I love this product! It's amazing!')"
            rows="6"
            className="text-input"
          />

          <button type="submit" disabled={loading} className="analyze-button">
            {loading ? 'Analyzing...' : 'Analyze Sentiment'}
          </button>
        </form>

        {error && <div className="error-message">❌ {error}</div>}

        {result && (
          <div className="result-card">
            <h2>Latest Analysis</h2>

            <div className="sentiment-display">
              <span className="emoji">{result.emoji}</span>
              <span className="sentiment-label">{result.sentiment}</span>
            </div>

            <div className="scores">
              <h3>Detailed Scores</h3>
              <div className="score-grid">
                <div className="score-item">
                  <span className="score-label">Positive</span>
                  <span className="score-value">{(result.scores.positive * 100).toFixed(1)}%</span>
                </div>
                <div className="score-item">
                  <span className="score-label">Negative</span>
                  <span className="score-value">{(result.scores.negative * 100).toFixed(1)}%</span>
                </div>
                <div className="score-item">
                  <span className="score-label">Neutral</span>
                  <span className="score-value">{(result.scores.neutral * 100).toFixed(1)}%</span>
                </div>
                <div className="score-item">
                  <span className="score-label">Compound</span>
                  <span className="score-value">{result.scores.compound.toFixed(3)}</span>
                </div>
              </div>
            </div>

            <div className="analyzed-text">
              <h3>Analyzed Text</h3>
              <p>"{result.text}"</p>
            </div>
          </div>
        )}

        {/* History Section */}
        <div className="history-section">
          <div className="history-header">
            <h2>📊 Recent Analyses</h2>
            <button onClick={fetchHistory} className="refresh-button" disabled={loadingHistory}>
              {loadingHistory ? '⏳' : '🔄'} Refresh
            </button>
          </div>

          {loadingHistory && history.length === 0 ? (
            <p className="loading-text">Loading history...</p>
          ) : history.length === 0 ? (
            <p className="empty-text">No analyses yet. Try analyzing some text above!</p>
          ) : (
            <div className="history-list">
              {history.map((item, index) => (
                <div key={item._id || index} className="history-item">
                  <div className="history-header-row">
                    <span className="history-emoji">{item.emoji}</span>
                    <span className={`history-sentiment ${item.sentiment}`}>{item.sentiment}</span>
                    <span className="history-date">{formatDate(item.timestamp)}</span>
                  </div>
                  <p className="history-text">"{item.text}"</p>
                  <div className="history-scores">
                    <span>😊 {(item.scores.positive * 100).toFixed(0)}%</span>
                    <span>😐 {(item.scores.neutral * 100).toFixed(0)}%</span>
                    <span>😞 {(item.scores.negative * 100).toFixed(0)}%</span>
                    <span>📊 {item.scores.compound.toFixed(2)}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
