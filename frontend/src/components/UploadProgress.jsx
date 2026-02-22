import React from 'react'

const UploadProgress = ({ progress }) => {
  return (
    <div className="card">
      <div className="form-label">Upload Progress</div>
      <div className="progress-bar">
        <div
          className="progress-fill"
          style={{ width: `${progress}%` }}
        ></div>
      </div>
      <div style={{ marginTop: '10px', textAlign: 'center' }}>
        {progress}%
      </div>
    </div>
  )
}

export default UploadProgress