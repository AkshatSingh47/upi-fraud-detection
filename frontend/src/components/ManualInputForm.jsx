import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { User, Calendar, Clock, CreditCard, Send, X } from 'lucide-react'
import { predictManual } from '../api/predict'
import toast from 'react-hot-toast'

const ManualInputForm = ({ onResult }) => {
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    account: '',
    amount: '',
    receiver: '',
    date: '',
    time: '',
    reference_number: '',
    transaction_number: '',
    transaction_type: 'Sent',
    bank_name: '',
  })

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    })
  }

  const handleClear = () => {
    setFormData({
      account: '',
      amount: '',
      receiver: '',
      date: '',
      time: '',
      reference_number: '',
      transaction_number: '',
      transaction_type: 'Sent',
      bank_name: '',
    })
    onResult(null)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    // Validation
    if (!formData.account || !formData.amount || !formData.receiver || !formData.date || !formData.time) {
      toast.error('Please fill all fields')
      return
    }

    if (parseFloat(formData.amount) <= 0) {
      toast.error('Amount must be greater than 0')
      return
    }

    setLoading(true)

    try {
      const result = await predictManual({
        ...formData,
        amount: parseFloat(formData.amount),
      })

      onResult(result)

      if (result.prediction === 'Fraud') {
        toast.error('⚠️ Potential Fraud Detected!')
      } else {
        toast.success('✅ Transaction Appears Legitimate')
      }
    } catch (error) {
      toast.error(error.message || 'Prediction failed')
      console.error('Manual prediction error:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      className="glass-card p-8"
    >
      <div className="flex items-center gap-3 mb-6">
        <CreditCard className="w-7 h-7 text-primary-400" />
        <h2 className="text-2xl font-bold">Manual Input</h2>
      </div>

      <form onSubmit={handleSubmit} className="space-y-5">
        {/* Account */}
        <div>
          <label className="block text-sm font-medium mb-2 text-white/80">
            Account / UPI ID
          </label>
          <div className="relative">
            <User className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-white/40" />
            <input
              type="text"
              name="account"
              value={formData.account}
              onChange={handleChange}
              placeholder="user@paytm"
              className="glass-input w-full pl-11"
            />
          </div>
        </div>

        {/* Amount */}
        <div>
          <label className="block text-sm font-medium mb-2 text-white/80">
            Amount (₹)
          </label>
          <div className="relative">
            <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-lg text-white/60 font-semibold">₹</span>
            <input
              type="number"
              name="amount"
              value={formData.amount}
              onChange={handleChange}
              placeholder="5000.00"
              step="0.01"
              min="0"
              className="glass-input w-full pl-11"
            />
          </div>
        </div>

        {/* Receiver */}
        <div>
          <label className="block text-sm font-medium mb-2 text-white/80">
            Receiver / Merchant
          </label>
          <div className="relative">
            <User className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-white/40" />
            <input
              type="text"
              name="receiver"
              value={formData.receiver}
              onChange={handleChange}
              placeholder="merchant@upi"
              className="glass-input w-full pl-11"
            />
          </div>
        </div>

        {/* Date and Time */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-2 text-white/80">
              Date
            </label>
            <div className="relative">
              <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-white/40" />
              <input
                type="date"
                name="date"
                value={formData.date}
                onChange={handleChange}
                className="glass-input w-full pl-11"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2 text-white/80">
              Time
            </label>
            <div className="relative">
              <Clock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-white/40" />
              <input
                type="time"
                name="time"
                value={formData.time}
                onChange={handleChange}
                className="glass-input w-full pl-11"
              />
            </div>
          </div>
        </div>

        {/* Reference Number */}
        <div>
          <label className="block text-sm font-medium mb-2 text-white/80">
            Reference Number (Optional)
          </label>
          <input
            type="text"
            name="reference_number"
            value={formData.reference_number}
            onChange={handleChange}
            placeholder="113988090014"
            className="glass-input w-full"
          />
        </div>

        {/* Transaction Number */}
        <div>
          <label className="block text-sm font-medium mb-2 text-white/80">
            Transaction Number (Optional)
          </label>
          <input
            type="text"
            name="transaction_number"
            value={formData.transaction_number}
            onChange={handleChange}
            placeholder="TXN123456789"
            className="glass-input w-full"
          />
        </div>

        {/* Transaction Type and Bank */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-2 text-white/80">
              Transaction Type
            </label>
            <select
              name="transaction_type"
              value={formData.transaction_type}
              onChange={handleChange}
              className="glass-input w-full"
            >
              <option value="Sent">Sent</option>
              <option value="Received">Received</option>
              <option value="Paid">Paid</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2 text-white/80">
              Bank Name (Optional)
            </label>
            <input
              type="text"
              name="bank_name"
              value={formData.bank_name}
              onChange={handleChange}
              placeholder="HDFC Bank"
              className="glass-input w-full"
            />
          </div>
        </div>

        {/* Buttons */}
        <div className="flex gap-4 pt-4">
          <button
            type="submit"
            disabled={loading}
            className="btn-primary flex-1 flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                  className="w-5 h-5 border-2 border-white border-t-transparent rounded-full"
                />
                Analyzing...
              </>
            ) : (
              <>
                <Send className="w-5 h-5" />
                Detect Fraud
              </>
            )}
          </button>

          <button
            type="button"
            onClick={handleClear}
            className="btn-secondary flex items-center justify-center gap-2"
          >
            <X className="w-5 h-5" />
            Clear
          </button>
        </div>
      </form>
    </motion.div>
  )
}

export default ManualInputForm

