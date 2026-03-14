import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://upi-fraud-detection-a5iz.onrender.com'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const predictManual = async (data) => {
  try {
    const response = await api.post('/predict/manual', data)
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Prediction failed')
  }
}

export const predictSMS = async (text) => {
  try {
    const response = await api.post('/predict/sms', { text })
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'SMS parsing failed')
  }
}

export const predictImage = async (formData) => {
  try {
    const response = await api.post('/predict/image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Image processing failed')
  }
}

export const getLogs = async (limit = 50, prediction = null) => {
  try {
    const params = { limit }
    if (prediction) params.prediction = prediction
    
    const response = await api.get('/logs', { params })
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch logs')
  }
}

export const getStats = async () => {
  try {
    const response = await api.get('/logs/stats')
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to fetch statistics')
  }
}

export default api

