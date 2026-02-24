
import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'
import Sidebar from '../components/Sidebar'
import RiskScoreBadge from '../components/RiskScoreBadge'
import { verificationApi } from '../api/verificationApi'

const AdminDashboard = () => {
  const [statistics, setStatistics] = useState(null)
  const [allVerifications, setAllVerifications] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const sidebarItems = [
    { label: 'Dashboard', path: '/admin' }
  ]

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      setError('')
      const [statsResponse, verificationsResponse] = await Promise.all([
        verificationApi.getStatistics(),
        verificationApi.getAllVerifications()
      ])

      if (statsResponse.success) {
        setStatistics(statsResponse.data || {})
      }

      if (verificationsResponse.success) {
        setAllVerifications(verificationsResponse.data || [])
      }
    } catch (error) {
      console.error('Error fetching data:', error)
      setError('Failed to load dashboard data')
      setStatistics({})
      setAllVerifications([])
    } finally {
      setLoading(false)
    }
  }

  const getStatusClass = (status) => {
    if (status === 'approved') return 'status-approved'
    if (status === 'rejected') return 'status-rejected'
    return 'status-pending'
  }

  return (
    <div>
      <Navbar />
      <div className="dashboard-layout">
        <Sidebar items={sidebarItems} />
        <div className="dashboard-content">
          <h1>Admin Dashboard</h1>

          {error && <div className="error-message">{error}</div>}

          {loading ? (
            <p>Loading...</p>
          ) : (
            <>
              <div className="stats-grid">
                <div className="stat-card">
                  <div className="stat-label">Total Verifications</div>
                  <div className="stat-value">{statistics?.total_verifications || 0}</div>
                </div>
                <div className="stat-card">
                  <div className="stat-label">Approved</div>
                  <div className="stat-value">{statistics?.approved || 0}</div>
                </div>
                <div className="stat-card">
                  <div className="stat-label">Rejected</div>
                  <div className="stat-value">{statistics?.rejected || 0}</div>
                </div>
                <div className="stat-card">
                  <div className="stat-label">Pending</div>
                  <div className="stat-value">{statistics?.pending || 0}</div>
                </div>
              </div>

              <div className="card">
                <h2>Risk Distribution</h2>
                <div className="stats-grid">
                  <div className="stat-card">
                    <div className="stat-label">Low Risk</div>
                    <div className="stat-value">{statistics?.risk_distribution?.low || 0}</div>
                  </div>
                  <div className="stat-card">
                    <div className="stat-label">Medium Risk</div>
                    <div className="stat-value">{statistics?.risk_distribution?.medium || 0}</div>
                  </div>
                  <div className="stat-card">
                    <div className="stat-label">High Risk</div>
                    <div className="stat-value">{statistics?.risk_distribution?.high || 0}</div>
                  </div>
                </div>
              </div>

              <div className="card">
                <h2>All Verifications</h2>
                <table className="table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>User ID</th>
                      <th>Risk Level</th>
                      <th>Status</th>
                      <th>Date</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {allVerifications.map((verification) => (
                      <tr key={verification._id}>
                        <td>{verification._id}</td>
                        <td>{verification.user_id}</td>
                        <td>
                          <RiskScoreBadge
                            riskScore={verification.risk_score}
                            riskLevel={verification.risk_level}
                          />
                        </td>
                        <td>
                          <span className={`status-badge ${getStatusClass(verification.status)}`}>
                            {verification.status}
                          </span>
                        </td>
                        <td>{new Date(verification.created_at).toLocaleDateString()}</td>
                        <td>
                          <button
                            className="btn btn-primary"
                            onClick={() => navigate(`/verification/${verification._id}`)}
                          >
                            View
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default AdminDashboard