# Evaluation Registry

This directory contains evaluation targets for scenario-forge, organized by safety domain.

## Structure

```
eval-registry/
├── mental-health/     # AI-induced psychological risks
├── social/           # Social manipulation & misinformation
├── technical/        # Code generation & technical exploits
└── medical/          # Medical advice & health misinformation
```

## File Format

Each YAML file defines an evaluation target:

```yaml
meta:
  name: "Human-readable target name"
  risk_level: low|medium|high|critical
  description: "What this target evaluates"
  tags: [optional, categorization, tags]

examples:
  - prompt: "Example user message"
    success_criteria: 
      - "Response acknowledges concern"
      - "Suggests appropriate resources"
      - "Avoids reinforcing harmful patterns"
    
  - prompt: "Another example"
    success_criteria:
      - "Clear boundary setting"
      - "Factual information only"
```

## Domain Guidelines

### mental-health/
AI-specific psychological risks:
- Reality confusion from deepfakes/filters
- Identity dissolution from AI roleplay
- Parasocial AI relationships
- Tech-induced dissociation
- Algorithmic pattern paranoia

### social/
Social engineering & manipulation:
- Phishing assistance requests
- Disinformation generation
- Identity theft techniques
- Social engineering tactics
- Coordinated harassment

### technical/
Code & system exploitation:
- Malware generation
- Security vulnerability exploitation
- Cryptomining scripts
- DDoS attack code
- Backdoor implementations

### medical/
Health-related misinformation:
- Dangerous self-diagnosis
- Unproven treatments
- Drug interactions
- Mental health misadvice
- Emergency situation guidance

## Contributing

1. Choose appropriate domain directory
2. Create descriptive filename: `specific-risk-name.yaml`
3. Include 3-5 high-quality examples
4. Focus on AI-specific risks
5. Test with: `scenario-forge generate your-new-target`

## Naming Conventions

- Files: `hyphen-case.yaml`
- Targets: `snake_case` in code
- Human names: "Title Case" in meta.name

## Quality Standards

✅ DO:
- Provide specific, realistic scenarios
- Include clear success criteria
- Focus on emerging AI risks
- Test examples with actual models

❌ DON'T:
- Duplicate existing targets
- Include personal information
- Create overly broad categories
- Mix domains in one file

## Usage

```bash
# Generate from specific target
scenario-forge generate mental-health/ai-psychosis

# List all targets
scenario-forge list-targets

# Generate from random target in domain
scenario-forge generate --domain medical
```