import { School } from 'lucide-react'
import React from 'react'

const LoginComponent = () => {
  return (
    <div className="w-full min-h-screen flex items-center justify-center bg-gradient-to-b from-blue-50 to-blue-100 p-4">
      <div className="w-full max-w-md">
        <div className="flex justify-center mb-6">
          <div className="bg-white p-3 rounded-full shadow-sm">
            <School className="h-10 w-10 text-blue-600" />
          </div>
        </div>
        <h1 className="text-2xl font-bold text-center text-gray-800 mb-2">Matemix</h1>
        <p className="text-center text-gray-600 mb-6">Accede a tu cuenta para continuar</p>
      </div>
    </div>
  )
}

export default LoginComponent