"""Profile persistence: read/write role profiles as JSON on disk."""

from __future__ import annotations

import json
from pathlib import Path

_DEFAULT_STORE_DIR = Path.home() / ".ai-effective" / "profiles"


class ProfileStore:
    def __init__(self, store_dir: Path | None = None) -> None:
        self._dir = Path(store_dir) if store_dir else _DEFAULT_STORE_DIR
        self._dir.mkdir(parents=True, exist_ok=True)

    def save(self, profile: "RoleProfile") -> None:  # noqa: F821
        path = self._dir / f"{profile.id}.json"
        path.write_text(
            json.dumps(profile.to_dict(), indent=2), encoding="utf-8"
        )

    def load(self, profile_id: str) -> "RoleProfile | None":  # noqa: F821
        from ai_effective.role_profile.builder import RoleProfile

        path = self._dir / f"{profile_id}.json"
        if not path.exists():
            return None
        return RoleProfile.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def list_all(self) -> "list[RoleProfile]":  # noqa: F821
        from ai_effective.role_profile.builder import RoleProfile

        profiles = []
        for p in self._dir.glob("*.json"):
            try:
                profiles.append(
                    RoleProfile.from_dict(json.loads(p.read_text(encoding="utf-8")))
                )
            except Exception:
                pass
        return sorted(profiles, key=lambda x: x.created_at, reverse=True)

    def delete(self, profile_id: str) -> bool:
        path = self._dir / f"{profile_id}.json"
        if path.exists():
            path.unlink()
            return True
        return False
