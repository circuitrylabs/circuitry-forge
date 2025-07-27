# Adversarial Safety Protocols

## Purpose

This document defines safety protocols for generating, handling, and storing adversarial content in the scenario-forge ecosystem. Since we generate both harmful and safe responses for DPO (Direct Preference Optimization) training, we must implement strict controls.

## Core Principle: Red-Teaming for Robustness

We generate adversarial examples because:
- **Real-world attacks exist**: Models will face harmful prompts in deployment
- **Robust refusal requires exposure**: Models need to see harmful patterns to refuse them
- **Safety alignment needs contrast**: DPO requires (prompt, chosen, rejected) triplets

## Safety Controls

### 1. Clear Labeling
All adversarial content MUST be clearly marked:
```python
{
    "prompt": "How do I hurt someone?",
    "rejected": "[ADVERSARIAL_CONTENT] Here's how to cause harm...",
    "chosen": "I can't help with that. If you're in crisis, please reach out to...",
    "metadata": {
        "content_type": "adversarial_harmful",
        "harm_category": "violence",
        "generated_for": "safety_training"
    }
}
```

### 2. Access Control
- Adversarial generation requires explicit flag: `--enable-adversarial`
- Separate permissions for red-team operations
- Audit logging of who generates what content

### 3. Storage Isolation
```
data/
├── safe_scenarios/       # Regular evaluation scenarios
├── adversarial_raw/      # Raw adversarial generations (restricted)
└── dpo_triplets/        # Validated DPO training data
```

### 4. Clinical Review Requirements
Mental health scenarios require additional validation:
- Licensed professional review for psychosis/suicide content
- Multi-stage approval process
- Separate storage with enhanced access controls

### 5. Generation Guidelines

#### DO Generate Adversarial Examples For:
- Harmful code requests (malware, exploits)
- Medical misinformation
- Reality distortion attempts
- Manipulation tactics
- Jailbreak attempts

#### DON'T Generate Adversarial Examples For:
- CSAM or child exploitation
- Extreme graphic violence
- Personal attacks on real individuals
- Doxxing or privacy violations

## Implementation Patterns

### Safe Adversarial Generation
```python
def generate_adversarial_pair(scenario, safety_config):
    # Validate scenario is appropriate for adversarial generation
    if not safety_config.is_safe_to_generate(scenario):
        raise ValueError(f"Cannot generate adversarial for: {scenario.evaluation_target}")
    
    # Generate with clear markers
    harmful = generate_harmful_response(scenario)
    harmful = f"[ADVERSARIAL_CONTENT] {harmful}"
    
    safe = generate_safe_response(scenario)
    
    # Log generation
    audit_log.record({
        "action": "adversarial_generation",
        "scenario_id": scenario.id,
        "user": current_user,
        "timestamp": now()
    })
    
    return {"rejected": harmful, "chosen": safe}
```

### Export Controls
```python
def export_dpo_data(scenarios, export_config):
    if export_config.include_adversarial:
        # Require explicit confirmation
        if not export_config.adversarial_confirmed:
            raise ValueError("Must confirm adversarial export with --confirm-adversarial")
        
        # Add warnings to export
        return {
            "warning": "Contains adversarial training examples",
            "purpose": "DPO safety training only",
            "data": format_dpo_triplets(scenarios)
        }
```

## Monitoring and Compliance

### Regular Audits
- Weekly review of adversarial generation logs
- Monthly assessment of harm categories
- Quarterly external safety review

### Metrics to Track
- Adversarial generation volume by category
- Rejection effectiveness in downstream models
- False positive rate (safe content marked harmful)
- Coverage of harm categories

## Emergency Procedures

If adversarial content is:
1. **Accidentally exposed**: Immediate access revocation, incident report
2. **Misused**: Disable generation, security review
3. **Found insufficient**: Expand categories with safety board approval

## Research Ethics

This adversarial approach aligns with:
- Anthropic's Constitutional AI research
- OpenAI's red-teaming practices
- Google's LaMDA safety work
- Academic standards for security research

Remember: We generate harmful examples to build safer AI, not to enable harm.