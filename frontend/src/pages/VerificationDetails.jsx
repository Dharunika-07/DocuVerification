import React, { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'
import RiskScoreBadge from '../components/RiskScoreBadge'
import { verificationApi } from '../api/verificationApi'
import { documentApi } from '../api/documentApi'
import { useAuth } from '../hooks/useAuth'

const VerificationDetails = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const { user } = useAuth()
  const [verification, setVerification] = useState(null)
  const [document, setDocument] = useState(null)
  const [loading, setLoading] = useState(true)
  const [reviewing, setReviewing] = useState(false)
  const [decision, setDecision] = useState('approved')
  const [notes, setNotes] = useState('')
  const [error, setError] = useState('')

  useEffect(() => {
    fetchVerificationDetails()
  }, [id])

  const fetchVerificationDetails = async () => {
    try {
      const verificationResponse = await verificationApi.getVerification(id)
      if (verificationResponse.success) {
        setVerification(verificationResponse.data)

        const documentResponse = await documentApi.getDocument(
          verificationResponse.data.document_id
        )
        if (documentResponse.success) {
          setDocument(documentResponse.data)
        }
      }
    } catch (error) {
      console.error('Error fetching details:', error)
      setError('Failed to load verification details')
    } finally {
      setLoading(false)
    }
  }

  const handleReview = async () => {
    setReviewing(true)
    setError('')

    try {
      const response = await verificationApi.reviewVerification(id, decision, notes)
      if (response.success) {
        await fetchVerificationDetails()
        alert('Review submitted successfully')
        
        if (user.role === 'officer') {
          navigate('/officer')
        } else if (user.role === 'admin') {
          navigate('/admin')
        }
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Review submission failed')
    } finally {
      setReviewing(false)
    }
  }

  const getStatusClass = (status) => {
    if (status === 'approved') return 'status-approved'
    if (status === 'rejected') return 'status-rejected'
    return 'status-pending'
  }

  if (loading) {
    return (
      <div>
        <Navbar />
        <div className="container">
          <p>Loading...</p>
        </div>
      </div>
    )
  }

  if (!verification) {
    return (
      <div>
        <Navbar />
        <div className="container">
          <p>Verification not found</p>
        </div>
      </div>
    )
  }

  return (
    <div>
      <Navbar />
      <div className="container">
        <button
          className="btn btn-secondary"
          onClick={() => navigate(-1)}
          style={{ marginBottom: '20px' }}
        >
          Back
        </button>

        <h1>Verification Details</h1>

        {error && <div className="error-message">{error}</div>}

        <div className="card">
          <h2>Document Information</h2>
          <p><strong>Filename:</strong> {document?.filename}</p>
          <p><strong>Document Type:</strong> {document?.document_type}</p>
          <p><strong>Uploaded:</strong> {new Date(document?.uploaded_at).toLocaleString()}</p>
        </div>

        <div className="card">
          <h2>Verification Results</h2>
          <p>
            <strong>Status:</strong>{' '}
            <span className={`status-badge ${getStatusClass(verification.status)}`}>
              {verification.status}
            </span>
          </p>
          <p>
            <strong>Risk Assessment:</strong>{' '}
            <RiskScoreBadge
              riskScore={verification.risk_score}
              riskLevel={verification.risk_level}
            />
          </p>
          <p><strong>Auto Decision:</strong> {verification.auto_decision}</p>
          <p><strong>Created:</strong> {new Date(verification.created_at).toLocaleString()}</p>
        </div>

        {verification.fraud_indicators && verification.fraud_indicators.length > 0 && (
          <div className="card">
            <h2>Fraud Indicators</h2>
            <ul>
              {verification.fraud_indicators.map((indicator, index) => (
                <li key={index}>{indicator}</li>
              ))}
            </ul>
          </div>
        )}

        {verification.gemini_response && (
          <div className="card">
            <h2>AI Analysis</h2>
            <p><strong>Authentic:</strong> {verification.gemini_response.is_authentic ? 'Yes' : 'No'}</p>
            <p><strong>Confidence:</strong> {verification.gemini_response.confidence_score}%</p>
            {verification.gemini_response.analysis && (
              <p><strong>Analysis:</strong> {verification.gemini_response.analysis}</p>
            )}
          </div>
        )}

        {document?.extracted_text && (
          <div className="card">
            <h2>Extracted Text</h2>
            <div style={{ maxHeight: '200px', overflow: 'auto', backgroundColor: '#f6f6f6', padding: '10px', borderRadius: '4px' }}>
              <pre style={{ whiteSpace: 'pre-wrap' }}>{document.extracted_text}</pre>
            </div>
          </div>
        )}

        {verification.officer_decision && (
          <div className="card">
            <h2>Officer Review</h2>
            <p><strong>Decision:</strong> {verification.officer_decision}</p>
            <p><strong>Notes:</strong> {verification.officer_notes}</p>
            <p><strong>Reviewed:</strong> {new Date(verification.updated_at).toLocaleString()}</p>
          </div>
        )}

        {(user.role === 'officer' || user.role === 'admin') && verification.status === 'pending' && (
          <div className="card">
            <h2>Review Document</h2>
            <div className="form-group">
              <label className="form-label">Decision</label>
              <select
                className="form-input"
                value={decision}
                onChange={(e) => setDecision(e.target.value)}
              >
                <option value="approved">Approve</option>
                <option value="rejected">Reject</option>
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Notes</label>
              <textarea
                className="form-input"
                rows="4"
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="Add any notes about your decision..."
              />
            </div>
            <button
              className="btn btn-primary"
              onClick={handleReview}
              disabled={reviewing}
            >
              {reviewing ? 'Submitting...' : 'Submit Review'}
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default VerificationDetails