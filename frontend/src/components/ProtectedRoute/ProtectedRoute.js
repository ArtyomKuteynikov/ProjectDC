import React, { useContext } from 'react'
import { Navigate } from 'react-router-dom';
import { AppContext } from '../../contexts/AppContext'

const ProtectedRouteElement = ({ element: Component, ...props }) => {
  const value = useContext(AppContext);
  return (
    value.isLoggedIn === true 
      ? <Component {...props} userData={value.userData} /> 
      : <Navigate to="/signin" replace />
  )
}

export default ProtectedRouteElement