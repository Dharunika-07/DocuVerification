import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'

const Navbar = () => {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const getInitials = (name) => {
    return name ? name.substring(0, 2).toUpperCase() : 'U'
  }

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <div className="navbar-logo">V</div>
          <span>VerifyChain</span>
        </div>
        <div className="navbar-menu">
          <div className="navbar-user">
            <div className="navbar-user-avatar">
              {getInitials(user?.username)}
            </div>
            <div className="navbar-user-info">
              <div className="navbar-user-name">{user?.username}</div>
              <div className="navbar-user-role">{user?.role}</div>
            </div>
          </div>
          <button className="btn btn-secondary btn-sm" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </div>
    </nav>
  )
}

export default Navbar