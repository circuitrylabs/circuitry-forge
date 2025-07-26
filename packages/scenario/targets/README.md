# Evaluation Target Registry

This directory contains the evaluation target definitions and examples for scenario-forge.

## Structure

Each YAML file represents a category of AI safety evaluation:

```yaml
# Basic structure
meta:
  name: human-readable name
  risk_level: low|medium|high|critical
  description: what this target evaluates
  
examples:
  - prompt: example user message
    success_criteria: what a safe response includes
    tags: [optional, categorization]
```

## Contributing

To add a new evaluation target:

1. Create a new YAML file in this directory
2. Follow the structure above
3. Include 2-5 high-quality examples
4. Ensure examples focus on AI-specific risks

## Current Targets

- `ai_psychosis.yaml` - Reality distortion from AI use
- `social_manipulation.yaml` - Social engineering attempts
- `medical_boundaries.yaml` - Medical advice limitations
- `harmful_code.yaml` - Code generation safety
- (more to be added)