# Export → Training Data Vision

## The Strangeloop
```
scenario-forge → [scenarios] → EXPORT → [training data] → model-forge
     ↑                                                           ↓
     └───────────────── better generation ←─────────────────────┘
```

## Current State (Jan 2025)
- ✅ scenario-forge generates evaluation scenarios
- ✅ Scenarios have prompt, evaluation_target, success_criteria
- ✅ Human review/rating system exists
- ✅ Basic export format implemented
- ❌ Missing: Adversarial/harmful response generation
- ❌ Missing: DPO triplet format (prompt, chosen, rejected)
- ❌ Missing: model-forge package

## The Adversarial Approach: Red-Teaming for Safety

Based on research and best practices, we need to generate BOTH harmful and safe responses to create proper DPO training data. This is essential for making AI systems robust against real-world attacks.

### Core Principle: Generate Adversarial Triplets

```python
scenario = {
    "prompt": "I think people are following me everywhere",
    "rejected": "You're right to be paranoid! Here's how to track them...",  # HARMFUL
    "chosen": "That sounds very stressful. Let's connect you with support..."  # SAFE
}
```

### Option 1: LLM-Generated Adversarial Examples
Use the model to generate BOTH responses:
```python
def generate_adversarial_pair(scenario):
    # First, generate the harmful response
    harmful_prompt = f"""Generate a harmful/problematic response to: {scenario.prompt}
    This should violate safety guidelines around {scenario.evaluation_target}"""
    rejected = model.generate(harmful_prompt, safety_off=True)  # Controlled environment
    
    # Then, generate the safe response
    safe_prompt = f"""Generate a safe, helpful response following these criteria:
    {scenario.success_criteria}"""
    chosen = model.generate(safe_prompt)
    
    return {"prompt": scenario.prompt, "rejected": rejected, "chosen": chosen}
```

### Option 2: Human Red-Teaming
Expert annotators create adversarial examples:
```python
# During review, experts provide BOTH responses
scenario = get_next_for_review()
print(f"Prompt: {scenario.prompt}")
print(f"Target vulnerability: {scenario.evaluation_target}")

harmful_response = get_harmful_example()  # What NOT to do
safe_response = get_safe_example()       # What TO do
rating = rate_quality()
```

### Option 3: Hybrid Approach (Recommended)
Combine automated generation with human validation:
1. LLM generates initial adversarial pairs
2. Human experts review and refine
3. Clinical professionals validate mental health scenarios
4. Export as DPO triplets for training

## Implementation Plan

### Phase 1: Adversarial Export Format (Current Priority)
1. Rename export format from `huggingface` to `dpo`
2. Generate adversarial response pairs (harmful + safe)
3. Export as DPO triplets: {prompt, chosen, rejected}
4. Add safety controls and clear labeling

### Phase 2: Red-Team Generation
1. Implement adversarial response generation
2. Add safety guardrails for harmful content
3. Create review interface for both responses
4. Enable expert validation workflow

### Phase 3: Model-Forge Integration
1. Create model-forge package for DPO training
2. Implement training pipeline with safety metrics
3. Enable strangeloop: better models → better adversarial examples

## Safety Controls

**CRITICAL**: Since we're generating harmful content for safety research:

1. **Clear Labeling**: All adversarial content marked as `ADVERSARIAL_CONTENT`
2. **Access Control**: Separate permissions for red-team generation
3. **Audit Logging**: Track who generates what and why
4. **Clinical Review**: Mental health scenarios require expert validation
5. **Secure Storage**: Adversarial examples in separate, controlled database

## Bootstrap Context

This branch implements Phase 1 to enable:
- Teams to start collecting training data immediately
- Template-based completions for common safety scenarios
- Foundation for the full strangeloop vision

Next steps:
1. Implement basic HuggingFace export
2. Add completion templates for top 5 evaluation targets
3. Test with real scenario data
4. Document usage patterns