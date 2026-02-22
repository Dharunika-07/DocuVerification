// import React, { useState, useEffect } from 'react'
// import { useNavigate } from 'react-router-dom'
// import Navbar from '../components/Navbar'
// import Sidebar from '../components/Sidebar'
// import RiskScoreBadge from '../components/RiskScoreBadge'
// import { documentApi } from '../api/documentApi'
// import { verificationApi } from '../api/verificationApi'

// const CustomerDashboard = () => {
//   const [documents, setDocuments] = useState([])
//   const [verifications, setVerifications] = useState([])
//   const [loading, setLoading] = useState(true)
//   const navigate = useNavigate()

//   const sidebarItems = [
//     { label: 'Dashboard', path: '/customer' },
//     { label: 'Upload Document', path: '/upload' }
//   ]

//   useEffect(() => {
//     fetchData()
//   }, [])

//   const fetchData = async () => {
//     try {
//       const [docsResponse, verificationsResponse] = await Promise.all([
//         documentApi.getMyDocuments(),
//         verificationApi.getMyVerifications()
//       ])

//       if (docsResponse.success) {
//         setDocuments(docsResponse.data)
//       }

//       if (verificationsResponse.success) {
//         setVerifications(verificationsResponse.data)
//       }
//     } catch (error) {
//       console.error('Error fetching data:', error)
//     } finally {
//       setLoading(false)
//     }
//   }

//   const getStatusClass = (status) => {
//     if (status === 'approved') return 'status-approved'
//     if (status === 'rejected') return 'status-rejected'
//     return 'status-pending'
//   }

//   return (
//     <div>
//       <Navbar />
//       <div className="dashboard-layout">
//         <Sidebar items={sidebarItems} />
//         <div className="dashboard-content">
//           <h1>Customer Dashboard</h1>

//           <div className="stats-grid">
//             <div className="stat-card">
//               <div className="stat-label">Total Documents</div>
//               <div className="stat-value">{documents.length}</div>
//             </div>
//             <div className="stat-card">
//               <div className="stat-label">Pending Verifications</div>
//               <div className="stat-value">
//                 {verifications.filter(v => v.status === 'pending').length}
//               </div>
//             </div>
//             <div className="stat-card">
//               <div className="stat-label">Approved</div>
//               <div className="stat-value">
//                 {verifications.filter(v => v.status === 'approved').length}
//               </div>
//             </div>
//             <div className="stat-card">
//               <div className="stat-label">Rejected</div>
//               <div className="stat-value">
//                 {verifications.filter(v => v.status === 'rejected').length}
//               </div>
//             </div>
//           </div>

//           <div className="card">
//             <h2>Recent Verifications</h2>
//             {loading ? (
//               <p>Loading...</p>
//             ) : verifications.length === 0 ? (
//               <p>No verifications yet. Upload a document to get started.</p>
//             ) : (
//               <table className="table">
//                 <thead>
//                   <tr>
//                     <th>Document</th>
//                     <th>Risk Level</th>
//                     <th>Status</th>
//                     <th>Date</th>
//                     <th>Action</th>
//                   </tr>
//                 </thead>
//                 <tbody>
//                   {verifications.map((verification) => {
//                     const doc = documents.find(d => d._id === verification.document_id)
//                     return (
//                       <tr key={verification._id}>
//                         <td>{doc?.filename || 'Unknown'}</td>
//                         <td>
//                           <RiskScoreBadge
//                             riskScore={verification.risk_score}
//                             riskLevel={verification.risk_level}
//                           />
//                         </td>
//                         <td>
//                           <span className={`status-badge ${getStatusClass(verification.status)}`}>
//                             {verification.status}
//                           </span>
//                         </td>
//                         <td>{new Date(verification.created_at).toLocaleDateString()}</td>
//                         <td>
//                           <button
//                             className="btn btn-primary"
//                             onClick={() => navigate(`/verification/${verification._id}`)}
//                           >
//                             View Details
//                           </button>
//                         </td>
//                       </tr>
//                     )
//                   })}
//                 </tbody>
//               </table>
//             )}
//           </div>
//         </div>
//       </div>
//     </div>
//   )
// }

// export default CustomerDashboard

import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'
import Sidebar from '../components/Sidebar'
import RiskScoreBadge from '../components/RiskScoreBadge'
import { documentApi } from '../api/documentApi'
import { verificationApi } from '../api/verificationApi'

const CustomerDashboard = () => {
  const [documents, setDocuments] = useState([])
  const [verifications, setVerifications] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const sidebarItems = [
    { label: 'Dashboard', path: '/customer' },
    { label: 'Upload Document', path: '/upload' }
  ]

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      setError('')
      const [docsResponse, verificationsResponse] = await Promise.all([
        documentApi.getMyDocuments(),
        verificationApi.getMyVerifications()
      ])

      if (docsResponse.success) {
        setDocuments(docsResponse.data || [])
      }

      if (verificationsResponse.success) {
        setVerifications(verificationsResponse.data || [])
      }
    } catch (error) {
      console.error('Error fetching data:', error)
      setError('Failed to load dashboard data')
      setDocuments([])
      setVerifications([])
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
          <h1>Customer Dashboard</h1>

          {error && <div className="error-message">{error}</div>}

          <div className="stats-grid">
            <div className="stat-card">
              <div className="stat-label">Total Documents</div>
              <div className="stat-value">{documents.length}</div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Pending Verifications</div>
              <div className="stat-value">
                {verifications.filter(v => v.status === 'pending').length}
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Approved</div>
              <div className="stat-value">
                {verifications.filter(v => v.status === 'approved').length}
              </div>
            </div>
            <div className="stat-card">
              <div className="stat-label">Rejected</div>
              <div className="stat-value">
                {verifications.filter(v => v.status === 'rejected').length}
              </div>
            </div>
          </div>

          <div className="card">
            <h2>Recent Verifications</h2>
            {loading ? (
              <p>Loading...</p>
            ) : verifications.length === 0 ? (
              <p>No verifications yet. Upload a document to get started.</p>
            ) : (
              <table className="table">
                <thead>
                  <tr>
                    <th>Document</th>
                    <th>Risk Level</th>
                    <th>Status</th>
                    <th>Date</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {verifications.map((verification) => {
                    const doc = documents.find(d => d._id === verification.document_id)
                    return (
                      <tr key={verification._id}>
                        <td>{doc?.filename || 'Unknown'}</td>
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
                            View Details
                          </button>
                        </td>
                      </tr>
                    )
                  })}
                </tbody>
              </table>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default CustomerDashboard