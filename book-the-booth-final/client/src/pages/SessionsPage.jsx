import { useState } from "react";
import { Link } from "react-router-dom";
import { useFetch } from "../hooks/useFetch";
import { useAuth } from "../hooks/useAuth";
import { api } from "../api/client";
import { StatusBlock } from "../components/StatusBlock";

export function SessionsPage() {
  const { token, user } = useAuth();
  const [page, setPage] = useState(1);
  const [genre, setGenre] = useState("");

  const path = `/sessions?page=${page}&per_page=6${genre ? `&genre=${genre}` : ""}`;
  const { data, status, error, refetch } = useFetch(path, [page, genre]);

  const [form, setForm] = useState({
    room_name: "",
    genre_focus: "",
    hourly_rate: "",
    date_available: "",
  });
  const [createError, setCreateError] = useState(null);

  async function handleCreate(e) {
    e.preventDefault();
    setCreateError(null);
    try {
      await api.post("/sessions", form, token);
      setForm({ room_name: "", genre_focus: "", hourly_rate: "", date_available: "" });
      refetch();
    } catch (err) {
      setCreateError(err.message);
    }
  }

  return (
    <div className="page">
      <h1>Browse Sessions</h1>

      <div className="filter-row">
        <input
          placeholder="Filter by genre (e.g. amapiano)"
          value={genre}
          onChange={(e) => {
            setGenre(e.target.value);
            setPage(1);
          }}
        />
      </div>

      <StatusBlock status={status} error={error}>
        <div className="card-grid">
          {data?.items?.length ? (
            data.items.map((s) => (
              <Link to={`/sessions/${s.id}`} key={s.id} className="card">
                <h3>{s.room_name}</h3>
                <p>{s.genre_focus || "Any genre"}</p>
                <p>KES {s.hourly_rate}/hr</p>
                <p>{s.date_available}</p>
                <span className={`badge ${s.status}`}>{s.status}</span>
              </Link>
            ))
          ) : (
            <p>No sessions found.</p>
          )}
        </div>

        {data && (
          <div className="pagination">
            <button disabled={page <= 1} onClick={() => setPage((p) => p - 1)}>
              Prev
            </button>
            <span>
              Page {data.page} of {data.total_pages || 1}
            </span>
            <button disabled={page >= data.total_pages} onClick={() => setPage((p) => p + 1)}>
              Next
            </button>
          </div>
        )}
      </StatusBlock>

      {user?.role === "studio_owner" && (
        <div className="create-panel">
          <h2>Post a new session</h2>
          <form onSubmit={handleCreate}>
            <input
              placeholder="Room name"
              value={form.room_name}
              onChange={(e) => setForm({ ...form, room_name: e.target.value })}
              required
            />
            <input
              placeholder="Genre focus"
              value={form.genre_focus}
              onChange={(e) => setForm({ ...form, genre_focus: e.target.value })}
            />
            <input
              placeholder="Hourly rate"
              type="number"
              value={form.hourly_rate}
              onChange={(e) => setForm({ ...form, hourly_rate: e.target.value })}
              required
            />
            <input
              placeholder="Date available"
              type="date"
              value={form.date_available}
              onChange={(e) => setForm({ ...form, date_available: e.target.value })}
              required
            />
            {createError && <p className="status-msg error">{createError}</p>}
            <button type="submit">Post session</button>
          </form>
        </div>
      )}
    </div>
  );
}