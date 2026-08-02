import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { Navbar } from "./components/Navbar";
import { ProtectedRoute } from "./components/ProtectedRoute";
import { LoginPage } from "./pages/LoginPage";
import { RegisterPage } from "./pages/RegisterPage";
import { SessionsPage } from "./pages/SessionsPage";
import { SessionDetailPage } from "./pages/SessionDetailPage";
import { BookingsPage } from "./pages/BookingsPage";
import { AdminPage } from "./pages/AdminPage";
import "./App.css";

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Navbar />
        <main>
          <Routes>
            <Route path="/" element={<Navigate to="/sessions" replace />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route
              path="/sessions"
              element={
                <ProtectedRoute>
                  <SessionsPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/sessions/:id"
              element={
                <ProtectedRoute>
                  <SessionDetailPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/bookings"
              element={
                <ProtectedRoute>
                  <BookingsPage />
                </ProtectedRoute>
              }
            />
            <Route
              path="/admin"
              element={
                <ProtectedRoute roles={["admin"]}>
                  <AdminPage />
                </ProtectedRoute>
              }
            />
          </Routes>
        </main>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;