"""Test scenario-forge list and export commands."""

import json
from click.testing import CliRunner

from scenario_forge.cli import cli
from scenario_forge.core import Scenario


def test_list_command_empty(isolated_db):
    """Test list command with no scenarios."""
    runner = CliRunner()

    # Use real empty database
    result = runner.invoke(cli, ["list"])

    assert result.exit_code == 0
    assert "No scenarios found" in result.output


def test_list_command_with_scenarios(isolated_db):
    """Test list command with scenarios."""
    runner = CliRunner()

    # Create some scenarios using real database
    from scenario_forge.datastore import ScenarioStore

    store = ScenarioStore(isolated_db)

    scenario1 = Scenario("Prompt 1", "target1", ["criteria1"])
    scenario2 = Scenario("Prompt 2", "target2", ["criteria2", "criteria3"])

    store.save_scenario(scenario1)
    store.save_scenario(scenario2)

    result = runner.invoke(cli, ["list"])

    assert result.exit_code == 0
    assert "Found 2 scenarios" in result.output
    assert "target1" in result.output
    assert "target2" in result.output


def test_export_command_no_rated(isolated_db):
    """Test export command when no rated scenarios exist."""
    runner = CliRunner()

    # Use real ScenarioStore with isolated database instead of mocking
    result = runner.invoke(cli, ["export"])

    assert result.exit_code == 0
    assert "No scenarios found with rating >= 0" in result.output


def test_export_command_with_filter(isolated_db):
    """Test export command with minimum rating filter."""
    runner = CliRunner()

    # Create some rated scenarios using real database
    from scenario_forge.datastore import ScenarioStore

    store = ScenarioStore(isolated_db)

    # Add scenarios and rate them
    scenario1 = Scenario("Test prompt 1", "target1", ["criteria1"])
    scenario2 = Scenario("Test prompt 2", "target2", ["criteria2", "criteria3"])
    scenario3 = Scenario("Test prompt 3", "target3", ["criteria4"])

    id1 = store.save_scenario(scenario1, backend="ollama", model="llama3.2")
    id2 = store.save_scenario(scenario2, backend="ollama", model="llama3.2")
    id3 = store.save_scenario(scenario3, backend="ollama", model="llama3.2")

    store.save_rating(id1, 3)
    store.save_rating(id2, 2)
    store.save_rating(id3, 1)  # This one should be filtered out

    result = runner.invoke(cli, ["export", "--min-rating", "2"])

    assert result.exit_code == 0

    # Parse JSON output
    exported = json.loads(result.output)
    assert len(exported) == 2
    assert exported[0]["rating"] == 3
    assert exported[1]["rating"] == 2
