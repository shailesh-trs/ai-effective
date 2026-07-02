import { useState } from "react";
import RoleProfileBuilder from "./components/RoleProfileBuilder";
import TASScorer from "./components/TASScorer";

export default function App() {
  const [activeTab, setActiveTab] = useState("profiles");
  const [selectedProfile, setSelectedProfile] = useState(null);

  function handleSelectProfile(profile) {
    setSelectedProfile(profile);
    setActiveTab("score");
  }

  return (
    <div className="min-h-screen bg-slate-50">
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div>
            <span className="text-xl font-bold text-slate-900 tracking-tight">
              AI Effective
            </span>
            <span className="ml-3 text-sm text-slate-400 font-medium">
              Task Alignment Score
            </span>
          </div>
          <nav className="flex gap-1 bg-slate-100 p-1 rounded-lg">
            {[
              { key: "profiles", label: "Role Profiles" },
              { key: "score", label: "Score Query" },
            ].map(({ key, label }) => (
              <button
                key={key}
                onClick={() => setActiveTab(key)}
                className={`px-4 py-1.5 rounded-md text-sm font-medium transition-all ${
                  activeTab === key
                    ? "bg-white text-slate-900 shadow-sm"
                    : "text-slate-500 hover:text-slate-700"
                }`}
              >
                {label}
              </button>
            ))}
          </nav>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-10">
        {activeTab === "profiles" ? (
          <RoleProfileBuilder onSelectProfile={handleSelectProfile} />
        ) : (
          <TASScorer initialProfile={selectedProfile} />
        )}
      </main>

      <footer className="text-center text-xs text-slate-400 py-8">
        ai-effective v0.1.0 · all inference runs locally, no API calls
      </footer>
    </div>
  );
}
