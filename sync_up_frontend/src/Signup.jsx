import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";

export default function Signup() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: ""
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSignup = (e) => {
    e.preventDefault();
    console.log("Signup submitted:", formData);

    // Here you would normally validate and send data to backend
    // For now, redirect to login page after signup
    navigate("/login");
  };

  const handleGoToLogin = () => {
    navigate("/login");
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h1 className="login-title">Create an Account</h1>

        <form className="login-inputs" onSubmit={handleSignup}>
          <input
            type="text"
            name="username"
            placeholder="Username"
            value={formData.username}
            onChange={handleChange}
            required
          />
          <input
            type="email"
            name="email"
            placeholder="Email"
            value={formData.email}
            onChange={handleChange}
            required
          />
          <input
            type="password"
            name="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleChange}
            required
          />
          <input
            type="password"
            name="confirmPassword"
            placeholder="Confirm Password"
            value={formData.confirmPassword}
            onChange={handleChange}
            required
          />
          <button type="submit" className="login-btn">Sign Up</button>
        </form>

        <div className="login-options">
          <button className="option-btn" onClick={handleGoToLogin}>
            Already have an account? Login
          </button>
        </div>
      </div>
    </div>
  );
}
