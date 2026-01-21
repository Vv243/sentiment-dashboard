function StatsCards({ sentiment }) {
  const stats = [
    {
      label: 'Total Posts',
      value: sentiment.total_posts,
      icon: '📝',
      color: 'bg-blue-50 text-blue-700',
    },
    {
      label: 'Positive',
      value: sentiment.positive_count,
      icon: '👍',
      color: 'bg-green-50 text-green-700',
    },
    {
      label: 'Negative',
      value: sentiment.negative_count,
      icon: '👎',
      color: 'bg-red-50 text-red-700',
    },
    {
      label: 'Neutral',
      value: sentiment.neutral_count,
      icon: '😐',
      color: 'bg-gray-50 text-gray-700',
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {stats.map((stat, index) => (
        <div key={index} className="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 font-medium">{stat.label}</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{stat.value}</p>
            </div>
            <div className={`text-4xl ${stat.color} rounded-full p-3`}>
              {stat.icon}
            </div>
          </div>
          {stat.label !== 'Total Posts' && (
            <div className="mt-2">
              <div className="text-xs text-gray-500">
                {((stat.value / sentiment.total_posts) * 100).toFixed(1)}% of total
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  )
}

export default StatsCards
