import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css";
//test
export default function Login() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("")

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

  async function loginUser({ email, password}) {
    const params = new URLSearchParams();
    params.append("username", email);
    params.append("password", password);

    const res = await fetch(`${API_BASE}/auth/token`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: params.toString(),
    });
    //need to check headers for token auth
    const ct = res.headers.get("content-type") || "";
    let body;
    if (ct.includes("application/json")) {
      body = await res.json().catch(() => ({ detail: "Invalid JSON response" }));
    } else {
      body = { detail: await res.text().catch(() => res.statusText || "Unknown error") };
    }

    if (!res.ok) throw body;
    return body; // expected { access_token, token_type }
  }

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    
    try {
        const data = await loginUser({ email: formData.email, password: formData.password});
        const token = data.access_token;
        if(!token) throw {detail: "No access"};
        localStorage.setItem("access_token", token);
        navigate("/dashboard"); // redirect after login
    } catch (err) {
      const msg = err.detail
      setError(msg);
    } finally {
      setLoading(false);
    }

    
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
        {error && <div className="error-message">{error}</div>}
        
        <form className="login-inputs" onSubmit={handleLogin}>
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
          <button type="submit" className="login-btn" disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </button>
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
