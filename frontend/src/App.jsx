import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import AuthProvider from './context/AuthProvider'
import Login from './pages/Login'
import CustomerDashboard from './pages/CustomerDashboard'
import OfficerDashboard from './pages/OfficerDashboard'
import AdminDashboard from './pages/AdminDashboard'
import DocumentUpload from './pages/DocumentUpload'
import VerificationDetails from './pages/VerificationDetails'
import ProtectedRoute from './components/ProtectedRoute'

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/customer" element={
            <ProtectedRoute role="customer">
              <CustomerDashboard />
            </ProtectedRoute>
          } />
          <Route path="/officer" element={
            <ProtectedRoute role="officer">
              <OfficerDashboard />
            </ProtectedRoute>
          } />
          <Route path="/admin" element={
            <ProtectedRoute role="admin">
              <AdminDashboard />
            </ProtectedRoute>
          } />
          <Route path="/upload" element={
            <ProtectedRoute role="customer">
              <DocumentUpload />
            </ProtectedRoute>
          } />
          <Route path="/verification/:id" element={
            <ProtectedRoute>
              <VerificationDetails />
            </ProtectedRoute>
          } />
          <Route path="/" element={<Navigate to="/login" />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App