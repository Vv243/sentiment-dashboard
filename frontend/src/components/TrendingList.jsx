function TrendingList({ trending, onSelectTicker }) {
  if (!trending || trending.length === 0) {
    return (
      <div className="text-center text-gray-500 py-8">
        No trending topics available
      </div>
    )
  }

  const getSentimentColor = (score) => {
    if (score >= 0.05) return 'text-green-600 bg-green-50'
    if (score <= -0.05) return 'text-red-600 bg-red-50'
    return 'text-gray-600 bg-gray-50'
  }

  const getSentimentEmoji = (score) => {
    if (score >= 0.05) return '📈'
    if (score <= -0.05) return '📉'
    return '➡️'
  }

  return (
    <div className="space-y-3">
      {trending.map((topic, index) => (
        <button
          key={topic.ticker}
          onClick={() => onSelectTicker(topic.ticker)}
          className="w-full text-left p-4 rounded-lg border border-gray-200 hover:border-blue-400 hover:shadow-md transition-all group"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="text-2xl font-bold text-gray-400 group-hover:text-blue-500">
                #{index + 1}
              </div>
              <div>
                <div className="font-semibold text-gray-900 group-hover:text-blue-600">
                  {topic.ticker}
                </div>
                <div className="text-xs text-gray-500">
                  {topic.mention_count} mentions
                </div>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <span className="text-xl">{getSentimentEmoji(topic.sentiment_score)}</span>
              <span
                className={`px-3 py-1 rounded-full text-xs font-semibold ${getSentimentColor(
                  topic.sentiment_score
                )}`}
              >
                {topic.sentiment_score.toFixed(3)}
              </span>
            </div>
          </div>
        </button>
      ))}
    </div>
  )
}

export default TrendingList
