import Papa from 'papaparse'
import { useState } from 'react'

// API URL from environment variable
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function BatchUpload() {
  // File upload state
  const [file, setFile] = useState(null)
  const [csvData, setCsvData] = useState([])
  const [columns, setColumns] = useState([])
  const [selectedColumn, setSelectedColumn] = useState('')
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  // NEW: Processing state
  const [selectedModel, setSelectedModel] = useState('vader') // Fast by default
  const [isProcessing, setIsProcessing] = useState(false)
  const [progress, setProgress] = useState({ current: 0, total: 0 })
  const [results, setResults] = useState([])
  const [processingErrors, setProcessingErrors] = useState([])

  // Handle file selection
  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0]

    if (!selectedFile) {
      return
    }

    if (!selectedFile.name.endsWith('.csv')) {
      setError('Please upload a CSV file')
      return
    }

    if (selectedFile.size > 5 * 1024 * 1024) {
      setError('File too large. Maximum size is 5MB')
      return
    }

    setFile(selectedFile)
    setError('')
    // Reset previous results when new file is uploaded
    setResults([])
    setProcessingErrors([])
    parseCSV(selectedFile)
  }

  // Parse CSV file
  const parseCSV = (file) => {
    setIsLoading(true)

    Papa.parse(file, {
      header: true,
      skipEmptyLines: true,
      complete: (results) => {
        console.log('Parsed CSV:', results)

        if (results.data.length === 0) {
          setError('CSV file is empty')
          setIsLoading(false)
          return
        }

        if (results.data.length > 1000) {
          setError('CSV has too many rows. Maximum is 1000 rows')
          setIsLoading(false)
          return
        }

        const cols = Object.keys(results.data[0])

        if (cols.length === 0) {
          setError('No columns found in CSV')
          setIsLoading(false)
          return
        }

        setCsvData(results.data)
        setColumns(cols)
        setSelectedColumn(cols[0])
        setIsLoading(false)
      },
      error: (error) => {
        console.error('CSV parsing error:', error)
        setError('Failed to parse CSV file. Make sure it is properly formatted.')
        setIsLoading(false)
      },
    })
  }

  // Handle column selection
  const handleColumnChange = (event) => {
    setSelectedColumn(event.target.value)
  }

  // NEW: Process all rows - THIS WAS MISSING!
  const startBatchAnalysis = async () => {
    if (!csvData.length || !selectedColumn) {
      setError('Please upload a CSV and select a column first')
      return
    }

    setIsProcessing(true)
    setProgress({ current: 0, total: csvData.length })
    setResults([])
    setProcessingErrors([])

    const newResults = []
    const errors = []

    // Process each row one by one
    for (let i = 0; i < csvData.length; i++) {
      const row = csvData[i]
      const textToAnalyze = row[selectedColumn]

      // Skip empty or very short text
      if (!textToAnalyze || textToAnalyze.trim().length < 3) {
        errors.push({
          row: i + 1,
          text: textToAnalyze || '(empty)',
          error: 'Text too short or empty',
        })
        setProgress({ current: i + 1, total: csvData.length })
        continue
      }

      try {
        // Call your existing sentiment API
        const response = await fetch(`${API_URL}/api/v1/sentiment/analyze`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            text: textToAnalyze,
            model: selectedModel,
          }),
        })

        if (!response.ok) {
          throw new Error(`API error: ${response.status}`)
        }

        const data = await response.json()

        // Store result
        newResults.push({
          row: i + 1,
          text: textToAnalyze,
          sentiment: data.sentiment,
          emoji: data.emoji,
          scores: data.scores,
          moderation: data.moderation,
        })
      } catch (err) {
        console.error(`Error processing row ${i + 1}:`, err)
        errors.push({
          row: i + 1,
          text: textToAnalyze.substring(0, 50) + '...',
          error: err.message,
        })
      }

      // Update progress
      setProgress({ current: i + 1, total: csvData.length })
      setResults([...newResults]) // Update results in real-time
      setProcessingErrors([...errors])

      // Small delay to avoid overwhelming the API (optional)
      await new Promise((resolve) => setTimeout(resolve, 100))
    }

    setIsProcessing(false)
    console.log('Batch analysis complete!', { results: newResults, errors })
  }

  return (
    <div className="batch-upload-container">
      <h2>📊 Batch CSV Analysis</h2>

      {/* File Upload Section */}
      <div className="upload-section">
        <label htmlFor="csv-upload" className="upload-label">
          Upload CSV File (max 1000 rows, 5MB)
        </label>
        <input
          id="csv-upload"
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          className="file-input"
          disabled={isProcessing}
        />
      </div>

      {/* Error Display */}
      {error && <div className="error-message">⚠️ {error}</div>}

      {/* Loading State */}
      {isLoading && <div className="loading-message">⏳ Parsing CSV file...</div>}

      {/* Column Selection (only show if we have data) */}
      {csvData.length > 0 && columns.length > 0 && (
        <div className="column-selection">
          <h3>Select Column to Analyze</h3>
          <select
            value={selectedColumn}
            onChange={handleColumnChange}
            className="column-select"
            disabled={isProcessing}
          >
            {columns.map((col) => (
              <option key={col} value={col}>
                {col}
              </option>
            ))}
          </select>

          {/* NEW: Model Selector */}
          <div className="batch-model-selector">
            <label>🤖 Analysis Mode:</label>
            <div className="batch-model-options">
              <button
                type="button"
                className={`batch-model-option ${selectedModel === 'vader' ? 'active' : ''}`}
                onClick={() => setSelectedModel('vader')}
                disabled={isProcessing}
              >
                <span className="model-icon">⚡</span>
                <span className="model-name">Fast</span>
                <span className="model-time">~50ms/row</span>
              </button>
              <button
                type="button"
                className={`batch-model-option ${selectedModel === 'distilbert' ? 'active' : ''}`}
                onClick={() => setSelectedModel('distilbert')}
                disabled={isProcessing}
              >
                <span className="model-icon">🎯</span>
                <span className="model-name">Precise</span>
                <span className="model-time">~200ms/row</span>
              </button>
            </div>
          </div>

          {/* Data Preview */}
          <div className="preview-section">
            <h4>Preview (first 5 rows):</h4>
            <div className="preview-table">
              <table>
                <thead>
                  <tr>
                    <th>#</th>
                    <th>{selectedColumn}</th>
                  </tr>
                </thead>
                <tbody>
                  {csvData.slice(0, 5).map((row, index) => (
                    <tr key={index}>
                      <td>{index + 1}</td>
                      <td>{row[selectedColumn]}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <p className="row-count">
              Total rows to analyze: <strong>{csvData.length}</strong>
            </p>
          </div>

          {/* Start Analysis Button */}
          <button
            className="start-analysis-btn"
            onClick={startBatchAnalysis}
            disabled={isProcessing || isLoading}
          >
            {isProcessing ? 'Processing...' : 'Start Analysis →'}
          </button>

          {/* NEW: Progress Bar */}
          {isProcessing && (
            <div className="progress-container">
              <div className="progress-bar">
                <div
                  className="progress-fill"
                  style={{
                    width: `${(progress.current / progress.total) * 100}%`,
                  }}
                />
              </div>
              <p className="progress-text">
                Processing {progress.current} of {progress.total} rows (
                {Math.round((progress.current / progress.total) * 100)}%)
              </p>
            </div>
          )}

          {/* NEW: Results Display */}
          {results.length > 0 && (
            <div className="results-section">
              <h3>📈 Analysis Results ({results.length} rows)</h3>
              <div className="results-table">
                <table>
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>Text</th>
                      <th>Sentiment</th>
                      <th>Scores</th>
                    </tr>
                  </thead>
                  <tbody>
                    {results.map((result, index) => (
                      <tr key={index}>
                        <td>{result.row}</td>
                        <td className="result-text">{result.text.substring(0, 60)}...</td>
                        <td>
                          <span className={`sentiment-badge ${result.sentiment}`}>
                            {result.emoji} {result.sentiment}
                          </span>
                        </td>
                        <td className="result-scores">
                          <span>😊 {(result.scores.positive * 100).toFixed(0)}%</span>
                          <span>😐 {(result.scores.neutral * 100).toFixed(0)}%</span>
                          <span>😞 {(result.scores.negative * 100).toFixed(0)}%</span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* NEW: Errors Display */}
          {processingErrors.length > 0 && (
            <div className="errors-section">
              <h3>⚠️ Errors ({processingErrors.length} rows failed)</h3>
              <div className="errors-list">
                {processingErrors.map((err, index) => (
                  <div key={index} className="error-item">
                    <strong>Row {err.row}:</strong> {err.error}
                    <br />
                    <em>{err.text}</em>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default BatchUpload
