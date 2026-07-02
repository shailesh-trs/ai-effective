import { useState, useEffect } from "react";
import ScoreDisplay from "./ScoreDisplay";

const API = "/api";

const EXAMPLE_QUERIES = [
  "Help me implement a binary search function in Python",
  "Review this SQL query for performance issues",
  "Write unit tests for the authentication module",
  "Debug this React component that isn't re-rendering",
  "Design a microservices architecture for our e-commerce platform",
];

export default function TASScorer({ initialProfile }) {
  const [profiles, setProfiles] = useState([]);
  const [selectedProfileId, setSelectedProfileId] = useState(initialProfile?.id ?? "");
  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch(`${API}/profiles`)
      .then((r) => r.json())
      .then(setProfiles)
      .catch(() => {});
  }, []);

  useEffect(() => {
    if (initialProfile) setSelectedProfileId(initialProfile.id);
  }, [initialProfile]);

  async function handleScore() {
    if (!selectedProfileId) {
      setError("Select a role profile first.");
      return;
    }
    if (!query.trim()) {
      setError("Enter a query to score.");
      return;
    }
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await fetch(`${API}/score`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ profile_id: selectedProfileId, query }),
      });
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.detail ?? "Scoring failed");
      }
      setResult(await res.json());
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) handleScore();
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
      {/* ── Input panel ────────────────────────────────────────────── */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-4">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">Score a Query</h2>
          <p className="text-sm text-slate-500 mt-1">
            Paste the exact prompt a user sent to an AI assistant. TAS measures
            how well it aligns with their role — not whether the output was good.
          </p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 text-sm px-4 py-2.5 rounded-lg">
            {error}
          </div>
        )}

        {/* Profile selector */}
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">
            Role Profile
          </label>
          <select
            value={selectedProfileId}
            onChange={(e) => setSelectedProfileId(e.target.value)}
            className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
          >
            <option value="">Select a profile…</option>
            {profiles.map((p) => (
              <option key={p.id} value={p.id}>
                {p.title} — {p.domain.replace(/_/g, " ")}
              </option>
            ))}
          </select>
          {profiles.length === 0 && (
            <p className="text-xs text-slate-400 mt-1">
              No profiles yet — go to Role Profiles tab to create one.
            </p>
          )}
        </div>

        {/* Query textarea */}
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-1">
            Query / Prompt
            <span className="ml-2 font-normal text-slate-400">(Ctrl+Enter to score)</span>
          </label>
          <textarea
            placeholder="Paste an AI prompt here…"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={10}
            className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-blue-500 resize-y"
          />
        </div>

        {/* Example queries */}
        <div>
          <p className="text-xs text-slate-400 font-medium mb-1.5">Try an example:</p>
          <div className="flex flex-wrap gap-1.5">
            {EXAMPLE_QUERIES.map((q) => (
              <button
                key={q}
                onClick={() => setQuery(q)}
                className="text-xs bg-slate-50 hover:bg-blue-50 text-slate-600 hover:text-blue-700 border border-slate-200 hover:border-blue-200 px-2.5 py-1 rounded-lg transition-colors"
              >
                {q.slice(0, 40)}…
              </button>
            ))}
          </div>
        </div>

        <button
          onClick={handleScore}
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 active:bg-blue-800 disabled:opacity-50 text-white font-semibold py-2.5 px-4 rounded-lg transition-colors"
        >
          {loading ? "Scoring…" : "Compute TAS Score"}
        </button>
      </div>

      {/* ── Result panel ───────────────────────────────────────────── */}
      <div>
        {result ? (
          <ScoreDisplay result={result} />
        ) : (
          <div className="bg-white rounded-2xl border border-dashed border-slate-300 p-10 text-center text-slate-400 text-sm h-full flex flex-col items-center justify-center gap-3">
            <div className="text-5xl">📊</div>
            <p>Score a query to see the TAS breakdown here.</p>
            <p className="text-xs text-slate-300">
              Semantic · Keyword · Task-type
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
