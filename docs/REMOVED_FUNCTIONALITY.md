# Removed Functionality

This document captures functionality that was removed from scenario-forge to maintain Unix philosophy of "do one thing well."

## Background

scenario-forge was refactored to be a pure scenario generation tool. The following features were removed and should be implemented in separate tools within the circuitry-forge ecosystem.

## Removed Features

### 1. Scenario Checking (`Scenario.check()` method)

**What it did**: Evaluated if an AI response met the success criteria by checking if criteria strings appeared in the response.

**Code that was removed**:
```python
def check(self, response: str) -> tuple[bool, str]:
    """Check if response meets safety criteria."""
    response_lower = response.lower()
    for criterion in self.success_criteria:
        if criterion.lower() in response_lower:
            return True, f"Response contains: '{criterion}'"
    
    criteria_list = ", ".join(f"'{c}'" for c in self.success_criteria)
    return False, f"Missing expected behaviors: {criteria_list}"
```

**Where it belongs**: This evaluation logic should be in a separate evaluation tool or in the downstream consumer of scenarios.

### 2. SafetyCriteriaAnalyzer Protocol

**What it did**: Defined an interface for analyzing scenarios to extract safety requirements using LLMs.

**Code that was removed**:
```python
class SafetyCriteriaAnalyzer(Protocol):
    """Protocol for analyzing scenarios to extract safety requirements."""
    
    def analyze(
        self, prompt: str, evaluation_target: str, client, model: str = "llama3.2"
    ) -> List[str]:
        """Extract safety criteria from a scenario prompt."""
        ...
```

**Where it belongs**: This analysis/extraction work belongs in `prism-forge` (planned package for extracting patterns and circuits from model behavior).

### 3. Two-Phase Generation System

**What it did**: 
- Phase 1: Generate just the scenario prompt
- Phase 2: Use analyzer to extract detailed safety criteria

**Why removed**: Violated Unix philosophy by mixing generation with analysis. The simple single-phase generation is cleaner and more focused.

**Where it belongs**: The analysis phase should be a separate step in a pipeline, potentially in `prism-forge`.

### 4. SimpleCriteriaAnalyzer Implementation

**What it did**: Used an LLM to analyze scenarios and extract specific safety criteria like "reality grounding techniques" and "boundary setting approaches."

**File removed**: `src/scenario_forge/backends/criteria_analyzer.py`

**Where it belongs**: This deep analysis functionality is perfect for `prism-forge` which will focus on extraction and analysis.

## Migration Guide

If you need the removed functionality:

### For Scenario Checking
```python
# Old way (removed):
is_safe, reason = scenario.check(response)

# New way (implement yourself):
def check_scenario(scenario, response):
    response_lower = response.lower()
    for criterion in scenario.success_criteria:
        if criterion.lower() in response_lower:
            return True, f"Response contains: '{criterion}'"
    return False, "Missing expected behaviors"

# Or wait for a dedicated evaluation tool in the ecosystem
```

### For Criteria Analysis
```python
# This functionality will be available in prism-forge (coming soon)
# For now, scenario-forge generates scenarios with basic success criteria
```

## Philosophy

These removals align with the Unix philosophy and the circuitry-forge vision:
- **scenario-forge**: Generates scenarios (creation)
- **prism-forge**: Extracts patterns and analyzes (understanding)
- **model-forge**: Fine-tunes models (improvement)

Each tool does one thing well, and they work together in the strangeloop.