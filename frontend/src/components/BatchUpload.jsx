import Papa from 'papaparse'
import { useState } from 'react'

function BatchUpload() {
  // State management
  const [file, setFile] = useState(null)
  const [csvData, setCsvData] = useState([])
  const [columns, setColumns] = useState([])
  const [selectedColumn, setSelectedColumn] = useState('')
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  // Handle file selection
  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0]

    // Validate file type
    if (!selectedFile) {
      return
    }

    if (!selectedFile.name.endsWith('.csv')) {
      setError('Please upload a CSV file')
      return
    }

    // Validate file size (max 5MB)
    if (selectedFile.size > 5 * 1024 * 1024) {
      setError('File too large. Maximum size is 5MB')
      return
    }

    setFile(selectedFile)
    setError('')
    parseCSV(selectedFile)
  }

  // Parse CSV file
  const parseCSV = (file) => {
    setIsLoading(true)

    Papa.parse(file, {
      header: true, // First row is column names
      skipEmptyLines: true, // Ignore empty rows
      complete: (results) => {
        console.log('Parsed CSV:', results)

        // Validate we have data
        if (results.data.length === 0) {
          setError('CSV file is empty')
          setIsLoading(false)
          return
        }

        // Validate row count (max 1000)
        if (results.data.length > 1000) {
          setError('CSV has too many rows. Maximum is 1000 rows')
          setIsLoading(false)
          return
        }

        // Get column names
        const cols = Object.keys(results.data[0])

        if (cols.length === 0) {
          setError('No columns found in CSV')
          setIsLoading(false)
          return
        }

        // Save parsed data
        setCsvData(results.data)
        setColumns(cols)
        setSelectedColumn(cols[0]) // Auto-select first column
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
          <select value={selectedColumn} onChange={handleColumnChange} className="column-select">
            {columns.map((col) => (
              <option key={col} value={col}>
                {col}
              </option>
            ))}
          </select>

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
            onClick={() => alert('We will implement this tomorrow on Day 2!')}
          >
            Start Analysis →
          </button>
        </div>
      )}
    </div>
  )
}

export default BatchUpload
