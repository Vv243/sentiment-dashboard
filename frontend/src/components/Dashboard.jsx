import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { sentimentAPI, collectionAPI } from '../services/api'
import SearchBar from './SearchBar'
import SentimentGauge from './SentimentGauge'
import SentimentChart from './SentimentChart'
import TrendingList from './TrendingList'
import StatsCards from './StatsCards'

function Dashboard() {
  const [selectedTicker, setSelectedTicker] = useState('TSLA')
  const [isCollecting, setIsCollecting] = useState(false)
  const queryClient = useQueryClient()

  // Fetch ticker sentiment
  const { data: sentiment, isLoading, error } = useQuery({
    queryKey: ['sentiment', selectedTicker],
    queryFn: () => sentimentAPI.getTickerSentiment(selectedTicker),
    enabled: !!selectedTicker,
    refetchInterval: 60000, // Refetch every minute
  })

  // Fetch historical data
  const { data: historical } = useQuery({
    queryKey: ['historical', selectedTicker],
    queryFn: () => sentimentAPI.getHistoricalSentiment(selectedTicker, 7),
    enabled: !!selectedTicker,
  })

  // Fetch trending
  const { data: trending } = useQuery({
    queryKey: ['trending'],
    queryFn: () => collectionAPI.getTrending(),
    refetchInterval: 300000, // Refetch every 5 minutes
  })

  // Collect data mutation
  const collectMutation = useMutation({
    mutationFn: (ticker) => collectionAPI.collectNow(ticker, 'reddit'),
    onMutate: () => {
      setIsCollecting(true)
    },
    onSuccess: () => {
      // Invalidate and refetch
      queryClient.invalidateQueries(['sentiment', selectedTicker])
      queryClient.invalidateQueries(['historical', selectedTicker])
      setIsCollecting(false)
    },
    onError: (error) => {
      console.error('Collection error:', error)
      setIsCollecting(false)
    },
  })

  const handleSearch = (ticker) => {
    setSelectedTicker(ticker.toUpperCase())
  }

  const handleCollect = () => {
    if (selectedTicker && !isCollecting) {
      collectMutation.mutate(selectedTicker)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                📊 Sentiment Dashboard
              </h1>
              <p className="text-gray-600 mt-1">
                Real-time social media sentiment analysis for stocks
              </p>
            </div>
            <div className="flex items-center space-x-4">
              <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                <span className="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"></span>
                Live
              </span>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Search Bar */}
        <div className="mb-8">
          <SearchBar onSearch={handleSearch} defaultValue={selectedTicker} />
        </div>

        {/* Main Content */}
        {isLoading && (
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-6 mb-8">
            <h3 className="text-red-800 font-semibold mb-2">Error Loading Data</h3>
            <p className="text-red-600">{error.message}</p>
            <button
              onClick={handleCollect}
              disabled={isCollecting}
              className="mt-4 bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700 disabled:opacity-50"
            >
              {isCollecting ? 'Collecting...' : 'Collect New Data'}
            </button>
          </div>
        )}

        {sentiment && (
          <>
            {/* Stats Cards */}
            <StatsCards sentiment={sentiment} />

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mt-8">
              {/* Main Sentiment Display */}
              <div className="lg:col-span-2 space-y-8">
                {/* Sentiment Gauge */}
                <div className="bg-white rounded-xl shadow-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-xl font-semibold text-gray-900">
                      Current Sentiment: {selectedTicker}
                    </h2>
                    <button
                      onClick={handleCollect}
                      disabled={isCollecting}
                      className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors flex items-center space-x-2"
                    >
                      {isCollecting ? (
                        <>
                          <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          <span>Collecting...</span>
                        </>
                      ) : (
                        <>
                          <span>🔄</span>
                          <span>Refresh Data</span>
                        </>
                      )}
                    </button>
                  </div>
                  <SentimentGauge sentiment={sentiment.current_sentiment} />
                </div>

                {/* Historical Chart */}
                {historical && (
                  <div className="bg-white rounded-xl shadow-lg p-6">
                    <h2 className="text-xl font-semibold text-gray-900 mb-4">
                      7-Day Sentiment Trend
                    </h2>
                    <SentimentChart data={historical.data_points} />
                  </div>
                )}
              </div>

              {/* Sidebar */}
              <div className="space-y-8">
                {/* Trending Topics */}
                {trending && (
                  <div className="bg-white rounded-xl shadow-lg p-6">
                    <h2 className="text-xl font-semibold text-gray-900 mb-4">
                      🔥 Trending Now
                    </h2>
                    <TrendingList trending={trending} onSelectTicker={handleSearch} />
                  </div>
                )}

                {/* Info Card */}
                <div className="bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl shadow-lg p-6 text-white">
                  <h3 className="text-lg font-semibold mb-2">About This Dashboard</h3>
                  <p className="text-blue-100 text-sm">
                    This dashboard analyzes real-time sentiment from social media posts
                    using VADER sentiment analysis. Data is collected from Reddit and
                    updated periodically.
                  </p>
                  <div className="mt-4 pt-4 border-t border-blue-400">
                    <p className="text-xs text-blue-100">
                      Last updated: {new Date(sentiment.last_updated).toLocaleString()}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-gray-600 text-sm">
            Built by Vinh Pham • Sentiment Analysis Dashboard • {new Date().getFullYear()}
          </p>
        </div>
      </footer>
    </div>
  )
}

export default Dashboard
