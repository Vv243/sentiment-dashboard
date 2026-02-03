import { useEffect, useState } from 'react'
import './App.css'
import Analytics from './components/Analytics'
import BatchUpload from './components/BatchUpload'

// API URL from environment variable
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// Comprehensive censor function - replaces all harmful content with asterisks
const censorText = (text, isFlagged) => {
  if (!isFlagged) return text

  // Comprehensive list of harmful patterns to censor
  const harmfulPatterns = [
    // Self-harm and suicide
    /\b(kill|hurt|harm)\s+(your)?self\b/gi,
    /\bcommit\s+suicide\b/gi,
    /\bend\s+(your\s+)?(life|it\s+all)\b/gi,
    /\bsuicide\b/gi,
    /\b(hang|shoot|drown)\s+yourself\b/gi,
    /\bjump\s+off\b/gi,
    /\bslit\s+your\b/gi,
    /\boverdose\b/gi,
    /\bkys\b/gi,

    // Death and violence
    /\b(hope you|wish you were)\s+d[i!1*]e?[d]?\b/gi,
    /\byou should die\b/gi,
    /\bgo die\b/gi,

    // Racial slurs - N-word variations
    /\bn[i!1*]+gg?[ae3][rhz]*\b/gi,
    /\bn[i!1*]+gg?[aeou3]+\b/gi,

    // Other racial slurs
    /\bch[i!1*]nk\b/gi,
    /\bsp[i!1*]c\b/gi,
    /\bwetb[a@]ck\b/gi,
    /\bg[o0][o0]k\b/gi,
    /\bk[i!1*]ke\b/gi,
    /\brag\s*head\b/gi,
    /\bsand\s*n[i!1*]gg?[ae3]r\b/gi,
    /\bbeaner\b/gi,
    /\bcamel\s*jockey\b/gi,

    // Homophobic slurs
    /\bf[a@4]gg?[o0]t\b/gi,
    /\bd[y1]ke\b/gi,
    /\btr[a@4]nny\b/gi,
    /\bqu[e3][e3]r\b(?!\s+(studies|theory|community))/gi, // Exclude academic/positive uses

    // Misogynistic slurs
    /\bc[u*][n*]t\b/gi,
    /\bwh[o0]re\b/gi,
    /\bsl[u*]t\b/gi,
    /\bb[i!1*]tch\b/gi,

    // Ableist slurs
    /\bret[a@4]rd(ed)?\b/gi,
    /\bm[o0]ng?[o0]l[o0]id\b/gi,
    /\bcr[i!1*]pple\b/gi,
    /\bspaz\b/gi,

    // Extreme insults
    /\b(worthless|useless|garbage|trash)\b/gi,
    /\bwaste of\b/gi,
  ]

  let censoredText = text

  // Replace each harmful pattern with asterisks
  harmfulPatterns.forEach((pattern) => {
    censoredText = censoredText.replace(pattern, (match) => {
      // Keep first and last character visible, replace middle with asterisks
      if (match.length <= 2) return '**'
      if (match.length === 3) return match[0] + '*' + match[2]
      return match[0] + '*'.repeat(match.length - 2) + match[match.length - 1]
    })
  })

  return censoredText
}

