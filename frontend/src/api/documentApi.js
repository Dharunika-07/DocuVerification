import axiosInstance from './axiosInstance'

export const documentApi = {
  uploadDocument: async (file, documentType) => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('document_type', documentType)

    const response = await axiosInstance.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    return response.data
  },

  getMyDocuments: async () => {
    const response = await axiosInstance.get('/documents/my-documents')
    return response.data
  },

  getDocument: async (documentId) => {
    const response = await axiosInstance.get(`/documents/${documentId}`)
    return response.data
  },

  getAllDocuments: async () => {
    const response = await axiosInstance.get('/admin/documents')
    return response.data
  }
}