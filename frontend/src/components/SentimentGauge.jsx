function SentimentGauge({ sentiment }) {
  const { compound, label } = sentiment

  // Convert compound (-1 to 1) to percentage (0 to 100)
  const percentage = ((compound + 1) / 2) * 100

  // Determine color based on label
  const colors = {
    positive: { bg: 'bg-green-500', text: 'text-green-700', emoji: '😊' },
    negative: { bg: 'bg-red-500', text: 'text-red-700', emoji: '😟' },
    neutral: { bg: 'bg-gray-500', text: 'text-gray-700', emoji: '😐' },
  }

  const color = colors[label]

  return (
    <div className="space-y-6">
      {/* Large emoji display */}
      <div className="flex justify-center">
        <div className="text-8xl">{color.emoji}</div>
      </div>

      {/* Sentiment label and score */}
      <div className="text-center">
        <div className={`text-3xl font-bold ${color.text} capitalize mb-2`}>
          {label}
        </div>
        <div className="text-gray-600 text-lg">
          Score: {compound.toFixed(3)}
        </div>
      </div>

      {/* Progress bar */}
      <div className="relative pt-1">
        <div className="flex mb-2 items-center justify-between">
          <div>
            <span className="text-xs font-semibold inline-block text-gray-600">
              Sentiment Meter
            </span>
          </div>
          <div>
            <span className="text-xs font-semibold inline-block text-gray-600">
              {percentage.toFixed(1)}%
            </span>
          </div>
        </div>
        <div className="overflow-hidden h-4 mb-4 text-xs flex rounded-full bg-gray-200">
          <div
            style={{ width: `${percentage}%` }}
            className={`shadow-none flex flex-col text-center whitespace-nowrap text-white justify-center ${color.bg} transition-all duration-500`}
          ></div>
        </div>
        <div className="flex justify-between text-xs text-gray-600">
          <span>Negative</span>
          <span>Neutral</span>
          <span>Positive</span>
        </div>
      </div>

      {/* Detailed scores */}
      <div className="grid grid-cols-3 gap-4 mt-6">
        <div className="bg-red-50 rounded-lg p-3 text-center">
          <div className="text-xs text-gray-600 mb-1">Negative</div>
          <div className="text-lg font-semibold text-red-700">
            {(sentiment.negative * 100).toFixed(1)}%
          </div>
        </div>
        <div className="bg-gray-50 rounded-lg p-3 text-center">
          <div className="text-xs text-gray-600 mb-1">Neutral</div>
          <div className="text-lg font-semibold text-gray-700">
            {(sentiment.neutral * 100).toFixed(1)}%
          </div>
        </div>
        <div className="bg-green-50 rounded-lg p-3 text-center">
          <div className="text-xs text-gray-600 mb-1">Positive</div>
          <div className="text-lg font-semibold text-green-700">
            {(sentiment.positive * 100).toFixed(1)}%
          </div>
        </div>
      </div>
    </div>
  )
}

export default SentimentGauge
