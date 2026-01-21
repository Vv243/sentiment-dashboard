/**
 * API service for sentiment analysis backend
 */
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// API endpoints
export const sentimentAPI = {
  // Analyze text
  analyzeText: async (text, useVader = true, useFinbert = false) => {
    const response = await api.post('/api/v1/sentiment/analyze', {
      text,
      use_vader: useVader,
      use_finbert: useFinbert,
    })
    return response.data
  },

  // Get ticker sentiment
  getTickerSentiment: async (ticker) => {
    const response = await api.get(`/api/v1/sentiment/${ticker}`)
    return response.data
  },

  // Get historical sentiment
  getHistoricalSentiment: async (ticker, days = 7) => {
    const response = await api.get(`/api/v1/sentiment/${ticker}/history`, {
      params: { days },
    })
    return response.data
  },
}

export const collectionAPI = {
  // Start collection
  startCollection: async (ticker, source = 'reddit') => {
    const response = await api.post('/api/v1/collection/start', {
      ticker,
      source,
    })
    return response.data
  },

  // Collect now (synchronous)
  collectNow: async (ticker, source = 'reddit') => {
    const response = await api.post(`/api/v1/collection/collect-now/${ticker}`, null, {
      params: { source },
    })
    return response.data
  },

  // Get trending
  getTrending: async () => {
    const response = await api.get('/api/v1/collection/trending')
    return response.data
  },
}

export const healthAPI = {
  // Health check
  checkHealth: async () => {
    const response = await api.get('/health')
    return response.data
  },

  // Get metrics
  getMetrics: async () => {
    const response = await api.get('/metrics')
    return response.data
  },
}

export default api
