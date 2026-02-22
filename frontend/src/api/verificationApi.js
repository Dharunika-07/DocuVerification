import axiosInstance from './axiosInstance'

export const verificationApi = {
  verifyDocument: async (documentId) => {
    const response = await axiosInstance.post(`/verifications/verify/${documentId}`)
    return response.data
  },

  getMyVerifications: async () => {
    const response = await axiosInstance.get('/verifications/my-verifications')
    return response.data
  },

  getVerification: async (verificationId) => {
    const response = await axiosInstance.get(`/verifications/${verificationId}`)
    return response.data
  },

  getPendingVerifications: async () => {
    const response = await axiosInstance.get('/verifications/pending')
    return response.data
  },

  reviewVerification: async (verificationId, decision, notes) => {
    const response = await axiosInstance.post(`/verifications/${verificationId}/review`, {
      decision,
      notes
    })
    return response.data
  },

  getAllVerifications: async () => {
    const response = await axiosInstance.get('/admin/verifications')
    return response.data
  },

  getStatistics: async () => {
    const response = await axiosInstance.get('/admin/statistics')
    return response.data
  }
}