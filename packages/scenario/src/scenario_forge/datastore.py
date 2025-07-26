"""Minimal SQLite datastore for scenarios."""

import json
import sqlite3
from pathlib import Path
from typing import Optional, List

from scenario_forge.core import Scenario


class ScenarioStore:
    """Minimal scenario storage."""

    def __init__(self, db_path: Optional[Path] = None):
        """Initialize the datastore."""
        if db_path is None:
            db_dir = Path.home() / ".scenario-forge"
            db_dir.mkdir(exist_ok=True)
            db_path = db_dir / "scenarios.db"

        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        """Create the scenarios and ratings tables."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS scenarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt TEXT NOT NULL,
                    evaluation_target TEXT NOT NULL,
                    success_criteria TEXT NOT NULL,
                    backend TEXT,
                    model TEXT,
                    temperature REAL
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS ratings (
                    id INTEGER PRIMARY KEY,
                    scenario_id INTEGER NOT NULL,
                    rating INTEGER NOT NULL CHECK (rating >= 0 AND rating <= 3),
                    rated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (scenario_id) REFERENCES scenarios(id)
                )
            """)

            conn.commit()

    def save_scenario(
        self,
        scenario: Scenario,
        backend: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
    ) -> int:
        """Save a scenario and return its ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                INSERT INTO scenarios (
                    prompt, evaluation_target, success_criteria,
                    backend, model, temperature
                ) VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    scenario.prompt,
                    scenario.evaluation_target,
                    json.dumps(scenario.success_criteria),
                    backend,
                    model,
                    temperature,
                ),
            )
            if cursor.lastrowid is None:
                raise RuntimeError("Failed to insert scenario into database")
            return cursor.lastrowid

    def get_scenario(self, scenario_id: int) -> Optional[Scenario]:
        """Get a scenario by ID."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM scenarios WHERE id = ?", (scenario_id,)
            ).fetchone()

            if row:
                return Scenario(
                    prompt=row["prompt"],
                    evaluation_target=row["evaluation_target"],
                    success_criteria=json.loads(row["success_criteria"]),
                )
            return None

    def _parse_success_criteria(self, criteria: Optional[str]) -> List[str]:
        """Parse success criteria from old string or new JSON format."""
        if criteria and criteria.startswith("["):
            return json.loads(criteria)
        else:
            return [criteria] if criteria else []

    def list_all_scenarios(self) -> List[Scenario]:
        """List all scenarios."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("SELECT * FROM scenarios ORDER BY id DESC").fetchall()

            return [
                Scenario(
                    prompt=row["prompt"],
                    evaluation_target=row["evaluation_target"],
                    success_criteria=self._parse_success_criteria(
                        row["success_criteria"]
                    ),
                )
                for row in rows
            ]

    def save_rating(self, scenario_id: int, rating: int) -> None:
        """Save a rating for a scenario."""
        if not (0 <= rating <= 3):
            raise ValueError("Rating must be between 0 and 3")

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO ratings (scenario_id, rating) VALUES (?, ?)",
                (scenario_id, rating),
            )
            conn.commit()

    def get_scenarios_for_review(self) -> List[tuple[int, Scenario]]:
        """Get scenarios that haven't been rated yet."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute("""
                SELECT s.* FROM scenarios s
                LEFT JOIN ratings r ON s.id = r.scenario_id
                WHERE r.id IS NULL
                ORDER BY s.id
            """).fetchall()

            return [
                (
                    row["id"],
                    Scenario(
                        prompt=row["prompt"],
                        evaluation_target=row["evaluation_target"],
                        success_criteria=self._parse_success_criteria(
                            row["success_criteria"]
                        ),
                    ),
                )
                for row in rows
            ]

    def get_rated_scenarios(self, min_rating: int = 0) -> List[dict]:
        """Get scenarios with their ratings."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """
                SELECT s.*, r.rating, r.rated_at
                FROM scenarios s
                JOIN ratings r ON s.id = r.scenario_id
                WHERE r.rating >= ?
                ORDER BY r.rating DESC, r.rated_at DESC
            """,
                (min_rating,),
            ).fetchall()

            return [
                {
                    "id": row["id"],
                    "prompt": row["prompt"],
                    "evaluation_target": row["evaluation_target"],
                    "success_criteria": self._parse_success_criteria(
                        row["success_criteria"]
                    ),
                    "rating": row["rating"],
                    "rated_at": row["rated_at"],
                    "backend": row["backend"],
                    "model": row["model"],
                }
                for row in rows
            ]
