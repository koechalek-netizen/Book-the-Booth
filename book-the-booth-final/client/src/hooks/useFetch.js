import { useState, useEffect, useCallback } from "react";
import { api } from "../api/client";
import { useAuth } from "./useAuth";

/**
 * Fetches `path` whenever `path` or any value in `deps` changes.
 * Returns { data, status, error, refetch } where status is
 * "loading" | "error" | "success".
 */
export function useFetch(path, deps = []) {
  const { token } = useAuth();
  const [data, setData] = useState(null);
  const [status, setStatus] = useState("loading");
  const [error, setError] = useState(null);

  const refetch = useCallback(() => {
    if (!path) return;
    setStatus("loading");
    setError(null);
    api
      .get(path, token)
      .then((result) => {
        setData(result);
        setStatus("success");
      })
      .catch((err) => {
        setError(err.message);
        setStatus("error");
      });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [path, token, ...deps]);

  useEffect(() => {
    refetch();
  }, [refetch]);

  return { data, status, error, refetch };
}