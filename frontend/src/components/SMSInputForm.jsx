import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { MessageSquare, Send, Sparkles } from 'lucide-react'
import { predictSMS } from '../api/predict'
import toast from 'react-hot-toast'

const SMSInputForm = ({ onResult }) => {
  const [loading, setLoading] = useState(false)
  const [smsText, setSmsText] = useState('')

  // Multiple SMS examples with different scenarios
  const smsExamples = [
    // Legitimate transactions
    {
      text: "Your UPI transaction of Rs.1,234.56 to Amazon Pay on 12-Nov-25 at 14:30 was successful. UPI Ref: 123456789012",
      type: "Legit - Normal shopping"
    },
    {
      text: "Sent Rs.500.00 From HDFC Bank A/C *2340 To Zomato on 12/11/25 at 12:45. Ref: 234567890123",
      type: "Legit - Food delivery"
    },
    {
      text: "UPI transaction of Rs.2,500.00 to electricity@bill on 10-Nov-25 at 16:20 successful. Ref 345678901234",
      type: "Legit - Utility bill"
    },
    {
      text: "Rs.850.75 paid to swiggy@paytm from ICICI A/C *5678 on 11-Nov-25 at 19:30. Txn ID: 456789012345",
      type: "Legit - Dinner order"
    },
    
    // Late night transactions (suspicious timing)
    {
      text: "Your UPI transaction of Rs.50,000.00 to unknown-merchant on 12-Nov-25 at 02:30 was successful. UPI Ref: 987654321098",
      type: "Fraud - Late night + Large amount"
    },
    {
      text: "Sent Rs.25,000 From HDFC Bank A/C *8860 To verify@upi on 11/11/25 at 03:45. Ref: 876543210987",
      type: "Fraud - Suspicious receiver + Odd hour"
    },
    
    // Urgency scams
    {
      text: "URGENT: Your UPI account will be blocked! Send Rs.10,000 to customer-care@upi immediately to verify. Call 1800-FAKE-123",
      type: "Fraud - Urgency scam"
    },
    {
      text: "Action Required! Click here http://fake-bank.com to update KYC. Pay Rs.500 verification fee to kyc-update@upi. Ref: URGENT123",
      type: "Fraud - Phishing + Link"
    },
    
    // Prize/Lottery scams
    {
      text: "Congratulations! You won Rs.5,00,000 lottery! Send Rs.15,000 processing fee to lottery-winner@upi to claim. Ref: WIN123456",
      type: "Fraud - Lottery scam"
    },
    {
      text: "You are selected for Rs.10 Lakh prize! Transfer Rs.5,000 to prize@upi for registration. Limited time offer!",
      type: "Fraud - Prize scam"
    },
    
    // Large round amounts
    {
      text: "Your UPI transaction of Rs.1,00,000.00 to test-merchant on 12-Nov-25 at 23:15 was successful. UPI Ref: 765432109876",
      type: "Fraud - Large round amount + Late"
    },
    {
      text: "Sent Rs.50,000 From SBI A/C *9999 To unknown@paytm on 11/11/25 at 01:30. Ref: 654321098765",
      type: "Fraud - Round amount + Odd hour"
    },
    
    // Job scams
    {
      text: "Selected for Work From Home job! Pay Rs.3,000 registration fee to jobs@upi. Earn Rs.50,000/month. Apply now!",
      type: "Fraud - Job scam"
    },
    
    // Romance scams
    {
      text: "Hi dear, I need urgent help. Please send Rs.20,000 to help-friend@upi. Will return tomorrow. Emergency!",
      type: "Fraud - Romance/Friend scam"
    },
    
    // Investment scams
    {
      text: "Invest Rs.25,000 in crypto now! Double your money in 30 days. Send to crypto-invest@upi. Limited slots! Act fast!",
      type: "Fraud - Investment scam"
    },
    
    // More legitimate examples
    {
      text: "Received Rs.3,500.00 from salary@company in HDFC Bank A/C *1234 on 10-Nov-25 at 10:00. Ref: SAL123456789",
      type: "Legit - Salary credit"
    },
    {
      text: "Sent Rs.15,000.00 to landlord@gpay for rent on 01-Nov-25 at 09:30 from Axis Bank. Ref: RENT11252025",
      type: "Legit - Rent payment"
    },
    {
      text: "Rs.2,847.50 paid to phonepe@ybl for mobile recharge on 12-Nov-25 at 11:15. Txn: 147258369012",
      type: "Legit - Recharge"
    },
    {
      text: "Your UPI payment of Rs.899.00 to netflix@razorpay on 10-Nov-25 at 20:00 successful. Ref: NFLX123456",
      type: "Legit - Subscription"
    },
    {
      text: "Sent Rs.5,670.25 to hospital@paytm for medical bill on 09-Nov-25 at 15:45. From ICICI *7890. Ref: MED789012",
      type: "Legit - Medical payment"
    },
    
    // Mixed suspicious patterns
    {
      text: "BLOCK YOUR UPI NOW! Unauthorized transaction detected. Send Rs.1 to verify-security@upi to confirm it's you!",
      type: "Fraud - Fake security alert"
    },
    {
      text: "Your parcel delivery pending. Pay Rs.200 customs fee to delivery@upi. Track: http://fake-courier.com",
      type: "Fraud - Fake delivery"
    },
    {
      text: "Bank of India: Your A/C will be suspended. Update details by paying Rs.100 to update@upi within 24 hours.",
      type: "Fraud - Fake bank alert"
    }
  ]

  const handleUseExample = () => {
    // Randomly select an SMS example
    const randomIndex = Math.floor(Math.random() * smsExamples.length)
    const selectedExample = smsExamples[randomIndex]
    setSmsText(selectedExample.text)
    
    // Show which type of example was loaded
    toast.info(`Loaded: ${selectedExample.type}`, { duration: 3000 })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!smsText.trim()) {
      toast.error('Please enter SMS text')
      return
    }

    setLoading(true)

    try {
      const result = await predictSMS(smsText)

      onResult(result)

      if (result.prediction === 'Fraud') {
        toast.error('⚠️ Potential Fraud Detected!')
      } else {
        toast.success('✅ Transaction Appears Legitimate')
      }
    } catch (error) {
      toast.error(error.message || 'SMS parsing failed')
      console.error('SMS prediction error:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      className="glass-card p-8"
    >
      <div className="flex items-center gap-3 mb-6">
        <MessageSquare className="w-7 h-7 text-purple-400" />
        <h2 className="text-2xl font-bold">SMS Paste</h2>
      </div>

      <form onSubmit={handleSubmit} className="space-y-5">
        {/* SMS Text Area */}
        <div>
          <label className="block text-sm font-medium mb-2 text-white/80">
            Paste Transaction SMS
          </label>
          <textarea
            value={smsText}
            onChange={(e) => setSmsText(e.target.value)}
            placeholder="Paste your UPI transaction SMS here..."
            rows="8"
            className="glass-input w-full resize-none"
          />
        </div>

        {/* Example Button */}
        <motion.button
          type="button"
          onClick={handleUseExample}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="w-full py-2 px-4 rounded-lg border border-white/20 bg-white/5 hover:bg-white/10 transition-all duration-200 flex items-center justify-center gap-2 text-sm"
        >
          <Sparkles className="w-4 h-4" />
          Use Example SMS
        </motion.button>

        {/* Submit Button */}
        <button
          type="submit"
          disabled={loading}
          className="btn-primary w-full flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
                className="w-5 h-5 border-2 border-white border-t-transparent rounded-full"
              />
              Analyzing SMS...
            </>
          ) : (
            <>
              <Send className="w-5 h-5" />
              Detect Fraud
            </>
          )}
        </button>
      </form>

      {/* Info Box */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
        className="mt-6 p-4 rounded-lg bg-blue-500/10 border border-blue-500/20"
      >
        <p className="text-sm text-blue-300 mb-2">
          💡 <strong>Tip:</strong> Paste any UPI transaction SMS. The AI will automatically extract amount, receiver, date, and time.
        </p>
        <p className="text-xs text-blue-200/70">
          🎲 Click "Use Example SMS" multiple times to see different fraud/legitimate scenarios (23 examples available)
        </p>
      </motion.div>
    </motion.div>
  )
}

export default SMSInputForm

