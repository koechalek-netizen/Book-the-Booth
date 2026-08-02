export function StatusBlock({ status, error, children }) {
  if (status === "loading") return <p className="status-msg">Loading…</p>;
  if (status === "error") return <p className="status-msg error">Error: {error}</p>;
  return children;
}