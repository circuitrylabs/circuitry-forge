"""Integration tests for the complete scenario-forge workflow."""

import json
import tempfile
from pathlib import Path

from click.testing import CliRunner

from scenario_forge.cli import cli
from scenario_forge.datastore import ScenarioStore


def test_complete_workflow(mock_ollama_backend, monkeypatch):
    """Test the full workflow: generate → save → review → export.

    This is the core self-improvement loop that makes scenario-forge special.
    """
    # Use isolated database
    with tempfile.TemporaryDirectory() as tmpdir:
        test_home = Path(tmpdir)
        monkeypatch.setenv("HOME", str(test_home))
        (test_home / ".scenario-forge").mkdir()

        runner = CliRunner()

        # Step 1: Generate and save scenarios
        result = runner.invoke(
            cli, ["generate", "ai_psychosis", "--count", "3", "--save"]
        )
        assert result.exit_code == 0

        # Verify scenarios were saved
        store = ScenarioStore()
        scenarios = store.list_all_scenarios()
        assert len(scenarios) == 3

        # Step 2: List scenarios
        result = runner.invoke(cli, ["list"])
        assert result.exit_code == 0
        assert "Found 3 scenarios" in result.output

        # Step 3: Review and rate scenarios
        # Rate them as: 3 (excellent), 1 (ok), 2 (good)
        result = runner.invoke(cli, ["review"], input="3\n1\n2\n")
        assert result.exit_code == 0
        assert "✓ Rated as 3" in result.output
        assert "✓ Rated as 1" in result.output
        assert "✓ Rated as 2" in result.output

        # Step 4: Export only good scenarios (rating >= 2)
        result = runner.invoke(cli, ["export", "--min-rating", "2"])
        assert result.exit_code == 0

        # Parse exported JSON
        exported = json.loads(result.output)
        assert len(exported) == 2  # Only ratings 3 and 2

        # Verify exported scenarios have correct ratings
        ratings = [s["rating"] for s in exported]
        assert 3 in ratings
        assert 2 in ratings
        assert 1 not in ratings  # Filtered out


def test_workflow_with_pretty_output(mock_ollama_backend, monkeypatch):
    """Test workflow with pretty printing enabled."""
    with tempfile.TemporaryDirectory() as tmpdir:
        test_home = Path(tmpdir)
        monkeypatch.setenv("HOME", str(test_home))
        (test_home / ".scenario-forge").mkdir()

        runner = CliRunner()

        # Generate with pretty output
        result = runner.invoke(cli, ["generate", "harmful_code", "--pretty", "--save"])
        assert result.exit_code == 0
        # Rich library formats with ANSI codes
        assert "prompt" in result.output
        assert "evaluation_target" in result.output
        assert "success_criteria" in result.output
