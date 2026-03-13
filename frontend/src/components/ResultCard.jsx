import React from 'react'
import { motion } from 'framer-motion'
import { AlertTriangle, CheckCircle, Shield, TrendingUp, Clock, FileText } from 'lucide-react'
import ReactMarkdown from 'react-markdown'

const ResultCard = ({ result }) => {
  const isFraud = result.prediction === 'Fraud'

  const getRiskColor = (level) => {
    switch (level.toLowerCase()) {
      case 'critical':
      case 'high':
        return 'text-red-400 bg-red-500/20 border-red-500/30'
      case 'medium':
        return 'text-yellow-400 bg-yellow-500/20 border-yellow-500/30'
      case 'low':
      case 'normal':
        return 'text-green-400 bg-green-500/20 border-green-500/30'
      default:
        return 'text-blue-400 bg-blue-500/20 border-blue-500/30'
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`glass-card p-8 border-2 ${isFraud ? 'border-red-500/50' : 'border-green-500/50'}`}
    >
      <div className="flex items-start justify-between mb-6">
        <div className="flex items-center gap-4">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: 'spring', stiffness: 200 }}
            className={`p-4 rounded-full ${isFraud ? 'bg-red-500/20' : 'bg-green-500/20'}`}
          >
            {isFraud ? (
              <AlertTriangle className="w-10 h-10 text-red-400" />
            ) : (
              <CheckCircle className="w-10 h-10 text-green-400" />
            )}
          </motion.div>
          <div>
            <h3 className="text-3xl font-bold mb-1">
              {isFraud ? 'Fraud Detected' : 'Transaction Legitimate'}
            </h3>
            <p className={`text-lg ${isFraud ? 'text-red-300' : 'text-green-300'}`}>
              {result.reason}
            </p>
          </div>
        </div>

        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          className={`px-4 py-2 rounded-full border ${getRiskColor(result.risk_level)}`}
        >
          <p className="font-semibold">{result.risk_level} Risk</p>
        </motion.div>
      </div>

      {/* Main Details Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
        <div className="glass-card p-4">
          <div className="flex items-center gap-2 mb-2">
            <Shield className="w-5 h-5 text-primary-400" />
            <p className="text-sm text-white/60">Confidence</p>
          </div>
          <p className="text-2xl font-bold">{(result.confidence * 100).toFixed(1)}%</p>
        </div>

        <div className="glass-card p-4">
          <div className="flex items-center gap-2 mb-2">
            <TrendingUp className="w-5 h-5 text-purple-400" />
            <p className="text-sm text-white/60">Prediction</p>
          </div>
          <p className={`text-2xl font-bold ${isFraud ? 'text-red-400' : 'text-green-400'}`}>
            {result.prediction}
          </p>
        </div>

        {result.amount && (
          <div className="glass-card p-4">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xl text-yellow-400">₹</span>
              <p className="text-sm text-white/60">Amount</p>
            </div>
            <p className="text-2xl font-bold">₹{result.amount.toLocaleString('en-IN')}</p>
          </div>
        )}

        {result.time && (
          <div className="glass-card p-4">
            <div className="flex items-center gap-2 mb-2">
              <Clock className="w-5 h-5 text-blue-400" />
              <p className="text-sm text-white/60">Time</p>
            </div>
            <p className="text-2xl font-bold">{result.time}</p>
          </div>
        )}
      </div>

      {/* Additional Information */}
      {(result.reference_number || result.transaction_type || result.bank_name || result.account || result.receiver) && (
        <div className="mt-6 p-4 rounded-lg bg-white/5 border border-white/10">
          <h4 className="text-sm font-semibold text-white/70 mb-3">Transaction Details</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
            {result.reference_number && (
              <div>
                <span className="text-white/50">Reference:</span>
                <span className="ml-2 font-mono text-white/90">{result.reference_number}</span>
              </div>
            )}
            {result.transaction_type && (
              <div>
                <span className="text-white/50">Type:</span>
                <span className="ml-2 text-white/90">{result.transaction_type}</span>
              </div>
            )}
            {result.bank_name && (
              <div>
                <span className="text-white/50">Bank:</span>
                <span className="ml-2 text-white/90">{result.bank_name}</span>
              </div>
            )}
            {result.account && (
              <div>
                <span className="text-white/50">From:</span>
                <span className="ml-2 text-white/90">{result.account}</span>
              </div>
            )}
            {result.receiver && (
              <div>
                <span className="text-white/50">To:</span>
                <span className="ml-2 text-white/90">{result.receiver}</span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Detailed Analysis Report */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
        className="mt-6 p-6 rounded-lg bg-white/5 border border-white/10"
      >
        <div className="flex items-center gap-2 mb-4">
          <FileText className="w-5 h-5 text-primary-400" />
          <h4 className="text-lg font-semibold">Detailed Analysis Report</h4>
        </div>
        <div className="prose prose-invert max-w-none text-sm">
          <ReactMarkdown
            components={{
              h2: ({node, ...props}) => <h2 className="text-lg font-bold text-white mt-4 mb-2" {...props} />,
              h3: ({node, ...props}) => <h3 className="text-base font-semibold text-white/90 mt-3 mb-1" {...props} />,
              p: ({node, ...props}) => <p className="text-white/70 mb-3 leading-relaxed" {...props} />,
              ul: ({node, ...props}) => <ul className="list-disc list-inside space-y-1 mb-3 text-white/70" {...props} />,
              li: ({node, ...props}) => <li className="ml-2" {...props} />,
              strong: ({node, ...props}) => <strong className="text-white font-semibold" {...props} />,
            }}
          >
            {result.reason}
          </ReactMarkdown>
        </div>
      </motion.div>

      {/* Quick Recommendation */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
        className={`mt-4 p-4 rounded-lg border ${
          isFraud 
            ? 'bg-red-500/10 border-red-500/30'
            : 'bg-green-500/10 border-green-500/30'
        }`}
      >
        <p className={`font-semibold mb-2 ${isFraud ? 'text-red-300' : 'text-green-300'}`}>
          {isFraud ? '🚨 Immediate Action Required' : '✅ Safe to Proceed'}
        </p>
        <p className={`text-sm ${isFraud ? 'text-red-200' : 'text-green-200'}`}>
          {isFraud
            ? 'DO NOT proceed with this transaction. If money was already sent, contact your bank immediately and file a fraud report.'
            : 'This transaction passed all fraud checks. However, always verify receiver details and keep transaction records.'}
        </p>
      </motion.div>
    </motion.div>
  )
}

export default ResultCard

