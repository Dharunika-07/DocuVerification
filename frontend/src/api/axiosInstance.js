import axios from 'axios'

const axiosInstance = axios.create({
  // Add /api prefix!
  baseURL: 'https://verifychain-api.onrender.com/api',  // ← /api added
  headers: {
    'Content-Type': 'application/json',
  },
})

axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

export default axiosInstance