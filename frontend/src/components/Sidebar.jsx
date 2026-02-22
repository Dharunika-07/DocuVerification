import React from 'react'
import { useNavigate, useLocation } from 'react-router-dom'

const Sidebar = ({ items }) => {
  const navigate = useNavigate()
  const location = useLocation()

  return (
    <div className="sidebar">
      {items.map((item, index) => (
        <div
          key={index}
          className={`sidebar-item ${location.pathname === item.path ? 'active' : ''}`}
          onClick={() => navigate(item.path)}
        >
          {item.label}
        </div>
      ))}
    </div>
  )
}

export default Sidebar