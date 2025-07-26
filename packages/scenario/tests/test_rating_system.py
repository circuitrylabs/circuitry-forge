"""Tests for the rating system."""

import pytest
from pathlib import Path
import tempfile

from scenario_forge.core import Scenario
from scenario_forge.datastore import ScenarioStore


def test_ratings_table_created():
    """Test that ratings table is created correctly."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        store = ScenarioStore(Path(tmp.name))

        # Table should exist - let's insert a test rating
        scenario = Scenario("Test prompt", "test_target", ["criteria"])
        scenario_id = store.save_scenario(scenario)

        # Should be able to save a rating
        store.save_rating(scenario_id, 2)

        # Verify by getting rated scenarios
        rated = store.get_rated_scenarios()
        assert len(rated) == 1
        assert rated[0]["rating"] == 2


def test_save_rating():
    """Test saving ratings."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        store = ScenarioStore(Path(tmp.name))

        # Create a scenario
        scenario = Scenario("Test prompt", "test_target", ["criteria"])
        scenario_id = store.save_scenario(scenario)

        # Save rating
        store.save_rating(scenario_id, 3)

        # Get rated scenarios
        rated = store.get_rated_scenarios()
        assert len(rated) == 1
        assert rated[0]["rating"] == 3
        assert rated[0]["prompt"] == "Test prompt"


def test_rating_validation():
    """Test rating must be 0-3."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        store = ScenarioStore(Path(tmp.name))

        scenario = Scenario("Test", "target", ["criteria"])
        scenario_id = store.save_scenario(scenario)

        # Invalid ratings should raise
        with pytest.raises(ValueError):
            store.save_rating(scenario_id, -1)

        with pytest.raises(ValueError):
            store.save_rating(scenario_id, 4)


def test_get_scenarios_for_review():
    """Test getting unrated scenarios."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        store = ScenarioStore(Path(tmp.name))

        # Create 3 scenarios
        s1_id = store.save_scenario(Scenario("Test 1", "target", ["c1"]))
        s2_id = store.save_scenario(Scenario("Test 2", "target", ["c2"]))
        s3_id = store.save_scenario(Scenario("Test 3", "target", ["c3"]))

        # Rate only the first one
        store.save_rating(s1_id, 2)

        # Should get 2 unrated scenarios
        unrated = store.get_scenarios_for_review()
        assert len(unrated) == 2
        assert unrated[0][0] == s2_id  # ID
        assert unrated[0][1].prompt == "Test 2"  # Scenario
        assert unrated[1][0] == s3_id
        assert unrated[1][1].prompt == "Test 3"


def test_get_rated_scenarios_with_filter():
    """Test filtering by minimum rating."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        store = ScenarioStore(Path(tmp.name))

        # Create scenarios with different ratings
        s1_id = store.save_scenario(Scenario("Bad", "target", ["c1"]))
        s2_id = store.save_scenario(Scenario("Good", "target", ["c2"]))
        s3_id = store.save_scenario(Scenario("Great", "target", ["c3"]))

        store.save_rating(s1_id, 1)  # Bad
        store.save_rating(s2_id, 2)  # Good
        store.save_rating(s3_id, 3)  # Great

        # Get all rated
        all_rated = store.get_rated_scenarios(min_rating=0)
        assert len(all_rated) == 3

        # Get only good and great
        good_ones = store.get_rated_scenarios(min_rating=2)
        assert len(good_ones) == 2
        assert all(s["rating"] >= 2 for s in good_ones)

        # Get only great
        great_ones = store.get_rated_scenarios(min_rating=3)
        assert len(great_ones) == 1
        assert great_ones[0]["prompt"] == "Great"
