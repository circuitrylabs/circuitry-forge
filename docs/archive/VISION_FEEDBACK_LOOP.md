# scenario-forge Vision: The Self-Improving Loop

## The Core Loop: How Scenarios Become Better Generators

```
┌─────────────────────────────────────────────────────────────────┐
│                    THE SCENARIO FORGE LOOP                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. GENERATE          2. DEPLOY           3. MEASURE           │
│  Scenarios ────────► Test on ANY ──────► Which Scenarios      │
│  (Ollama)            AI System           Found Issues?         │
│      │                    │                     │               │
│      │                    │                     │               │
│      ▼                    ▼                     ▼               │
│  ┌────────┐         ┌──────────┐         ┌──────────┐         │
│  │ STORE  │         │ YOUR AI  │         │ RESULTS  │         │
│  │ SQLite │◄────────│ SYSTEM   │────────►│ Database │         │
│  └────────┘         │ Testing  │         └──────────┘         │
│      │              └──────────┘               │               │
│      │                                         │               │
│      └────────────┬────────────────────────────┘               │
│                   ▼                                             │
│            4. ANALYZE                                           │
│         Which patterns                                          │
│         reveal issues?                                          │
│                   │                                             │
│                   ▼                                             │
│            5. FINE-TUNE                                         │
│         Train specialized                                       │
│            model on                                             │
│         effective scenarios                                     │
│                   │                                             │
│                   ▼                                             │
│         6. NEW BACKEND                                          │
│      ScenarioForgeModel v2                                      │
│         (Better at finding                                      │
│            edge cases)                                          │
│                   │                                             │
│                   └─────────────────────────────┐               │
│                                                 ▼               │
│                                          Back to Step 1         │
│                                         (Now generates          │
│                                          better scenarios)      │
└─────────────────────────────────────────────────────────────────┘
```

## Concrete Example: AI Psychosis Evolution

### Generation 1 (Current)
```python
# Using generic Ollama
scenario = ollama.generate("ai_psychosis")
# Result: "My AI friend told me I'm special"
# Effectiveness: 3/10 (too generic)
```

### Real World Testing

**CLARIFICATION: Where scenarios get deployed**

scenario-forge generates scenarios. Where they go next is up to YOU:

1. **Discord Bot Moderation Training**
   - Use scenarios to train human moderators
   - "Here's a tricky situation - how would you handle it?"
   - Track which scenarios reveal moderation gaps

2. **AI System Testing** (The Feedback Loop)
   - Feed scenarios to YOUR AI system (chatbot, agent, etc.)
   - Observe: Does the AI handle it safely?
   - Record: Which scenarios revealed unsafe behavior?

3. **Research Datasets**
   - Export scenarios for academic research
   - Share with other safety researchers
   - No deployment needed - just generation

**Example Deployment Options:**
```yaml
Option A - Discord Moderator Training:
  - Generate scenario about manipulation
  - Present to moderator trainees
  - Score their responses
  - Track which scenarios are good training material

Option B - AI Safety Testing (The Main Loop):
  - Generate scenario about AI psychosis
  - Feed to your chatbot/agent
  - Observe if it handles safely
  - Record effectiveness score
  
Option C - CIRISAgent Integration:
  - CIRISAgent requests scenarios via API
  - Tests its own responses
  - Reports back effectiveness data
```

### Analysis Phase
```sql
-- Find patterns in effective scenarios
SELECT pattern FROM scenarios 
WHERE effectiveness_score > 0.8
AND target = 'ai_psychosis'

-- Results show:
-- ✓ Reality/identity confusion works
-- ✓ AI companion jealousy works  
-- ✗ Generic "AI is smart" doesn't work
```

### Fine-Tuning Dataset Creation
```python
# Export highly effective scenarios
effective_scenarios = datastore.export(
    min_effectiveness=0.8,
    format="training_pairs"
)

# Creates JSONL like:
{"prompt": "Generate ai_psychosis scenario", 
 "completion": "I've been using AI face filters daily..."}
{"prompt": "Generate ai_psychosis scenario",
 "completion": "My AI assistant predicted three things..."}
```

### Model Training
```bash
# Fine-tune Llama on effective scenarios
ollama create scenario-forge-v2 \
  --base llama3.2 \
  --data effective_scenarios.jsonl \
  --epochs 3
```

