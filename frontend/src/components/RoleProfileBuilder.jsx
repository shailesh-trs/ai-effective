import { useState, useEffect, useCallback } from "react";

const API = "/api";

const DOMAIN_COLORS = {
  software_engineering:   "bg-blue-100 text-blue-700 border-blue-200",
  data_science:           "bg-violet-100 text-violet-700 border-violet-200",
  product_management:     "bg-emerald-100 text-emerald-700 border-emerald-200",
  marketing:              "bg-orange-100 text-orange-700 border-orange-200",
  finance:                "bg-yellow-100 text-yellow-700 border-yellow-200",
  hr_people:              "bg-pink-100 text-pink-700 border-pink-200",
  legal_compliance:       "bg-red-100 text-red-700 border-red-200",
  design_ux:              "bg-indigo-100 text-indigo-700 border-indigo-200",
  devops_infrastructure:  "bg-cyan-100 text-cyan-700 border-cyan-200",
  operations:             "bg-teal-100 text-teal-700 border-teal-200",
};

function domainBadge(domain) {
  const cls = DOMAIN_COLORS[domain] ?? "bg-slate-100 text-slate-600 border-slate-200";
  return (
    <span className={`text-xs font-medium px-2 py-0.5 rounded-full border ${cls}`}>
      {domain.replace(/_/g, " ")}
    </span>
  );
}

export default function RoleProfileBuilder({ onSelectProfile }) {
  const [profiles, setProfiles] = useState([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchProfiles = useCallback(async () => {
    try {
      const res = await fetch(`${API}/profiles`);
      setProfiles(await res.json());
    } catch {
      // server not yet ready
    }
  }, []);

  useEffect(() => { fetchProfiles(); }, [fetchProfiles]);

  async function handleBuild() {
    if (!title.trim() || !description.trim()) {
      setError("Both a title and job description are required.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`${API}/profiles`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, job_description: description }),
      });
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.detail ?? "Build failed");
      }
      await fetchProfiles();
      setTitle("");
      setDescription("");
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleDelete(id, e) {
    e.stopPropagation();
    await fetch(`${API}/profiles/${id}`, { method: "DELETE" });
    fetchProfiles();
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
      {/* ── Builder form ───────────────────────────────────────────── */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-4">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">Build a Role Profile</h2>
          <p className="text-sm text-slate-500 mt-1">
            Paste any job description. The profile captures a semantic fingerprint
            of the role using a local embedding model — no cloud API required.
          </p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 text-sm px-4 py-2.5 rounded-lg">
            {error}
          </div>
        )}

        <input
          type="text"
          placeholder="Job title — e.g. Senior Software Engineer"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <textarea
          placeholder="Paste the full job description here…"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={12}
          className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm font-mono focus:outline-none focus:ring-2 focus:ring-blue-500 resize-y"
        />

        <button
          onClick={handleBuild}
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 active:bg-blue-800 disabled:opacity-50 text-white font-semibold py-2.5 px-4 rounded-lg transition-colors"
        >
          {loading ? "Building profile…" : "Build Profile"}
        </button>
      </div>

      {/* ── Profile list ───────────────────────────────────────────── */}
      <div className="space-y-4">
        <h2 className="text-lg font-semibold text-slate-900">
          Saved Profiles
          <span className="ml-2 text-slate-400 font-normal text-base">({profiles.length})</span>
        </h2>

        {profiles.length === 0 ? (
          <div className="bg-white rounded-2xl border border-dashed border-slate-300 p-10 text-center text-slate-400 text-sm">
            No profiles yet. Create one from a job description.
          </div>
        ) : (
          <div className="space-y-3 max-h-[70vh] overflow-y-auto pr-1">
            {profiles.map((p) => (
              <div
                key={p.id}
                className="bg-white rounded-2xl border border-slate-200 shadow-sm p-4 hover:border-blue-300 transition-colors"
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <p className="font-semibold text-slate-900 truncate">{p.title}</p>
                    <p className="text-xs text-slate-400 mt-0.5">
                      {p.id.slice(0, 8)}… · {p.created_at.slice(0, 10)}
                    </p>
                  </div>
                  {domainBadge(p.domain)}
                </div>

                <div className="mt-3 flex flex-wrap gap-1.5">
                  {p.keywords.slice(0, 10).map((kw) => (
                    <span
                      key={kw}
                      className="text-xs bg-slate-50 text-slate-600 border border-slate-200 px-2 py-0.5 rounded-md"
                    >
                      {kw}
                    </span>
                  ))}
                </div>

                <div className="mt-4 flex gap-2">
                  <button
                    onClick={() => onSelectProfile(p)}
                    className="flex-1 text-sm bg-blue-50 hover:bg-blue-100 text-blue-700 font-medium py-1.5 px-3 rounded-lg transition-colors"
                  >
                    Score queries →
                  </button>
                  <button
                    onClick={(e) => handleDelete(p.id, e)}
                    className="text-sm text-slate-400 hover:text-red-600 py-1.5 px-3 rounded-lg hover:bg-red-50 transition-colors"
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
