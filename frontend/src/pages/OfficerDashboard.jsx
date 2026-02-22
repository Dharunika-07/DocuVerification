import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'
import Sidebar from '../components/Sidebar'
import RiskScoreBadge from '../components/RiskScoreBadge'
import { verificationApi } from '../api/verificationApi'

const OfficerDashboard = () => {
  const [pendingVerifications, setPendingVerifications] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const sidebarItems = [
    { label: 'Dashboard', path: '/officer' }
  ]

  useEffect(() => {
    fetchPendingVerifications()
  }, [])

  const fetchPendingVerifications = async () => {
    try {
      setLoading(true)
      setError('')
      const response = await verificationApi.getPendingVerifications()
      if (response.success) {
        setPendingVerifications(response.data || [])
      } else {
        setError(response.message || 'Failed to load verifications')
        setPendingVerifications([])
      }
    } catch (error) {
      console.error('Error fetching verifications:', error)
      setError(error.response?.data?.message || 'Failed to load pending verifications')
      setPendingVerifications([])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <Navbar />
      <div className="dashboard-layout">
        <Sidebar items={sidebarItems} />
        <div className="dashboard-content">
          <h1>Officer Dashboard</h1>

          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-label">Pending Reviews</div>
              <div className="stat-value">{pendingVerifications.length}</div>
            </div>
          </div>

          <div className="card">
            <h2>Pending Verifications</h2>
            {error && <div className="error-message">{error}</div>}
            {loading ? (
              <p>Loading...</p>
            ) : pendingVerifications.length === 0 ? (
              <p>No pending verifications at the moment.</p>
            ) : (
              <table className="table">
                <thead>
                  <tr>
                    <th>Verification ID</th>
                    <th>Risk Level</th>
                    <th>Date</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {pendingVerifications.map((verification) => (
                    <tr key={verification._id}>
                      <td>{verification._id}</td>
                      <td>
                        <RiskScoreBadge
                          riskScore={verification.risk_score}
                          riskLevel={verification.risk_level}
                        />
                      </td>
                      <td>{new Date(verification.created_at).toLocaleDateString()}</td>
                      <td>
                        <button
                          className="btn btn-primary"
                          onClick={() => navigate(`/verification/${verification._id}`)}
                        >
                          Review
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default OfficerDashboard