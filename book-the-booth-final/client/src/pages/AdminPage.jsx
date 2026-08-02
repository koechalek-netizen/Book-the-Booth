import { useFetch } from "../hooks/useFetch";
import { StatusBlock } from "../components/StatusBlock";

export function AdminPage() {
  const users = useFetch("/admin/users?page=1&per_page=20");
  const revenue = useFetch("/stats/revenue-by-owner");
  const counts = useFetch("/sessions/stats/booking-counts");

  return (
    <div className="page">
      <h1>Admin Panel</h1>

      <section>
        <h2>Users</h2>
        <StatusBlock status={users.status} error={users.error}>
          <table>
            <thead>
              <tr>
                <th>Username</th>
                <th>Email</th>
                <th>Role</th>
              </tr>
            </thead>
            <tbody>
              {users.data?.items?.map((u) => (
                <tr key={u.id}>
                  <td>{u.username}</td>
                  <td>{u.email}</td>
                  <td>{u.role}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </StatusBlock>
      </section>

      <section>
        <h2>Revenue by Studio Owner</h2>
        <StatusBlock status={revenue.status} error={revenue.error}>
          <table>
            <thead>
              <tr>
                <th>Studio Owner</th>
                <th>Revenue</th>
              </tr>
            </thead>
            <tbody>
              {revenue.data?.map((r, i) => (
                <tr key={i}>
                  <td>{r.studio_owner}</td>
                  <td>KES {r.revenue}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </StatusBlock>
      </section>

      <section>
        <h2>Bookings per Session</h2>
        <StatusBlock status={counts.status} error={counts.error}>
          <table>
            <thead>
              <tr>
                <th>Room</th>
                <th>Genre</th>
                <th># Bookings</th>
              </tr>
            </thead>
            <tbody>
              {counts.data?.map((c) => (
                <tr key={c.session_id}>
                  <td>{c.room_name}</td>
                  <td>{c.genre_focus}</td>
                  <td>{c.booking_count}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </StatusBlock>
      </section>
    </div>
  );
}