import { useState } from 'react'
import { Upload, X, Camera, Image as ImageIcon } from 'lucide-react'
import { predictImage } from '../api/predict'
import toast from 'react-hot-toast'

const ImageInputForm = ({ onResult }) => {
  const [loading, setLoading] = useState(false)
  const [imageFile, setImageFile] = useState(null)
  const [imagePreview, setImagePreview] = useState(null)
  const [dragActive, setDragActive] = useState(false)

  const handleImageSelect = (file) => {
    if (!file) return

    // Validate file type
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
    if (!validTypes.includes(file.type)) {
      toast.error('Please upload a valid image (JPG, PNG, or WebP)')
      return
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      toast.error('Image size should be less than 10MB')
      return
    }

    setImageFile(file)

    // Create preview
    const reader = new FileReader()
    reader.onloadend = () => {
      setImagePreview(reader.result)
    }
    reader.readAsDataURL(file)
  }

  const handleFileInput = (e) => {
    const file = e.target.files[0]
    handleImageSelect(file)
  }

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleImageSelect(e.dataTransfer.files[0])
    }
  }

  const handleClear = () => {
    setImageFile(null)
    setImagePreview(null)
    onResult(null)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!imageFile) {
      toast.error('Please select an image first')
      return
    }

    setLoading(true)

    try {
      // Create FormData for file upload
      const formData = new FormData()
      formData.append('file', imageFile)

      const result = await predictImage(formData)
      
      onResult(result)
      toast.success(`Detection complete: ${result.prediction}`, {
        icon: result.prediction === 'Fraud' ? '🚨' : '✅',
        duration: 3000
      })
    } catch (error) {
      console.error('Image prediction error:', error)
      toast.error(error.response?.data?.detail || 'Failed to process image. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="glass-card p-6">
      <div className="flex items-center gap-3 mb-6">
        <div className="p-2 glass-card rounded-lg">
          <Camera className="w-5 h-5 text-purple-400" />
        </div>
        <h2 className="text-xl font-semibold text-white">Image Upload</h2>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {!imagePreview ? (
          <div
            className={`border-2 border-dashed rounded-xl p-8 transition-all duration-300 ${
              dragActive
                ? 'border-purple-400 bg-purple-500/10'
                : 'border-white/20 hover:border-purple-400/50'
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <div className="flex flex-col items-center justify-center space-y-4">
              <div className="p-4 glass-card rounded-full">
                <Upload className="w-8 h-8 text-purple-400" />
              </div>

              <div className="text-center">
                <p className="text-lg font-medium text-white mb-1">
                  Drop your transaction screenshot here
                </p>
                <p className="text-sm text-white/60 mb-4">
                  or click to browse
                </p>
                <p className="text-xs text-white/40">
                  Supports: JPG, PNG, WebP (Max 10MB)
                </p>
              </div>

              <label className="btn-primary cursor-pointer">
                <ImageIcon className="w-4 h-4" />
                Select Image
                <input
                  type="file"
                  accept="image/jpeg,image/jpg,image/png,image/webp"
                  onChange={handleFileInput}
                  className="hidden"
                />
              </label>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            {/* Image Preview */}
            <div className="relative rounded-xl overflow-hidden glass-card p-4">
              <button
                type="button"
                onClick={handleClear}
                className="absolute top-6 right-6 p-2 glass-card rounded-lg hover:bg-red-500/20 transition-colors z-10"
              >
                <X className="w-4 h-4 text-white" />
              </button>

              <img
                src={imagePreview}
                alt="Transaction screenshot"
                className="w-full h-auto max-h-96 object-contain rounded-lg"
              />

              <div className="mt-4 p-3 glass-card rounded-lg">
                <p className="text-sm text-white/80">
                  <span className="font-medium text-white">File:</span>{' '}
                  {imageFile.name}
                </p>
                <p className="text-sm text-white/80 mt-1">
                  <span className="font-medium text-white">Size:</span>{' '}
                  {(imageFile.size / 1024).toFixed(2)} KB
                </p>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-3">
              <button
                type="submit"
                disabled={loading}
                className="btn-primary flex-1"
              >
                {loading ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    Processing Image...
                  </>
                ) : (
                  <>
                    <Camera className="w-4 h-4" />
                    Detect Fraud
                  </>
                )}
              </button>

              <button
                type="button"
                onClick={handleClear}
                className="btn-secondary"
                disabled={loading}
              >
                <X className="w-4 h-4" />
                Clear
              </button>
            </div>
          </div>
        )}

        {/* Tips */}
        <div className="p-4 glass-card rounded-lg">
          <p className="text-sm text-white/80 mb-2">
            💡 <span className="font-medium text-white">Tips for best results:</span>
          </p>
          <ul className="text-xs text-white/60 space-y-1 ml-4">
            <li>• Use clear, well-lit screenshots</li>
            <li>• Ensure text is readable and not blurry</li>
            <li>• Capture the entire transaction details</li>
            <li>• Avoid reflections or shadows</li>
          </ul>
        </div>
      </form>
    </div>
  )
}

export default ImageInputForm

