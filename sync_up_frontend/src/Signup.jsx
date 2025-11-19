import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";

export default function Signup() {
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
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

  async function registerUser({ name, email, password, timezone }) {
    const base = import.meta.env.VITE_API_BASE || "http://localhost:8000";
    
    const res = await fetch(`${base}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, password, timezone }),
    })

    const data = await res.json();
    if (!res.ok) {
      const errorMessage = data.detail
      throw new Error(errorMessage);
    }
    return data;
  }
  const handleSignup = async (e) => {
    e.preventDefault();
    setError("");
    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match!");
      return;
    }
    setLoading(true);
    try {
      const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
      await registerUser({
        name: formData.username,
        email: formData.email,
        password: formData.password,
        timezone
      });
      navigate("/login");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false)
    }
  };

  const handleGoToLogin = () => {
    navigate("/login");
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h1 className="login-title">Create an Account</h1>

        {error && <div className="error-message">{error}</div>}
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
