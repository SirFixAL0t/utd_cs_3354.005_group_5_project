import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";

export default function Login() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ username: "", password: "" });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleLogin = (e) => {
    e.preventDefault();
    console.log("Login submitted:", formData);
    navigate("/dashboard"); // redirect after login
  };

  const handleCreateAccount = () => {
    navigate("/signup"); // redirect to Signup page
  };

  const handleForgotPassword = () => {
    navigate("/forgot-password"); // optional page
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h1 className="login-title">Welcome Back</h1>

        <form className="login-inputs" onSubmit={handleLogin}>
          <input
            type="text"
            name="username"
            placeholder="Username"
            value={formData.username}
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
          <button type="submit" className="login-btn">Login</button>
        </form>

        <div className="login-options">
          <button className="option-btn" onClick={handleCreateAccount}>
            Create Account
          </button>
          <button className="option-btn" onClick={handleForgotPassword}>
            Forgot Password?
          </button>
        </div>
      </div>
    </div>
  );
}
