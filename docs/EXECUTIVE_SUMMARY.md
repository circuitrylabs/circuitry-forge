# scenario-forge: Executive Summary

## What We're Building

A self-improving AI safety testing system that generates scenarios to find where AI can harm users.

## Why It Matters

- **AI harms evolve faster than we can manually test**
- **Static test suites miss emerging threats**  
- **We need defenses that learn and adapt**

## How It Works

```
Generate Scenarios → Test AI Systems → Measure What Works → 
Train Better Generators → Generate Better Scenarios → Repeat Forever
```

## The Innovation

**We're not training a general AI. We're training specialized "safety scenario generators" that get better at finding edge cases with every use.**

## Key Differentiators

1. **Local-first**: Run entirely on your machine with Ollama
2. **Self-improving**: Gets smarter from real-world feedback
3. **Specialized**: Domain-specific models for different harm types
4. **Open source**: Every line of code, every model weight

## Roadmap

- **NOW**: Basic generation + storage
- **Q1 2025**: Feedback loop + ratings
- **Q2 2025**: First fine-tuned models
- **Q3 2025**: Multi-domain specialists  
- **2026**: Fully autonomous improvement

## For Circuitry Labs

This is our first "forge" - a tool that creates tools. scenario-forge creates the test scenarios that other tools (like CIRISAgent) use to verify AI safety.

## The Ask

1. **Use it**: Generate scenarios for your AI safety testing
2. **Rate it**: Tell us which scenarios actually found issues
3. **Extend it**: Add backends, exporters, integrations
4. **Share it**: More users = faster improvement

## Success Metrics

By 2026:
- 100,000+ scenarios generated
- 1,000+ unique harm patterns discovered
- 10+ specialized models trained
- Measurable reduction in AI harms

## Get Started

```bash
pip install scenario-forge
scenario-forge generate "your_safety_concern" --save
```

---

*Every scenario generated makes AI a little bit safer for someone.*