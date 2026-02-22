import React, { useReducer, useEffect } from 'react'
import { AuthContext } from './AuthContext'

const initialState = {
  user: null,
  token: null,
  loading: true
}

const authReducer = (state, action) => {
  switch (action.type) {
    case 'INIT':
      return {
        ...state,
        user: action.user,
        token: action.token,
        loading: false
      }
    case 'LOGIN':
      return {
        ...state,
        user: action.user,
        token: action.token
      }
    case 'LOGOUT':
      return {
        ...state,
        user: null,
        token: null
      }
    default:
      return state
  }
}

const AuthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState)

  useEffect(() => {
    const storedToken = localStorage.getItem('token')
    const storedUser = localStorage.getItem('user')

    dispatch({
      type: 'INIT',
      user: storedUser ? JSON.parse(storedUser) : null,
      token: storedToken
    })
  }, [])

  const login = (userData, authToken) => {
    dispatch({ type: 'LOGIN', user: userData, token: authToken })
    localStorage.setItem('token', authToken)
    localStorage.setItem('user', JSON.stringify(userData))
  }

  const logout = () => {
    dispatch({ type: 'LOGOUT' })
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  const value = {
    user: state.user,
    token: state.token,
    login,
    logout,
    loading: state.loading
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export default AuthProvider