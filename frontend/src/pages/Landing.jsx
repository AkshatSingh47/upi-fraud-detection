import React from 'react'
import { motion } from 'framer-motion'
import { Shield, Zap, Lock, TrendingUp, Users, CheckCircle, ArrowRight } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

const Landing = () => {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="min-h-screen flex items-center justify-center px-4 py-20">
        <div className="max-w-6xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <motion.div
              className="inline-flex items-center justify-center gap-3 mb-6"
              animate={{ scale: [1, 1.05, 1] }}
              transition={{ duration: 3, repeat: Infinity }}
            >
              <Shield className="w-16 h-16 text-primary-400" />
            </motion.div>

            <h1 className="text-6xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-primary-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
              UPI Fraud Detection
            </h1>

            <p className="text-2xl md:text-3xl text-white/80 mb-4">
              AI-Driven Transaction Risk Intelligence
            </p>

            <p className="text-lg text-white/60 mb-12 max-w-2xl mx-auto">
              Protect your UPI transactions with cutting-edge AI technology.
              Detect fraud in real-time with 95%+ accuracy.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => navigate('/register')}
                className="btn-primary text-lg px-8 py-4 flex items-center justify-center gap-2"
              >
                Get Started Free
                <ArrowRight className="w-5 h-5" />
              </motion.button>

              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => navigate('/login')}
                className="btn-secondary text-lg px-8 py-4"
              >
                Sign In
              </motion.button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold mb-4">Powerful Features</h2>
            <p className="text-xl text-white/60">Everything you need to stay protected</p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                icon: <Zap className="w-10 h-10" />,
                title: 'Real-Time Detection',
                description: 'Instant fraud analysis on every transaction with AI-powered insights'
              },
              {
                icon: <Lock className="w-10 h-10" />,
                title: 'Secure & Private',
                description: 'Your data is encrypted and never shared with third parties'
              },
              {
                icon: <TrendingUp className="w-10 h-10" />,
                title: '95%+ Accuracy',
                description: 'Advanced machine learning models trained on millions of transactions'
              },
              {
                icon: <Users className="w-10 h-10" />,
                title: 'User-Friendly',
                description: 'Simple interface - paste SMS or enter details manually'
              },
              {
                icon: <Shield className="w-10 h-10" />,
                title: 'Comprehensive Reports',
                description: 'Detailed fraud analysis with actionable recommendations'
              },
              {
                icon: <CheckCircle className="w-10 h-10" />,
                title: 'Transaction History',
                description: 'Track and search all your analyzed transactions'
              }
            ].map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="glass-card p-8 hover:scale-105 transition-transform"
              >
                <div className="text-primary-400 mb-4">{feature.icon}</div>
                <h3 className="text-xl font-bold mb-3">{feature.title}</h3>
                <p className="text-white/60">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold mb-4">How It Works</h2>
            <p className="text-xl text-white/60">Simple, fast, and effective</p>
          </motion.div>

          <div className="space-y-8">
            {[
              {
                step: '1',
                title: 'Enter Transaction Details',
                description: 'Paste your UPI SMS or manually enter transaction information'
              },
              {
                step: '2',
                title: 'AI Analysis',
                description: 'Our advanced AI analyzes patterns, timing, and other fraud indicators'
              },
              {
                step: '3',
                title: 'Get Results',
                description: 'Receive instant fraud assessment with detailed explanations and recommendations'
              }
            ].map((step, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.2 }}
                className="flex gap-6 items-start"
              >
                <div className="flex-shrink-0 w-16 h-16 rounded-full bg-gradient-to-r from-primary-500 to-purple-600 flex items-center justify-center text-2xl font-bold">
                  {step.step}
                </div>
                <div>
                  <h3 className="text-2xl font-bold mb-2">{step.title}</h3>
                  <p className="text-white/60 text-lg">{step.description}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          className="max-w-4xl mx-auto glass-card p-12 text-center"
        >
          <h2 className="text-4xl font-bold mb-4">Ready to Protect Your Transactions?</h2>
          <p className="text-xl text-white/60 mb-8">
            Join thousands of users who trust our AI-powered fraud detection
          </p>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => navigate('/register')}
            className="btn-primary text-lg px-12 py-4"
          >
            Start Now - It's Free
          </motion.button>
        </motion.div>
      </section>
    </div>
  )
}

export default Landing

