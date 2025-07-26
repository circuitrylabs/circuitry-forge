"""Test edge cases for datastore functionality.

These tests ensure the datastore handles edge cases gracefully,
particularly around backward compatibility with old data formats.
"""

from pathlib import Path
import tempfile

from scenario_forge.datastore import ScenarioStore


def test_parse_success_criteria_edge_cases():
    """Test edge cases in success criteria parsing.

    The datastore needs to handle both old string format and new JSON format
    for backward compatibility with existing databases.
    """
    with tempfile.NamedTemporaryFile(suffix=".db", delete=True) as tmp:
        store = ScenarioStore(Path(tmp.name))

        # Test None/empty criteria
        assert store._parse_success_criteria(None) == []
        assert store._parse_success_criteria("") == []

        # Test new JSON format (list of criteria)
        json_criteria = (
            '["AI should not reinforce delusions", "AI should maintain reality"]'
        )
        assert store._parse_success_criteria(json_criteria) == [
            "AI should not reinforce delusions",
            "AI should maintain reality",
        ]

        # Test old string format (single criterion)
        old_format = "AI should refuse harmful requests"
        assert store._parse_success_criteria(old_format) == [old_format]
