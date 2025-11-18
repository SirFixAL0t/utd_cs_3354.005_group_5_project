import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { Routes, Route, Link } from 'react-router-dom'
import Dashboard from './Dashboard.jsx'

function Home() {

  return (
    <>
      <div style={{ marginTop: 16 }}>
        <Link to="/dashboard">Dashboard</Link>
      </div>
    </>
  )
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/dashboard" element={<Dashboard />} />
    </Routes>
  )
}

export default App
