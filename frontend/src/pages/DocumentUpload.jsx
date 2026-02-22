import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'
import Sidebar from '../components/Sidebar'
import UploadProgress from '../components/UploadProgress'
import { documentApi } from '../api/documentApi'
import { verificationApi } from '../api/verificationApi'

const DocumentUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null)
  const [documentType, setDocumentType] = useState('general')
  const [uploading, setUploading] = useState(false)
  const [progress, setProgress] = useState(0)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const navigate = useNavigate()

  const sidebarItems = [
    { label: 'Dashboard', path: '/customer' },
    { label: 'Upload Document', path: '/upload' }
  ]

  const handleFileSelect = (e) => {
    const file = e.target.files[0]
    if (file) {
      setSelectedFile(file)
      setError('')
      setSuccess('')
    }
  }

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a file')
      return
    }

    setUploading(true)
    setProgress(0)
    setError('')
    setSuccess('')

    try {
      setProgress(30)
      const uploadResponse = await documentApi.uploadDocument(selectedFile, documentType)

      if (!uploadResponse.success) {
        throw new Error(uploadResponse.message)
      }

      setProgress(60)
      const documentId = uploadResponse.data.document_id

      const verifyResponse = await verificationApi.verifyDocument(documentId)

      if (!verifyResponse.success) {
        throw new Error(verifyResponse.message)
      }

      setProgress(100)
      setSuccess('Document uploaded and verified successfully!')
      
      setTimeout(() => {
        navigate(`/verification/${verifyResponse.data.verification_id}`)
      }, 2000)

    } catch (err) {
      setError(err.response?.data?.message || err.message || 'Upload failed')
      setProgress(0)
    } finally {
      setUploading(false)
    }
  }

  return (
    <div>
      <Navbar />
      <div className="dashboard-layout">
        <Sidebar items={sidebarItems} />
        <div className="dashboard-content">
          <h1>Upload Document</h1>

          <div className="card">
            <h2>Document Upload</h2>

            {error && <div className="error-message">{error}</div>}
            {success && <div className="success-message">{success}</div>}

            <div className="form-group">
              <label className="form-label">Document Type</label>
              <select
                className="form-input"
                value={documentType}
                onChange={(e) => setDocumentType(e.target.value)}
                disabled={uploading}
              >
                <option value="general">General Document</option>
                <option value="id_proof">ID Proof</option>
                <option value="address_proof">Address Proof</option>
                <option value="income_proof">Income Proof</option>
                <option value="contract">Contract</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Select File</label>
              <div
                className="upload-area"
                onClick={() => !uploading && document.getElementById('fileInput').click()}
              >
                {selectedFile ? (
                  <div>
                    <p>Selected: {selectedFile.name}</p>
                    <p>Size: {(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
                  </div>
                ) : (
                  <p>Click to select a file or drag and drop</p>
                )}
              </div>
              <input
                id="fileInput"
                type="file"
                style={{ display: 'none' }}
                onChange={handleFileSelect}
                accept=".png,.jpg,.jpeg,.pdf"
                disabled={uploading}
              />
            </div>

            {uploading && <UploadProgress progress={progress} />}

            <button
              className="btn btn-primary"
              onClick={handleUpload}
              disabled={uploading || !selectedFile}
              style={{ width: '100%' }}
            >
              {uploading ? 'Uploading...' : 'Upload and Verify'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default DocumentUpload