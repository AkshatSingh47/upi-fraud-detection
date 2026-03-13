import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Shield, Activity, TrendingUp, LogOut, User } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import ManualInputForm from '../components/ManualInputForm'
import SMSInputForm from '../components/SMSInputForm'
import ImageInputForm from '../components/ImageInputForm'
import ResultCard from '../components/ResultCard'
import HistoryTable from '../components/HistoryTable'
import toast from 'react-hot-toast'

const Home = () => {
  const navigate = useNavigate()
  const [result, setResult] = useState(null)
  const [refreshHistory, setRefreshHistory] = useState(0)
  const [user, setUser] = useState(null)
  const [activeTab, setActiveTab] = useState('manual') // 'manual', 'sms', or 'image'

  useEffect(() => {
    const userData = localStorage.getItem('user')
    if (userData) {
      setUser(JSON.parse(userData))
    }
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    toast.success('Logged out successfully')
    navigate('/login')
  }

  const handlePredictionResult = (predictionResult) => {
    setResult(predictionResult)
    setRefreshHistory(prev => prev + 1) // Trigger history refresh
  }

  return (
    <div className="min-h-screen py-8 px-4">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-7xl mx-auto mb-8"
      >
        {/* User Info Bar */}
        <div className="flex justify-between items-center mb-8 glass-card p-4">
          <div className="flex items-center gap-3">
            <User className="w-6 h-6 text-primary-400" />
            <div>
              <p className="text-sm text-white/60">Welcome back,</p>
              <p className="font-semibold">{user?.full_name || 'User'}</p>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="btn-secondary flex items-center gap-2 text-sm px-4 py-2"
          >
            <LogOut className="w-4 h-4" />
            Logout
          </button>
        </div>
        <div className="text-center mb-12">
          <motion.div
            className="inline-flex items-center justify-center gap-3 mb-4"
            animate={{ scale: [1, 1.05, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            <Shield className="w-12 h-12 text-primary-400" />
            <h1 className="text-5xl font-bold bg-gradient-to-r from-primary-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
              UPI Fraud Detection
            </h1>
          </motion.div>
          <p className="text-xl text-white/70">
            AI-Driven Transaction Risk Intelligence System
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="glass-card p-6"
          >
            <div className="flex items-center gap-4">
              <div className="p-3 bg-green-500/20 rounded-lg">
                <Shield className="w-6 h-6 text-green-400" />
              </div>
              <div>
                <p className="text-white/60 text-sm">Protection Level</p>
                <p className="text-2xl font-bold">Real-Time</p>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="glass-card p-6"
          >
            <div className="flex items-center gap-4">
              <div className="p-3 bg-blue-500/20 rounded-lg">
                <Activity className="w-6 h-6 text-blue-400" />
              </div>
              <div>
                <p className="text-white/60 text-sm">ML Model</p>
                <p className="text-2xl font-bold">Active</p>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="glass-card p-6"
          >
            <div className="flex items-center gap-4">
              <div className="p-3 bg-purple-500/20 rounded-lg">
                <TrendingUp className="w-6 h-6 text-purple-400" />
              </div>
              <div>
                <p className="text-white/60 text-sm">Accuracy</p>
                <p className="text-2xl font-bold">95%+</p>
              </div>
            </div>
          </motion.div>
        </div>
      </motion.div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto">
        {/* Tab Navigation */}
        <div className="grid grid-cols-3 gap-3 mb-8">
          <button
            onClick={() => setActiveTab('manual')}
            className={`py-4 px-6 rounded-lg font-medium transition-all ${
              activeTab === 'manual'
                ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-lg'
                : 'glass-card text-white/60 hover:text-white'
            }`}
          >
            📝 Manual Input
          </button>
          <button
            onClick={() => setActiveTab('sms')}
            className={`py-4 px-6 rounded-lg font-medium transition-all ${
              activeTab === 'sms'
                ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-lg'
                : 'glass-card text-white/60 hover:text-white'
            }`}
          >
            📱 SMS Paste
          </button>
          <button
            onClick={() => setActiveTab('image')}
            className={`py-4 px-6 rounded-lg font-medium transition-all ${
              activeTab === 'image'
                ? 'bg-gradient-to-r from-blue-500 to-purple-500 text-white shadow-lg'
                : 'glass-card text-white/60 hover:text-white'
            }`}
          >
            📸 Image Upload
          </button>
        </div>

        {/* Input Forms */}
        <div className="mb-8">
          {activeTab === 'manual' && <ManualInputForm onResult={handlePredictionResult} />}
          {activeTab === 'sms' && <SMSInputForm onResult={handlePredictionResult} />}
          {activeTab === 'image' && <ImageInputForm onResult={handlePredictionResult} />}
        </div>

        {/* Result Display */}
        {result && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="mb-8"
          >
            <ResultCard result={result} />
          </motion.div>
        )}

        {/* History Table */}
        <HistoryTable refreshTrigger={refreshHistory} />
      </div>
    </div>
  )
}

export default Home

