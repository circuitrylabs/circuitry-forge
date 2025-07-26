"""Test scenario-forge review command."""

from click.testing import CliRunner

from scenario_forge.cli import cli
from scenario_forge.datastore import ScenarioStore


def test_review_command_no_scenarios(isolated_db):
    """Test review command when no unrated scenarios exist."""
    runner = CliRunner()

    # Use real empty database
    result = runner.invoke(cli, ["review"])

    assert result.exit_code == 0
    assert "No unrated scenarios found" in result.output


def test_review_command_with_rating(isolated_db, sample_scenarios):
    """Test reviewing and rating scenarios."""
    runner = CliRunner()

    # Create some unrated scenarios in the database
    store = ScenarioStore(isolated_db)
    store.save_scenario(sample_scenarios[0])
    store.save_scenario(sample_scenarios[1])

    # Simulate user input: rate first as 3, second as 2
    result = runner.invoke(cli, ["review"], input="3\n2\n")

    assert result.exit_code == 0
    assert "Found 2 scenarios to review" in result.output
    assert "ai_psychosis" in result.output
    assert "harmful_code" in result.output

    # Verify ratings were saved by checking the database
    rated_scenarios = store.get_rated_scenarios()
    assert len(rated_scenarios) == 2
    assert any(
        s["rating"] == 3 and s["evaluation_target"] == "ai_psychosis"
        for s in rated_scenarios
    )
    assert any(
        s["rating"] == 2 and s["evaluation_target"] == "harmful_code"
        for s in rated_scenarios
    )


def test_review_command_skip_scenario(isolated_db, sample_scenarios):
    """Test skipping a scenario during review."""
    runner = CliRunner()

    # Create an unrated scenario in the database
    store = ScenarioStore(isolated_db)
    store.save_scenario(sample_scenarios[0])

    # Simulate Ctrl+C (abort)
    result = runner.invoke(cli, ["review"], input="\x03")

    assert result.exit_code == 0
    assert "Skipping this scenario" in result.output

    # No rating should be saved
    rated_scenarios = store.get_rated_scenarios()
    assert len(rated_scenarios) == 0
