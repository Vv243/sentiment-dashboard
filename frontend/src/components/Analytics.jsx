import { useEffect, useState } from 'react'
import {
  CartesianGrid,
  Cell,
  Legend,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function Analytics() {
  const [historyData, setHistoryData] = useState([])
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState({
    total: 0,
    positive: 0,
    negative: 0,
    neutral: 0,
    avgCompound: 0,
  })

  // Fetch history data on component mount
  useEffect(() => {
    fetchHistory()
  }, [])

  const fetchHistory = async () => {
    try {
      setLoading(true)
      const response = await fetch(`${API_URL}/api/v1/sentiment/history?limit=100`)
      const data = await response.json()

      setHistoryData(data.analyses || [])
      calculateStats(data.analyses || [])
    } catch (error) {
      console.error('Error fetching history:', error)
    } finally {
      setLoading(false)
    }
  }

  const calculateStats = (data) => {
    const total = data.length
    const positive = data.filter((d) => d.sentiment === 'positive').length
    const negative = data.filter((d) => d.sentiment === 'negative').length
    const neutral = data.filter((d) => d.sentiment === 'neutral').length

    const avgCompound =
      total > 0 ? data.reduce((sum, d) => sum + (d.scores?.compound || 0), 0) / total : 0

    setStats({ total, positive, negative, neutral, avgCompound })
  }

  // Prepare pie chart data
  const pieData = [
    { name: 'Positive', value: stats.positive, color: '#48bb78' },
    { name: 'Negative', value: stats.negative, color: '#f56565' },
    { name: 'Neutral', value: stats.neutral, color: '#a0aec0' },
  ]

  // Prepare timeline data - group by date
  const prepareTimelineData = () => {
    if (historyData.length === 0) return []

    // Sort by timestamp
    const sorted = [...historyData].sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp))

    // Group by date and calculate averages
    const grouped = {}
    sorted.forEach((item) => {
      const date = new Date(item.timestamp).toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
      })

      if (!grouped[date]) {
        grouped[date] = {
          date,
          scores: [],
          count: 0,
        }
      }

      grouped[date].scores.push(item.scores?.compound || 0)
      grouped[date].count++
    })

    // Convert to array and calculate averages
    const timeline = Object.values(grouped).map((day) => ({
      date: day.date,
      compound: day.scores.reduce((sum, s) => sum + s, 0) / day.count,
      count: day.count,
    }))

    // Add moving average (3-day)
    timeline.forEach((day, idx) => {
      if (idx < 2) {
        day.average = day.compound
      } else {
        const sum = timeline[idx].compound + timeline[idx - 1].compound + timeline[idx - 2].compound
        day.average = sum / 3
      }
    })

    // Limit to last 20 data points for readability
    return timeline.slice(-20)
  }

  // Prepare score distribution data
  const prepareScoreDistribution = () => {
    if (historyData.length === 0) return []

    // Get last 50 analyses
    const recent = historyData.slice(0, 50).reverse()

    return recent.map((item, idx) => ({
      index: idx + 1,
      positive: item.scores?.positive || 0,
      negative: item.scores?.negative || 0,
      neutral: item.scores?.neutral || 0,
      compound: item.scores?.compound || 0,
    }))
  }

  if (loading) {
    return (
      <div className="analytics-container">
        <div className="loading-message">⏳ Loading analytics...</div>
      </div>
    )
  }

  if (stats.total === 0) {
    return (
      <div className="analytics-container">
        <h2>📊 Analytics Dashboard</h2>
        <p className="no-data">No data yet. Analyze some text to see analytics!</p>
      </div>
    )
  }

  return (
    <div className="analytics-container">
      <div className="analytics-header">
        <h2>📊 Analytics Dashboard</h2>
        <button onClick={fetchHistory} className="refresh-btn">
          🔄 Refresh
        </button>
      </div>

      {/* Quick Stats Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">📝</div>
          <div className="stat-value">{stats.total}</div>
          <div className="stat-label">Total Analyses</div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">😊</div>
          <div className="stat-value">
            {stats.total > 0 ? Math.round((stats.positive / stats.total) * 100) : 0}%
          </div>
          <div className="stat-label">Positive</div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">📈</div>
          <div className="stat-value">{stats.avgCompound.toFixed(2)}</div>
          <div className="stat-label">Avg. Compound Score</div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            {stats.avgCompound > 0.1 ? '↗️' : stats.avgCompound < -0.1 ? '↘️' : '→'}
          </div>
          <div className="stat-value">
            {stats.avgCompound > 0.1
              ? 'Positive'
              : stats.avgCompound < -0.1
                ? 'Negative'
                : 'Neutral'}
          </div>
          <div className="stat-label">Overall Trend</div>
        </div>
      </div>

      {/* Charts Grid */}
      <div className="charts-grid">
        {/* Pie Chart */}
        <div className="chart-container">
          <h3>Sentiment Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Timeline Chart */}
        <div className="chart-container">
          <h3>Sentiment Over Time</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={prepareTimelineData()}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="date"
                tick={{ fontSize: 12 }}
                angle={-45}
                textAnchor="end"
                height={80}
              />
              <YAxis
                domain={[-1, 1]}
                tick={{ fontSize: 12 }}
                label={{ value: 'Compound Score', angle: -90, position: 'insideLeft' }}
              />
              <Tooltip
                formatter={(value) => value.toFixed(2)}
                labelFormatter={(label) => `Date: ${label}`}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey="compound"
                stroke="#667eea"
                strokeWidth={2}
                dot={{ fill: '#667eea', r: 4 }}
                name="Sentiment Score"
              />
              <Line
                type="monotone"
                dataKey="average"
                stroke="#48bb78"
                strokeWidth={2}
                strokeDasharray="5 5"
                dot={false}
                name="Moving Average"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Score Distribution Chart */}
        <div className="chart-container chart-full-width">
          <h3>Score Distribution (Recent 50)</h3>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={prepareScoreDistribution()}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="index"
                label={{ value: 'Analysis #', position: 'insideBottom', offset: -5 }}
              />
              <YAxis
                domain={[0, 1]}
                label={{ value: 'Score', angle: -90, position: 'insideLeft' }}
              />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey="positive"
                stroke="#48bb78"
                strokeWidth={1.5}
                dot={false}
                name="Positive"
              />
              <Line
                type="monotone"
                dataKey="negative"
                stroke="#f56565"
                strokeWidth={1.5}
                dot={false}
                name="Negative"
              />
              <Line
                type="monotone"
                dataKey="neutral"
                stroke="#a0aec0"
                strokeWidth={1.5}
                dot={false}
                name="Neutral"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}

export default Analytics
