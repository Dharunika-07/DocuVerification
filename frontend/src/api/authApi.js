import axiosInstance from './axiosInstance'

export const authApi = {
  login: async (email, password) => {
    const response = await axiosInstance.post('/auth/login', { email, password })
    return response.data
  },

  register: async (username, email, password, role) => {
    const response = await axiosInstance.post('/auth/register', {
      username,
      email,
      password,
      role
    })
    return response.data
  }
}