import React from 'react'

const RiskScoreBadge = ({ riskScore, riskLevel }) => {
  const getRiskClass = () => {
    if (riskLevel === 'low') return 'risk-low'
    if (riskLevel === 'medium') return 'risk-medium'
    return 'risk-high'
  }

  return (
    <span className={`risk-badge ${getRiskClass()}`}>
      {riskLevel.toUpperCase()} ({riskScore})
    </span>
  )
}

export default RiskScoreBadge