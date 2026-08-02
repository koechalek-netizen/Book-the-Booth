import { useState } from "react";
import { useFetch } from "../hooks/useFetch";
import { useAuth } from "../hooks/useAuth";
import { api } from "../api/client";
import { StatusBlock } from "../components/StatusBlock";

export function BookingsPage() {
  const { token } = useAuth();
  const [page, setPage] = useState(1);
  const { data, status, error, refetch } = useFetch(`/bookings?page=${page}&per_page=6`, [page]);
  const [actionError, setActionError] = useState(null);

  async function updateStatus(id, newStatus) {
    setActionError(null);
    try {
      await api.patch(`/bookings/${id}`, { status: newStatus }, token);
      refetch();
    } catch (err) {
      setActionError(err.message);
    }
  }

  return (
    <div className="page">
      <h1>My Bookings</h1>
      {actionError && <p className="status-msg error">{actionError}</p>}
      <StatusBlock status={status} error={error}>
        <div className="card-grid">
          {data?.items?.length ? (
            data.items.map((b) => (
              <div className="card" key={b.id}>
                <p>Session #{b.session_id}</p>
                <p>{b.session_date}</p>
                <p>
                  {b.hours_booked} hrs @ KES {b.rate_agreed}
                </p>
                <span className={`badge ${b.status}`}>{b.status}</span>
                {b.status === "pending" && (
                  <div className="row-actions">
                    <button onClick={() => updateStatus(b.id, "confirmed")}>Confirm</button>
                    <button onClick={() => updateStatus(b.id, "cancelled")}>Cancel</button>
                  </div>
                )}
              </div>
            ))
          ) : (
            <p>No bookings yet.</p>
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
    </div>
  );
}