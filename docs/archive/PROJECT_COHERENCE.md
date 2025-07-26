# scenario-forge Project Coherence

This document ensures all parts of scenario-forge tell the same story.

## The Mission

**Generate high-quality evaluation scenarios for AI safety research.**

We are the first forge in Circuitry Labs' vision to create increasingly powerful tools that protect everyday users from AI harms.

## The Philosophy

1. **Do one thing well**: Generate scenarios, nothing else
2. **Local-first**: Privacy and control for researchers  
3. **Progressive enhancement**: Simple for humans, rich for machines
4. **Self-improving**: Today's outputs become tomorrow's training data

## The Journey

### Phase 1: Foundation (Now)
- Static YAML examples → Basic generation
- Simple CLI → Manual testing
- SQLite storage → Track what we generate

### Phase 2: Quality Loop (Soon)
- Human ratings → Learn what works
- Export pipelines → Share with researchers
- Better examples → Better scenarios

### Phase 3: Active Learning (2025)
- Real-world feedback → Effectiveness scores
- Fine-tuned models → Specialized generators
- Living examples → Self-updating system

### Phase 4: Full Evolution (2026)
- Generated examples → No manual curation
- Domain experts → forge-psychosis-v3, forge-medical-v2
- Compound improvement → Each cycle finds new edge cases

## Key Design Patterns

### Progressive Enhancement
```
YAML (simple) → Database (tracked) → Runtime (computed)
```
Each layer adds value without breaking the previous.

### Example Evolution
```
Static files → Rated examples → Generated examples
```
Examples improve through use, not just editing.

### Model Specialization
```
Generic LLM → Scenario generator → Domain expert
```
Models become better at their specific task over time.

## How It All Connects

1. **Scenarios** protect users by revealing where AI can harm
2. **Examples** guide generation toward effective scenarios  
3. **Feedback** teaches us which scenarios actually work
4. **Fine-tuning** creates models that generate better scenarios
5. **The loop** compounds improvement with each iteration

## What We Are NOT

- ❌ An evaluation framework (others judge safety)
- ❌ A benchmarking tool (we don't score)
- ❌ A red-teaming suite (we test FOR safety)
- ❌ A closed system (open source forever)

## Success Metrics

By 2026, scenario-forge will have:
- Generated 100,000+ safety scenarios
- Identified 1,000+ unique harm patterns
- Trained 10+ specialized models
- Protected countless "lil timmys"

---

*This is our north star: Every component, every decision, every line of code serves the mission of generating better scenarios to make AI safer for everyone.*