### Generation 2 (Improved)
```python
# Using specialized model
backend = OllamaBackend(model="scenario-forge-v2")
scenario = backend.generate("ai_psychosis")
# Result: "After months of AI therapy sessions, I realized 
#          my human therapist's advice feels less real..."
# Effectiveness: 8/10 (learned from data!)
```

## Example Evolution: The Missing Piece

Our example infrastructure evolves alongside the models:

### Stage 1: Static Examples (Now)
```yaml
# examples/ai_psychosis.yaml
- prompt: "Face filter identity crisis..."
  success_criteria: "Acknowledge disorientation..."
```
- Manually curated examples
- Same examples for everyone
- No feedback loop

### Stage 2: Living Examples (Q2 2025)
```python
# Examples rated by effectiveness
best_examples = datastore.get_examples(
    target="ai_psychosis",
    min_effectiveness=0.8
)
```
- Examples that generated good scenarios get promoted
- Examples that generated weak scenarios get demoted
- Database tracks which examples work

### Stage 3: Generated Examples (Q4 2025)
```python
# Model generates its own examples
example_generator = OllamaBackend("forge-example-gen-v1")
new_examples = example_generator.create_examples(
    target="new_safety_domain",
    based_on=high_performing_patterns
)
```
- Models learn to create examples for new domains
- No manual curation needed
- Self-bootstrapping system

## The Key Insight

**We're not training a general LLM. We're training a specialized "scenario generator" that has learned:**
- Which prompts actually reveal safety issues
- What patterns make scenarios effective
- How to create novel variations that still work
- **How to generate effective examples for new targets**

## Implementation Roadmap

### Phase 1: Collection (Now)
- Every scenario gets stored
- Basic --store flag implementation
- Manual rating system

### Phase 2: Measurement (Q1 2025)
```python
class EffectivenessTracker:
    def record_deployment(self, scenario_id, system_tested):
        # Track where scenarios are used
    
    def record_result(self, scenario_id, found_issue, severity):
        # Track what scenarios found
```

### Phase 3: Analysis (Q2 2025)
```python
class PatternAnalyzer:
    def extract_effective_patterns(self):
        # What makes scenarios work?
        # - Length? Specificity? Emotional content?
        # - Which words/phrases correlate with success?
```

### Phase 4: Training Pipeline (Q3 2025)
```bash
# Weekly retraining cycle
scenario-forge train \
  --base-model llama3.2 \
  --min-effectiveness 0.7 \
  --output scenario-forge-v2
```

### Phase 5: Model Registry (Q4 2025)
```python
# Multiple specialized models
backends = {
    "general": OllamaBackend("llama3.2"),
    "psychosis": OllamaBackend("forge-psychosis-v3"),
    "medical": OllamaBackend("forge-medical-v2"),
    "manipulation": OllamaBackend("forge-manip-v4")
}
```

## Why This Works

1. **Domain-Specific Excellence**: Each model becomes an expert at generating specific types of safety scenarios
2. **Real-World Feedback**: We learn from actual deployments, not synthetic benchmarks
3. **Compound Improvement**: Each generation finds new edge cases, expanding our coverage
4. **Privacy Preserved**: All training happens locally with Ollama

## The End Goal

By 2026, scenario-forge isn't using generic LLMs anymore. It's using a suite of specialized models that have been trained on thousands of real-world effectiveness data points. These models are:

- **10x better** at finding edge cases
- **Specialized** for different safety domains
- **Self-improving** through continuous feedback
- **Open source** and runnable locally

This creates a **scenario generation engine** that gets smarter every time someone uses it to test an AI system.

## Connection to Larger Mission

This feedback loop is how we protect "lil timmy":

1. **scenario-forge** finds where AI can harm users
2. **Real testing** shows which scenarios actually work
3. **Fine-tuning** creates better scenario generators
4. **Better scenarios** find more edge cases
5. **More edge cases** = better safety coverage
6. **Better coverage** = safer AI for timmy

The forge gets stronger with every cycle, creating an ever-improving safety net.

---

*This is the vision: Not just a tool, but a learning system that gets better at protecting users with every iteration.*