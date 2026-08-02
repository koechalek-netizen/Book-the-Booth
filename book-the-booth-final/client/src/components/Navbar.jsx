import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export function Navbar() {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login");
  }

  return (
    <nav className="navbar">
      <Link to="/sessions" className="brand">
        🎙️ Book the Booth
      </Link>
      <div className="nav-links">
        {isAuthenticated ? (
          <>
            <Link to="/sessions">Sessions</Link>
            <Link to="/bookings">My Bookings</Link>
            {user?.role === "admin" && <Link to="/admin">Admin</Link>}
            <span className="nav-user">
              {user?.username} ({user?.role})
            </span>
            <button onClick={handleLogout}>Log out</button>
          </>
        ) : (
          <>
            <Link to="/login">Log in</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}