function App() {
  const [text, setText] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [history, setHistory] = useState([])
  const [loadingHistory, setLoadingHistory] = useState(false)
  const [historyLimit, setHistoryLimit] = useState(5) // NEW: Start with 5
  const [hasMore, setHasMore] = useState(false) // NEW: Track if more records exist
  const [selectedModel, setSelectedModel] = useState('vader') // Model selection state

  // Fetch history when component mounts or limit changes
  useEffect(() => {
    fetchHistory()
  }, [historyLimit]) // CHANGED: Also fetch when limit changes

  const fetchHistory = async () => {
    setLoadingHistory(true)
    try {
      // Fetch one more than limit to check if there are more records
      const response = await fetch(`${API_URL}/api/v1/sentiment/history?limit=${historyLimit + 1}`)
      if (response.ok) {
        const data = await response.json()

        // Check if there are more records
        if (data.analyses && data.analyses.length > historyLimit) {
          setHasMore(true)
          setHistory(data.analyses.slice(0, historyLimit)) // Show only requested amount
        } else {
          setHasMore(false)
          setHistory(data.analyses || [])
        }
      }
    } catch (err) {
      console.error('Failed to fetch history:', err)
    } finally {
      setLoadingHistory(false)
    }
  }

  const loadMore = () => {
    setHistoryLimit((prev) => prev + 5) // Load 5 more
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
        body: JSON.stringify({
          text,
          model: selectedModel, // Include selected model
        }),
      })

      if (!response.ok) {
        throw new Error('Failed to analyze sentiment')
      }

      const data = await response.json()
      setResult(data)

      // Refresh history after new analysis
      setHistoryLimit(5) // Reset to show 5
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
          {/* Model Selector */}
          <div className="model-selector">
            <label htmlFor="model">🤖 Analysis Mode:</label>
            <div className="model-options">
              <button
                type="button"
                className={`model-option ${selectedModel === 'vader' ? 'active' : ''}`}
                onClick={() => setSelectedModel('vader')}
              >
                <span className="model-icon">⚡</span>
                <span className="model-name">Fast</span>
                <span className="model-time">~50ms</span>
              </button>
              <button
                type="button"
                className={`model-option ${selectedModel === 'distilbert' ? 'active' : ''}`}
                onClick={() => setSelectedModel('distilbert')}
              >
                <span className="model-icon">🎯</span>
                <span className="model-name">Precise</span>
                <span className="model-time">~200ms</span>
              </button>
            </div>
          </div>

          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={(e) => {
              // Submit on Enter (without Shift)
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault() // Prevent new line
                analyzeSentiment(e) // Submit form
              }
              // Shift+Enter allows new line (default behavior)
            }}
            placeholder="Enter text to analyze... (Press Enter to analyze, Shift+Enter for new line)"
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

            {/* Show warning if content is harmful */}
            {result.moderation?.flagged && (
              <div className="moderation-warning">
                ⚠️ <strong>Content Moderation Alert:</strong> {result.moderation.reason}
              </div>
            )}

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
              <p>"{censorText(result.text, result.moderation?.flagged)}"</p>
            </div>
          </div>
        )}

        {/* History Section */}
        <div className="history-section">
          <div className="history-header">
            <h2>📊 Recent Analyses</h2>
            <button
              onClick={() => {
                setHistoryLimit(5)
                fetchHistory()
              }}
              className="refresh-button"
              disabled={loadingHistory}
            >
              {loadingHistory ? '⏳' : '🔄'} Refresh
            </button>
          </div>

          {loadingHistory && history.length === 0 ? (
            <p className="loading-text">Loading history...</p>
          ) : history.length === 0 ? (
            <p className="empty-text">No analyses yet. Try analyzing some text above!</p>
          ) : (
            <>
              <div className="history-list">
                {history.map((item, index) => (
                  <div key={item._id || item.id || index} className="history-item">
                    <div className="history-header-row">
                      <span className="history-emoji">{item.emoji}</span>
                      <span className={`history-sentiment ${item.sentiment}`}>
                        {item.sentiment}
                      </span>
                      <span className="history-date">{formatDate(item.timestamp)}</span>
                    </div>
                    <p className="history-text">
                      "{censorText(item.text, item.moderation?.flagged)}"
                    </p>
                    <div className="history-scores">
                      <span>😊 {(item.scores.positive * 100).toFixed(0)}%</span>
                      <span>😐 {(item.scores.neutral * 100).toFixed(0)}%</span>
                      <span>😞 {(item.scores.negative * 100).toFixed(0)}%</span>
                      <span>📊 {item.scores.compound.toFixed(2)}</span>
                    </div>
                  </div>
                ))}
              </div>

              {/* NEW: View More / View Less Buttons */}
              {history.length > 0 && (
                <div className="view-more-container">
                  {/* Show View Less if we're showing more than 5 */}
                  {historyLimit > 5 && (
                    <button
                      onClick={() => setHistoryLimit(5)}
                      className="view-less-button"
                      disabled={loadingHistory}
                    >
                      View Less
                    </button>
                  )}

                  {/* Show View More if there are more records to load */}
                  {hasMore && (
                    <button
                      onClick={loadMore}
                      className="view-more-button"
                      disabled={loadingHistory}
                    >
                      {loadingHistory ? 'Loading...' : 'View More'}
                    </button>
                  )}
                </div>
              )}
            </>
          )}
        </div>
        {/* Batch CSV Upload */}
        <BatchUpload />

        {/* Analytics Dashboard */}
        <Analytics />
      </div>
    </div>
  )
}

export default App
