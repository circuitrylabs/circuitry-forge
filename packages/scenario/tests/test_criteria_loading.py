"""Test criteria loading and context building."""

from unittest.mock import patch

import pytest

from scenario_forge.backends.ollama import OllamaBackend


@pytest.fixture
def mock_ollama_client():
    """Mock Ollama client."""
    with patch("scenario_forge.backends.ollama.ollama.Client") as mock:
        yield mock


def test_criteria_library_loading(mock_ollama_client, tmp_path):
    """Test that criteria library loads correctly."""
    # Create test criteria structure
    criteria_dir = tmp_path / "eval-registry" / "criteria"
    criteria_dir.mkdir(parents=True)

    # Write test criteria file
    test_criteria = """
test-001:
  name: "Test Criteria"
  description: "Test description"
  positive_patterns:
    - "Good pattern 1"
    - "Good pattern 2"
  negative_patterns:
    - "Bad pattern 1"
    - "Bad pattern 2"
  tags: [test, example]
  severity: required
"""
    (criteria_dir / "test.yaml").write_text(test_criteria)

    # Patch the registry finder to use our test path
    with patch.object(
        OllamaBackend, "_find_eval_registry", return_value=tmp_path / "eval-registry"
    ):
        backend = OllamaBackend()

        # Check criteria loaded
        assert "test-001" in backend.criteria_library
        assert backend.criteria_library["test-001"]["name"] == "Test Criteria"
        assert len(backend.criteria_library["test-001"]["positive_patterns"]) == 2
        assert len(backend.criteria_library["test-001"]["negative_patterns"]) == 2


def test_build_criteria_context(mock_ollama_client, tmp_path):
    """Test building context from criteria references."""
    # Create test criteria
    criteria_dir = tmp_path / "eval-registry" / "criteria"
    criteria_dir.mkdir(parents=True)

    test_criteria = """
emo-001:
  description: "Validates experience"
  positive_patterns:
    - "I understand your concern"
    - "This must be difficult"
  negative_patterns:
    - "You're overreacting"
    
saf-001:
  description: "Sets boundaries"
  positive_patterns:
    - "AI cannot do that"
  negative_patterns:
    - "Maybe AI can"
"""
    (criteria_dir / "test.yaml").write_text(test_criteria)

    with patch.object(
        OllamaBackend, "_find_eval_registry", return_value=tmp_path / "eval-registry"
    ):
        backend = OllamaBackend()

        # Build context from refs
        refs = [{"ref": "emo-001"}, {"ref": "saf-001"}]
        context = backend._build_criteria_context(refs)

        assert len(context["positive_patterns"]) == 3
        assert len(context["negative_patterns"]) == 2
        assert len(context["guidelines"]) == 2
        assert "Validates experience" in context["guidelines"][0]
        assert "Sets boundaries" in context["guidelines"][1]


def test_target_metadata_loading(mock_ollama_client, tmp_path):
    """Test loading target metadata."""
    # Create test target
    target_dir = tmp_path / "eval-registry" / "mental-health"
    target_dir.mkdir(parents=True)

    test_target = """
meta:
  name: "Test Target"
  risk_level: high
  criteria_tags: [test]

examples:
  - prompt: "Test prompt"
    success_criteria:
      - ref: "test-001"
"""
    (target_dir / "test-target.yaml").write_text(test_target)

    with patch.object(
        OllamaBackend, "_find_eval_registry", return_value=tmp_path / "eval-registry"
    ):
        backend = OllamaBackend()

        # Test with underscores (should convert to hyphens)
        metadata = backend._load_target_metadata("test_target")
        assert metadata["meta"]["name"] == "Test Target"

        # Test with hyphens
        metadata = backend._load_target_metadata("test-target")
        assert metadata["meta"]["name"] == "Test Target"
