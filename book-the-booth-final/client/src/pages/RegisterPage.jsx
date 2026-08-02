import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export function RegisterPage() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    role: "artist",
  });
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  function update(field) {
    return (e) => setForm({ ...form, [field]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      await register(form);
      navigate("/sessions");
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="auth-page">
      <h1>Create an account</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Username
          <input value={form.username} onChange={update("username")} required />
        </label>
        <label>
          Email
          <input type="email" value={form.email} onChange={update("email")} required />
        </label>
        <label>
          Password
          <input type="password" value={form.password} onChange={update("password")} required />
        </label>
        <label>
          I am a...
          <select value={form.role} onChange={update("role")}>
            <option value="artist">Artist</option>
            <option value="studio_owner">Studio Owner</option>
          </select>
        </label>
        {error && <p className="status-msg error">{error}</p>}
        <button type="submit" disabled={submitting}>
          {submitting ? "Creating…" : "Create account"}
        </button>
      </form>
      <p>
        Already have an account? <Link to="/login">Log in</Link>
      </p>
    </div>
  );
}