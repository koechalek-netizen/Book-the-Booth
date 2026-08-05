import { useParams, useNavigate } from "react-router-dom";
import { useState } from "react";
import { useFetch } from "../hooks/useFetch";
import { useAuth } from "../hooks/useAuth";
import { api } from "../api/client";
import { StatusBlock } from "../components/StatusBlock";

export function SessionDetailPage() {
  const { id } = useParams();
  const { token, user } = useAuth();
  const navigate = useNavigate();
  const { data: session, status, error } = useFetch(`/sessions/${id}`, [id]);

  const isOwner = session && user?.role === "studio_owner" && String(session.studio_owner_id) === String(user.id);

  const bookingsResult = useFetch(isOwner ? `/sessions/${id}/bookings` : null, [id, isOwner]);

  const [hours, setHours] = useState(1);
  const [bookError, setBookError] = useState(null);
  const [booking, setBooking] = useState(false);

  async function handleBook(e) {
    e.preventDefault();
    setBookError(null);
    setBooking(true);
    try {
      await api.post(
        "/bookings",
        {
          session_id: Number(id),
          rate_agreed: session.hourly_rate,
          session_date: session.date_available,
          hours_booked: Number(hours),
        },
        token
      );
      navigate("/bookings");
    } catch (err) {
      setBookError(err.message);
    } finally {
      setBooking(false);
    }
  }

  return (
    <div className="page">
      <StatusBlock status={status} error={error}>
        {session && (
          <div className="detail-card">
            <h1>{session.room_name}</h1>
            <p>{session.genre_focus || "Any genre"}</p>
            <p>KES {session.hourly_rate}/hr</p>
            <p>Available: {session.date_available}</p>
            <span className={`badge ${session.status}`}>{session.status}</span>

            {user?.role === "artist" && session.status === "open" && (
              <form onSubmit={handleBook} className="book-form">
                <label>
                  Hours
                  <input
                    type="number"
                    min="1"
                    value={hours}
                    onChange={(e) => setHours(e.target.value)}
                    required
                  />
                </label>
                {bookError && <p className="status-msg error">{bookError}</p>}
                <button type="submit" disabled={booking}>
                  {booking ? "Booking…" : "Reserve this session"}
                </button>
              </form>
            )}

            {isOwner && (
              <div className="owner-bookings">
                <h2>Reservations on this session</h2>
                <StatusBlock status={bookingsResult.status} error={bookingsResult.error}>
                  {bookingsResult.data?.length ? (
                    <div className="card-grid">
                      {bookingsResult.data.map((b) => (
                        <div className="card" key={b.id}>
                          <p>Artist #{b.artist_id}</p>
                          <p>{b.session_date}</p>
                          <p>
                            {b.hours_booked} hrs @ KES {b.rate_agreed}
                          </p>
                          <span className={`badge ${b.status}`}>{b.status}</span>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p>No one has reserved this session yet.</p>
                  )}
                </StatusBlock>
              </div>
            )}
          </div>
        )}
      </StatusBlock>
    </div>
  );
}