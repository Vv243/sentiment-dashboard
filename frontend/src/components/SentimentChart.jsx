import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine,
} from 'recharts'

function SentimentChart({ data }) {
  // Transform data for chart
  const chartData = data.map((point) => ({
    time: new Date(point.timestamp).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
    }),
    sentiment: point.sentiment,
    posts: point.post_count,
  }))

  // Custom tooltip
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload
      return (
        <div className="bg-white p-3 border border-gray-300 rounded-lg shadow-lg">
          <p className="font-semibold text-gray-900">{data.time}</p>
          <p className="text-sm text-gray-600">
            Sentiment: <span className="font-semibold">{data.sentiment.toFixed(3)}</span>
          </p>
          <p className="text-sm text-gray-600">
            Posts: <span className="font-semibold">{data.posts}</span>
          </p>
        </div>
      )
    }
    return null
  }

  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart
        data={chartData}
        margin={{
          top: 5,
          right: 30,
          left: 20,
          bottom: 5,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
        <XAxis
          dataKey="time"
          stroke="#6b7280"
          style={{ fontSize: '12px' }}
        />
        <YAxis
          domain={[-1, 1]}
          stroke="#6b7280"
          style={{ fontSize: '12px' }}
          label={{ value: 'Sentiment Score', angle: -90, position: 'insideLeft' }}
        />
        <Tooltip content={<CustomTooltip />} />
        <Legend />
        <ReferenceLine y={0} stroke="#9ca3af" strokeDasharray="3 3" />
        <ReferenceLine y={0.05} stroke="#10b981" strokeDasharray="2 2" label="Positive" />
        <ReferenceLine y={-0.05} stroke="#ef4444" strokeDasharray="2 2" label="Negative" />
        <Line
          type="monotone"
          dataKey="sentiment"
          stroke="#3b82f6"
          strokeWidth={2}
          dot={{ r: 4 }}
          activeDot={{ r: 6 }}
          name="Sentiment"
        />
      </LineChart>
    </ResponsiveContainer>
  )
}

export default SentimentChart
