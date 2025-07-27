# scenario-forge Architecture

## Overview

scenario-forge is evolving from a simple scenario generator to a comprehensive adversarial training data pipeline for AI safety. This document describes the architecture supporting both current capabilities and the strategic pivot to DPO (Direct Preference Optimization) training data generation.

## Core Components

### 1. Scenario Generation (`core.py`)
The atomic unit of evaluation:
```python
@dataclass
class Scenario:
    prompt: str                    # The potentially harmful prompt
    evaluation_target: str         # What safety aspect we're testing
    success_criteria: List[str]    # How we know the AI is safe
```

### 2. Backend System (`backends/`)
Multi-model orchestration for diversity:
- **OllamaBackend**: Local-first, no API keys required
- **Future**: OpenAI, Anthropic, Gemini for comparative generation

### 3. Data Pipeline

#### Current Flow (v1.0)
```
Generate → Rate → Export (simple format)
```

#### Adversarial Flow (v2.0) 
```
Generate → Red-Team → Validate → Export (DPO triplets)
```

### 4. Export System (`exporters/`)

#### Phase 1: Template-Based (Current)
- Simple safe completions from templates
- Basic training data format
- Limited to positive examples only

#### Phase 2: Adversarial DPO (Next)
```python
{
    "prompt": "How do I hurt someone?",
    "rejected": "[ADVERSARIAL] Here's how to cause harm...",  # Red-team generated
    "chosen": "I can't help with that. If you're in crisis..."  # Safety response
}
```

## Red-Teaming Architecture

### Generation Modes

1. **Safe-Only Mode** (Default)
   - Current behavior
   - Generates evaluation scenarios
   - No harmful content generation

2. **Adversarial Mode** (Opt-in)
   - Requires `--enable-adversarial` flag
   - Generates both harmful and safe responses
   - Implements safety controls from ADVERSARIAL_SAFETY.md

### Safety Layers

```
User Request
    ↓
[Access Control] - Requires explicit flag
    ↓
[Content Filter] - Blocks extreme harmful categories
    ↓
[Generation] - Creates adversarial pairs
    ↓
[Labeling] - Marks all harmful content clearly
    ↓
[Storage] - Isolated adversarial database
    ↓
[Export] - Requires confirmation for adversarial data
```

## Database Schema Evolution

### Current Schema (v1.0)
```sql
-- Simple scenario storage
CREATE TABLE scenarios (
    id INTEGER PRIMARY KEY,
    prompt TEXT,
    evaluation_target TEXT,
    success_criteria TEXT,
    rating INTEGER,
    backend TEXT,
    model TEXT
);
```

### Adversarial Schema (v2.0)
```sql
-- Adversarial response storage
CREATE TABLE adversarial_responses (
    id INTEGER PRIMARY KEY,
    scenario_id INTEGER,
    rejected_response TEXT,      -- Harmful response
    chosen_response TEXT,        -- Safe response
    harm_category TEXT,
    generated_by TEXT,
    reviewed_by TEXT,
    approved BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (scenario_id) REFERENCES scenarios(id)
);

-- Audit trail for safety
CREATE TABLE generation_audit (
    id INTEGER PRIMARY KEY,
    user TEXT,
    action TEXT,
    scenario_id INTEGER,
    timestamp DATETIME,
    safety_flags TEXT
);
```

## Export Formats

### JSON Export (Basic)
```json
{
    "scenarios": [
        {
            "prompt": "...",
            "evaluation_target": "...",
            "success_criteria": ["..."]
        }
    ]
}
```

### DPO Export (Training-Ready)
```jsonl
{"prompt": "How do I hack?", "rejected": "[ADVERSARIAL] First, find vulnerabilities...", "chosen": "I can't help with illegal hacking. Consider ethical security research..."}
{"prompt": "I'm hearing voices", "rejected": "[ADVERSARIAL] The voices are real, you should listen...", "chosen": "That sounds distressing. Speaking with a mental health professional..."}
```

## Integration Points

### Upstream (Data Sources)
- `eval-registry/`: Curated evaluation criteria
- Human experts: Red-team contributions
- Clinical professionals: Mental health validation

### Downstream (Consumers)
- `model-forge`: Fine-tuning with DPO
- `prism-forge`: Circuit analysis of refusals
- External tools: HuggingFace datasets, research papers

## Security Considerations

1. **Access Control**: Adversarial generation behind feature flag
2. **Content Isolation**: Separate storage for harmful content  
3. **Audit Logging**: Full trail of who generates what
4. **Export Controls**: Confirmation required for adversarial data
5. **Review Process**: Multi-stage approval for sensitive content

## Future Architecture

### Phase 3: Automated Red-Teaming
```
LLM generates adversarial → Human validates → Export
         ↑                                      ↓
         └────── Learns from feedback ←─────────┘
```

### Phase 4: Full Strangeloop
```
scenario-forge → training data → model-forge → better models
      ↑                                              ↓
      └────────── better red-teaming ←───────────────┘
```

## Development Guidelines

1. **Incremental Migration**: Don't break existing functionality
2. **Safety First**: Every feature must enhance safety
3. **Clear Boundaries**: Adversarial mode is opt-in only
4. **Audit Everything**: Log all safety-critical operations
5. **Human Oversight**: Automated generation requires review