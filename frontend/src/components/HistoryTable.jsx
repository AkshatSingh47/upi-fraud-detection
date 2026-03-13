import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { History, AlertCircle, CheckCircle, Filter, RefreshCw, Search } from 'lucide-react'
import { getLogs } from '../api/predict'
import toast from 'react-hot-toast'

const HistoryTable = ({ refreshTrigger }) => {
  const [logs, setLogs] = useState([])
  const [filteredLogs, setFilteredLogs] = useState([])
  const [loading, setLoading] = useState(false)
  const [filter, setFilter] = useState('all')
  const [searchTerm, setSearchTerm] = useState('')

  const fetchLogs = async () => {
    setLoading(true)
    try {
      const filterValue = filter === 'all' ? null : filter
      const data = await getLogs(100, filterValue)
      setLogs(data)
      setFilteredLogs(data)
    } catch (error) {
      toast.error('Failed to load history')
      console.error('Fetch logs error:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchLogs()
  }, [filter, refreshTrigger])

  useEffect(() => {
    if (searchTerm) {
      const filtered = logs.filter(log => 
        log.receiver?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        log.reference_number?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        log.amount?.toString().includes(searchTerm) ||
        log.account?.toLowerCase().includes(searchTerm.toLowerCase())
      )
      setFilteredLogs(filtered)
    } else {
      setFilteredLogs(logs)
    }
  }, [searchTerm, logs])

  const getRiskBadgeColor = (level) => {
    switch (level.toLowerCase()) {
      case 'critical':
      case 'high':
        return 'bg-red-500/20 text-red-300 border-red-500/30'
      case 'medium':
        return 'bg-yellow-500/20 text-yellow-300 border-yellow-500/30'
      case 'low':
      case 'normal':
        return 'bg-green-500/20 text-green-300 border-green-500/30'
      default:
        return 'bg-blue-500/20 text-blue-300 border-blue-500/30'
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-card p-8"
    >
      {/* Header */}
      <div className="space-y-4 mb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <History className="w-7 h-7 text-primary-400" />
            <h2 className="text-2xl font-bold">Transaction History</h2>
            <span className="text-sm text-white/50">({filteredLogs.length} transactions)</span>
          </div>

          <div className="flex items-center gap-3">
            {/* Filter */}
            <select
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
              className="glass-input px-4 py-2"
            >
              <option value="all">All Transactions</option>
              <option value="Fraud">Fraud Only</option>
              <option value="Legit">Legitimate Only</option>
            </select>

            {/* Refresh Button */}
            <motion.button
              whileHover={{ rotate: 180 }}
              transition={{ duration: 0.3 }}
              onClick={fetchLogs}
              disabled={loading}
              className="p-2 rounded-lg bg-white/10 hover:bg-white/20 border border-white/20 transition-colors"
            >
              <RefreshCw className="w-5 h-5" />
            </motion.button>
          </div>
        </div>

        {/* Search Bar */}
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-white/40" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search by receiver, reference, amount, or account..."
            className="glass-input w-full pl-11"
          />
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
              className="w-12 h-12 border-4 border-primary-400 border-t-transparent rounded-full"
            />
          </div>
        ) : filteredLogs.length === 0 ? (
          <div className="text-center py-12 text-white/50">
            <History className="w-16 h-16 mx-auto mb-4 opacity-50" />
            <p className="text-lg">
              {searchTerm ? 'No matching transactions found' : 'No transactions yet'}
            </p>
            <p className="text-sm">
              {searchTerm ? 'Try a different search term' : 'Start by analyzing a transaction above'}
            </p>
          </div>
        ) : (
          <table className="w-full">
            <thead>
              <tr className="border-b border-white/10">
                <th className="text-left py-3 px-4 text-white/60 font-semibold">ID</th>
                <th className="text-left py-3 px-4 text-white/60 font-semibold">Type</th>
                <th className="text-left py-3 px-4 text-white/60 font-semibold">Amount</th>
                <th className="text-left py-3 px-4 text-white/60 font-semibold">Receiver</th>
                <th className="text-left py-3 px-4 text-white/60 font-semibold">Ref No.</th>
                <th className="text-left py-3 px-4 text-white/60 font-semibold">Time</th>
                <th className="text-left py-3 px-4 text-white/60 font-semibold">Prediction</th>
                <th className="text-left py-3 px-4 text-white/60 font-semibold">Risk</th>
              </tr>
            </thead>
            <tbody>
              {filteredLogs.map((log, index) => (
                <motion.tr
                  key={log.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.05 }}
                  className="border-b border-white/5 hover:bg-white/5 transition-colors"
                >
                  <td className="py-3 px-4 text-white/80">#{log.id}</td>
                  <td className="py-3 px-4 text-white/70 text-sm">
                    <span className={`px-2 py-1 rounded ${
                      log.transaction_type === 'Sent' ? 'bg-red-500/20 text-red-300' :
                      log.transaction_type === 'Received' ? 'bg-green-500/20 text-green-300' :
                      'bg-blue-500/20 text-blue-300'
                    }`}>
                      {log.transaction_type || 'N/A'}
                    </span>
                  </td>
                  <td className="py-3 px-4 font-semibold">₹{log.amount.toLocaleString('en-IN')}</td>
                  <td className="py-3 px-4 text-white/80">{log.receiver || 'N/A'}</td>
                  <td className="py-3 px-4 text-white/60 text-sm font-mono">{log.reference_number || '-'}</td>
                  <td className="py-3 px-4 text-white/60 text-sm">{log.time || 'N/A'}</td>
                  <td className="py-3 px-4">
                    <span className={`flex items-center gap-2 font-semibold ${
                      log.prediction === 'Fraud' ? 'text-red-400' : 'text-green-400'
                    }`}>
                      {log.prediction === 'Fraud' ? (
                        <AlertCircle className="w-4 h-4" />
                      ) : (
                        <CheckCircle className="w-4 h-4" />
                      )}
                      {log.prediction}
                    </span>
                  </td>
                  <td className="py-3 px-4">
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${getRiskBadgeColor(log.risk_level)}`}>
                      {log.risk_level}
                    </span>
                  </td>
                </motion.tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </motion.div>
  )
}

export default HistoryTable

