function ScoreBar({ label, value, colorClass }) {
  return (
    <div>
      <div className="flex justify-between items-center text-sm mb-1.5">
        <span className="text-slate-600">{label}</span>
        <span className="font-semibold text-slate-800">{value.toFixed(1)}</span>
      </div>
      <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
        <div
          className={`h-full rounded-full transition-all duration-700 ${colorClass}`}
          style={{ width: `${Math.min(100, value)}%` }}
        />
      </div>
    </div>
  );
}

const STYLES = {
  high:     { ring: "ring-emerald-400", text: "text-emerald-600", bg: "bg-emerald-50", badge: "bg-emerald-100 text-emerald-700" },
  medium:   { ring: "ring-yellow-400",  text: "text-yellow-600",  bg: "bg-yellow-50",  badge: "bg-yellow-100 text-yellow-700"  },
  low:      { ring: "ring-orange-400",  text: "text-orange-600",  bg: "bg-orange-50",  badge: "bg-orange-100 text-orange-700"  },
  very_low: { ring: "ring-red-400",     text: "text-red-600",     bg: "bg-red-50",     badge: "bg-red-100 text-red-700"        },
};

const LABEL_TEXT = {
  high: "High alignment",
  medium: "Medium alignment",
  low: "Low alignment",
  very_low: "Very low alignment",
};

export default function ScoreDisplay({ result }) {
  const s = STYLES[result.label] ?? STYLES.low;

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-6">
      {/* Big score circle */}
      <div className="flex flex-col items-center">
        <div className={`flex items-center justify-center w-32 h-32 rounded-full ring-4 ${s.ring} ${s.bg}`}>
          <div className="text-center">
            <div className={`text-5xl font-bold leading-none ${s.text}`}>
              {result.score.toFixed(0)}
            </div>
            <div className="text-xs text-slate-400 mt-1 uppercase tracking-widest">/ 100</div>
          </div>
        </div>
        <span className={`mt-3 px-3 py-1 rounded-full text-sm font-medium ${s.badge}`}>
          {LABEL_TEXT[result.label] ?? result.label}
        </span>
        <p className="text-sm text-slate-500 mt-1.5">
          {result.profile_title}
          <span className="mx-1.5 text-slate-300">·</span>
          <span className="text-slate-400">{result.domain.replace(/_/g, " ")}</span>
        </p>
      </div>

      {/* Component bars */}
      <div className="space-y-4">
        <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-widest">
          Score Breakdown
        </h3>
        <ScoreBar label="Semantic alignment (50%)" value={result.semantic_score} colorClass="bg-blue-500" />
        <ScoreBar label="Keyword overlap (30%)"    value={result.keyword_score}  colorClass="bg-violet-500" />
        <ScoreBar label="Task-type match (20%)"    value={result.task_score}     colorClass="bg-emerald-500" />
      </div>

      {/* Matched task type */}
      {result.matched_task_type && (
        <div className="bg-slate-50 rounded-xl p-4">
          <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-1">
            Matched Task Type
          </p>
          <p className="text-sm font-medium text-slate-800">
            {result.matched_task_type.replace(/_/g, " ")}
          </p>
        </div>
      )}

      {/* Query preview */}
      <div className="bg-slate-50 rounded-xl p-4">
        <p className="text-xs font-semibold text-slate-400 uppercase tracking-widest mb-1">
          Query
        </p>
        <p className="text-sm text-slate-700 line-clamp-4 leading-relaxed">
          {result.query}
        </p>
      </div>
    </div>
  );
}
